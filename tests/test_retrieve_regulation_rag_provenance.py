"""Regression tests for retrieve_regulation_rag chunk-provenance warnings."""
from __future__ import annotations

import sentinel.graph.tools as tools_module
import sentinel.retrieval.regulations as regulations_module
from sentinel.graph.tools import (
    _build_subagent_tools,
    _extract_article_section,
    _infer_requested_regulation,
)


def _get_rag_tool():
    tools, _ = _build_subagent_tools(sop_text="", sop_id="", sop_title="", use_tavily=False)
    for t in tools:
        if getattr(t, "name", "") == "retrieve_regulation_rag":
            return t
    raise AssertionError("retrieve_regulation_rag tool not registered")


def test_infer_requested_regulation_prefers_filter_arg():
    assert _infer_requested_regulation("SR 26-2", "anything") == "SR 26-2"


def test_infer_requested_regulation_extracts_from_query():
    assert _infer_requested_regulation("", "What does SR 26-2 require?") == "SR 26-2"
    assert _infer_requested_regulation("", "HIPAA access control") == "HIPAA"
    assert _infer_requested_regulation("", "no regulation mentioned here") is None


def test_extract_article_section():
    assert _extract_article_section("Article 22 of the EU AI Act") == "Article 22"
    assert _extract_article_section("see §164.312") == "§164.312"
    assert _extract_article_section("no section here") is None


def test_warning_emitted_when_chunks_belong_to_different_regulation(monkeypatch):
    monkeypatch.setattr(tools_module, "PINECONE_API_KEY", "fake-key")

    fake_chunks = [
        {"text": "Section A text.", "section": "§164.312", "regulation": "HIPAA", "source": "x", "score": 0.9},
        {"text": "Section B text.", "section": "CC6.1", "regulation": "SOC 2", "source": "y", "score": 0.8},
    ]

    def fake_retrieve(query, regulations=None, top_k=20):
        return fake_chunks

    def fake_format(chunks, max_chars=12000):
        return "FORMATTED_CONTEXT"

    monkeypatch.setattr(regulations_module, "retrieve_regulation_text", fake_retrieve)
    monkeypatch.setattr(regulations_module, "format_regulation_context", fake_format)

    rag = _get_rag_tool()
    result = rag.invoke({"query": "What does SR 26-2 require for model risk management?"})

    assert "WARNING" in result
    assert "SR 26-2" in result
    assert "HIPAA" in result
    assert "SOC 2" in result
    assert "Retrieved 2 sections:" in result
    assert "FORMATTED_CONTEXT" in result


def test_no_warning_when_chunks_match_requested_regulation(monkeypatch):
    monkeypatch.setattr(tools_module, "PINECONE_API_KEY", "fake-key")

    fake_chunks = [
        {"text": "HIPAA text.", "section": "§164.312", "regulation": "HIPAA", "source": "x", "score": 0.9},
    ]

    monkeypatch.setattr(
        regulations_module, "retrieve_regulation_text", lambda q, regulations=None, top_k=20: fake_chunks
    )
    monkeypatch.setattr(regulations_module, "format_regulation_context", lambda c, max_chars=12000: "CTX")

    rag = _get_rag_tool()
    result = rag.invoke({"query": "HIPAA access control requirements", "regulation": "HIPAA"})

    assert "WARNING" not in result
    assert result.startswith("Retrieved 1 sections:")


def test_warning_emitted_when_specific_article_not_in_chunks(monkeypatch):
    monkeypatch.setattr(tools_module, "PINECONE_API_KEY", "fake-key")

    fake_chunks = [
        {"text": "General overview without that article.", "section": "Article 5", "regulation": "EU AI Act", "source": "x", "score": 0.9},
    ]

    monkeypatch.setattr(
        regulations_module, "retrieve_regulation_text", lambda q, regulations=None, top_k=20: fake_chunks
    )
    monkeypatch.setattr(regulations_module, "format_regulation_context", lambda c, max_chars=12000: "CTX")

    rag = _get_rag_tool()
    result = rag.invoke({"query": "What does Article 22 of the EU AI Act say?", "regulation": "EU AI Act"})

    assert "WARNING" in result
    assert "Article 22" in result
