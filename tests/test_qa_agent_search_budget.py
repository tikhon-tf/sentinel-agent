"""Regression: qa_agent must terminate with a real answer when search_web returns
overlapping generic summaries — not loop until recursion_limit and surface the
LangGraph "Sorry, need more steps to process this request." fallback.

Reproduces the recent-guidance failure mode by mocking search_web to return
three semantically-identical responses and asserts the agent stops within
5 search_web invocations and returns a substantive answer.
"""
from __future__ import annotations

from unittest.mock import patch

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from sentinel.eval import agentic_qa


class _FakeToolModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


_GENERIC_SUMMARY = "Summary: regulators emphasize compliance"


def _make_search_web():
    calls: list[str] = []

    @tool
    def search_web(query: str) -> str:
        """Tavily search."""
        calls.append(query)
        return _GENERIC_SUMMARY

    return search_web, calls


def test_qa_agent_stops_on_overlapping_generic_search_results():
    search_web, calls = _make_search_web()

    final_answer = (
        "I could not locate the specific Fed/OCC/FDIC guidance documents from the "
        "past 12 months. Available web summaries only state that regulators "
        "emphasize compliance.\n\nCompliance level: gap"
    )
    responses = [
        AIMessage(content="", tool_calls=[{"name": "search_web", "args": {"query": "fed guidance past 12 months"}, "id": "1"}]),
        AIMessage(content="", tool_calls=[{"name": "search_web", "args": {"query": "occ supervisory guidance recent"}, "id": "2"}]),
        AIMessage(content="", tool_calls=[{"name": "search_web", "args": {"query": "fdic guidance 2024"}, "id": "3"}]),
        AIMessage(content=final_answer),
    ]
    fake_model = _FakeToolModel(responses=responses)

    with patch.object(agentic_qa, "_build_subagent_model", return_value=fake_model), \
         patch.object(agentic_qa, "_build_subagent_tools", return_value=([search_web], [])):
        result = agentic_qa.agentic_qa_answer(
            question="Has the Fed/OCC/FDIC issued any supervisory guidance in the past 12 months?",
            sop_id=None,
            use_tavily=True,
            recursion_limit=30,
        )

    assert "need more steps" not in (result["answer"] or "").lower()
    assert "Compliance level:" in result["answer"]
    assert len(calls) <= 5
