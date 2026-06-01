"""Regression tests for tool-call arg sanity guards in _build_subagent_tools.

These guard against Nemotron-style autoregressive token-repetition collapse
emitting runaway-token strings into structured tool args.
"""
from __future__ import annotations

from sentinel.graph import tools as tools_mod


def _tool_by_name(tool_list, name):
    for t in tool_list:
        if getattr(t, "name", None) == name:
            return t
    raise AssertionError(f"tool {name!r} not found in {[getattr(t, 'name', None) for t in tool_list]}")


def test_retrieve_regulation_rag_rejects_runaway_repetition(monkeypatch):
    monkeypatch.setattr(tools_mod, "PINECONE_API_KEY", "test-key", raising=False)
    tool_list, _ = tools_mod._build_subagent_tools(
        sop_text="x", sop_id="SOP-1", sop_title="t", use_tavily=False, retrieval="rag"
    )
    rag = _tool_by_name(tool_list, "retrieve_regulation_rag")
    garbage = "foo\n" + ("The" * 200)
    result = rag.invoke({"query": garbage})
    assert "runaway token repetition" in result.lower()


def test_record_finding_rejects_runaway_repetition_in_evidence_quote():
    tool_list, _ = tools_mod._build_subagent_tools(
        sop_text="x", sop_id="SOP-1", sop_title="t", use_tavily=False, retrieval="rag"
    )
    record = _tool_by_name(tool_list, "record_finding")
    garbage = "The" * 200
    result = record.invoke({
        "requirement_id": "HIPAA-164.312(a)",
        "requirement_title": "Access Control",
        "regulation": "HIPAA",
        "compliance_level": "gap",
        "severity": "high",
        "reasoning": "ok",
        "evidence_quote": garbage,
    })
    assert "runaway token repetition" in result.lower()
    assert "evidence_quote" in result
