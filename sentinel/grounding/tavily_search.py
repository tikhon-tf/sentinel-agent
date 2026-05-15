"""Tavily live regulation grounding — fetches the freshest regulation text and enforcement actions."""
from __future__ import annotations

from sentinel.config import TAVILY_API_KEY
from sentinel.models import RegulationClause


_client = None


def get_client():
    global _client
    if _client is None:
        from tavily import TavilyClient
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client


def ground_clause(clause: RegulationClause) -> str:
    """Fetch the latest regulation guidance and enforcement context for a clause."""
    if not TAVILY_API_KEY:
        return ""

    client = get_client()

    if clause.regulation == "SOC 2":
        query = (
            f"AICPA SOC 2 Trust Services Criteria {clause.clause_id} "
            f"{clause.title} latest guidance implementation requirements 2025 2026"
        )
    else:
        query = (
            f"HIPAA Security Rule {clause.reference} {clause.title} "
            f"HHS OCR guidance enforcement 2025 2026"
        )

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,
        )
    except Exception:
        return ""

    parts = []
    if response.get("answer"):
        parts.append(f"Summary: {response['answer']}")

    for result in response.get("results", [])[:3]:
        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")[:500]
        parts.append(f"Source: {title}\nURL: {url}\n{content}")

    return "\n\n".join(parts)


def ground_all_clauses(clauses: list[RegulationClause]) -> dict[str, str]:
    """Ground all clauses with live regulation context. Returns {clause_id: context}."""
    if not TAVILY_API_KEY:
        return {}

    contexts = {}
    for clause in clauses:
        ctx = ground_clause(clause)
        if ctx:
            contexts[clause.clause_id] = ctx

    return contexts
