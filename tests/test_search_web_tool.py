"""Tests that `search_web` does not leak Tavily's LLM-synthesized `answer` field."""
from __future__ import annotations

from unittest.mock import patch

import sentinel.graph.tools as tools_module
from sentinel.graph.tools import search_web


class _FakeTavilyClient:
    def __init__(self, *args, **kwargs):
        pass

    def search(self, **kwargs):
        assert kwargs.get("include_answer") is False
        return {
            "answer": "OCC Bulletin 2099-99 issued January 1, 2099 clarified all rules.",
            "results": [
                {
                    "title": "Real OCC page",
                    "url": "https://www.occ.gov/news/real",
                    "content": "Genuine page content snippet.",
                }
            ],
        }


def test_search_web_does_not_include_tavily_answer(monkeypatch):
    fake_tavily = type("M", (), {"TavilyClient": _FakeTavilyClient})
    monkeypatch.setitem(__import__("sys").modules, "tavily", fake_tavily)
    monkeypatch.setattr(tools_module, "TAVILY_API_KEY", "test-key")

    result = search_web.invoke({"query": "OCC AI bulletin 2025"})

    assert "OCC Bulletin 2099-99" not in result
    assert "January 1, 2099" not in result
    assert "Summary:" not in result
    assert "https://www.occ.gov/news/real" in result
    assert "Genuine page content snippet." in result
