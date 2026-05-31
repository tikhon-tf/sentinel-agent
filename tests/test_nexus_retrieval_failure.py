"""Regression tests for Nexus retrieval failure handling (issue 3d33c754)."""
from __future__ import annotations

import httpx
import pytest


def _make_502_response() -> httpx.Response:
    request = httpx.Request("POST", "https://prod.nexus.pinecone.io/knowql")
    return httpx.Response(status_code=502, request=request, text="Bad Gateway")


def test_retrieve_regulation_text_returns_structured_error_on_502(monkeypatch):
    """_retrieve_regulation_text must emit RETRIEVAL_ERROR: envelope on 502 — never the chatty 'Nexus retrieval failed:' string."""
    from sentinel.graph import tools as tools_module
    from sentinel.retrieval import nexus as nexus_module

    monkeypatch.setattr(tools_module, "NEXUS_API_KEY", "fake-key-for-test")

    def _raise_502(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "Server error '502 Bad Gateway' for url 'https://prod.nexus.pinecone.io/knowql'",
            request=httpx.Request("POST", "https://prod.nexus.pinecone.io/knowql"),
            response=_make_502_response(),
        )

    monkeypatch.setattr(nexus_module, "query_nexus", _raise_502)

    built = tools_module.build_tools(provider="nebius", use_tavily=False, retrieval="nexus")
    retrieve_tool = next(t for t in built if t.name == "retrieve_regulation_text_tool")

    result = retrieve_tool.invoke({"query": "What does SOC 2 CC6.1 require?"})

    assert isinstance(result, str)
    assert result.startswith("RETRIEVAL_ERROR:"), f"expected RETRIEVAL_ERROR envelope, got: {result!r}"
    assert not result.startswith("Nexus retrieval failed:"), (
        f"old chatty error string leaked through: {result!r}"
    )
    assert "Do NOT cite" in result


def test_query_nexus_retries_502_until_exhaustion(monkeypatch):
    """query_nexus must retry 502s and only raise after exhausting MAX_RETRIES."""
    from sentinel.retrieval import nexus as nexus_module

    monkeypatch.setattr(nexus_module, "_get_token", lambda: "fake-token")
    monkeypatch.setattr(nexus_module.time, "sleep", lambda _s: None)

    call_count = {"n": 0}

    def _always_502(url, headers=None, json=None, timeout=None):
        call_count["n"] += 1
        return _make_502_response()

    import httpx as _httpx_module
    monkeypatch.setattr(_httpx_module, "post", _always_502)

    with pytest.raises(httpx.HTTPStatusError):
        nexus_module.query_nexus("test query")

    assert call_count["n"] >= nexus_module.MAX_RETRIES, (
        f"expected at least {nexus_module.MAX_RETRIES} attempts before raising, got {call_count['n']}"
    )
