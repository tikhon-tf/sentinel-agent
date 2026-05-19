"""Regression tests for list_sops tool guidance and SENTINEL system prompt.

These tests pin the user-facing text that tells the agent how list_sops actually
matches (literal lowercase substring, not semantic search). They guard against
the previous behavior where ambiguous "search and discover" / "matches against"
phrasing caused the agent to issue natural-language queries, get no matches,
and burn 10-27 wasted calls per audit before falling back to list_sops("").
"""
from __future__ import annotations

from sentinel.graph.agent import SENTINEL_SYSTEM_PROMPT
from sentinel.graph.tools import list_sops


def test_natural_language_query_returns_literal_substring_guidance():
    """A natural-language paraphrase must not return the old terse 'No SOPs found' message;
    it must explain that this is a literal substring filter and recommend list_sops()."""
    result = list_sops.invoke({"query": "SSDLC secure software development lifecycle"})

    # New guidance must be present
    assert "literal substring filter" in result.lower()
    assert "not semantic search" in result.lower()
    assert "list_sops()" in result

    # Old terse message must be gone
    assert not result.startswith("No SOPs found matching")


def test_natural_language_query_mentions_shorter_literal_token():
    """The no-match message should suggest retrying with a shorter literal token."""
    result = list_sops.invoke({"query": "change management segregation duties"})
    assert "literal token" in result.lower() or "shorter literal" in result.lower()


def test_system_prompt_does_not_use_old_ambiguous_phrasing():
    """The original 'search and discover SOPs by title, ID, or business unit' line
    caused the agent to treat list_sops as semantic search. It must be replaced."""
    assert "search and discover SOPs by title, ID, or business unit" not in SENTINEL_SYSTEM_PROMPT


def test_system_prompt_states_literal_substring_matching():
    """The system prompt must make clear that list_sops is literal substring matching."""
    assert "literal" in SENTINEL_SYSTEM_PROMPT.lower()
    assert "substring" in SENTINEL_SYSTEM_PROMPT.lower()
    assert "not semantic search" in SENTINEL_SYSTEM_PROMPT.lower()
