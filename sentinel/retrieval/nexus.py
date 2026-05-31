"""Nexus KnowQL client for regulation retrieval (Act 2)."""
from __future__ import annotations

import logging
import threading
import time

logger = logging.getLogger(__name__)

MAX_RETRIES = 4

_token: str | None = None
_token_lock = threading.Lock()


def _login() -> str:
    import httpx
    from sentinel.config import NEXUS_API_KEY, NEXUS_BASE_URL

    resp = httpx.post(
        f"{NEXUS_BASE_URL}/api/v0/auth/login",
        json={"api_key": NEXUS_API_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def _get_token() -> str:
    global _token
    with _token_lock:
        if _token is None:
            _token = _login()
    return _token


def _reset_token() -> None:
    global _token
    with _token_lock:
        _token = None


def query_nexus(ask: str, ground: bool = True) -> dict:
    """Query Nexus KnowQL and return the response dict.

    Handles 401 (re-auth), 429 (rate limit), and 409 (context unavailable)
    with retries.
    """
    import httpx
    from sentinel.config import NEXUS_BASE_URL, NEXUS_CONTEXT_SLUG

    token = _get_token()
    payload = {
        "scope": [NEXUS_CONTEXT_SLUG],
        "ask": ask,
        "ground": ground,
    }

    for attempt in range(MAX_RETRIES + 1):
        resp = httpx.post(
            f"{NEXUS_BASE_URL}/knowql",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
            timeout=60,
        )

        if resp.status_code == 401:
            _reset_token()
            token = _get_token()
            continue

        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after_seconds") or int(resp.headers.get("Retry-After", 5))
            logger.warning("Nexus 429 rate-limited, retrying in %ds (attempt %d/%d)", retry_after, attempt + 1, MAX_RETRIES)
            time.sleep(retry_after)
            continue

        if resp.status_code == 409:
            backoff = 2 ** attempt
            logger.warning("Nexus 409 context unavailable, retrying in %ds (attempt %d/%d)", backoff, attempt + 1, MAX_RETRIES)
            time.sleep(backoff)
            continue

        if resp.status_code in (502, 503, 504):
            backoff = 2 ** attempt
            logger.warning("Nexus %d server error, retrying in %ds (attempt %d/%d)", resp.status_code, backoff, attempt + 1, MAX_RETRIES)
            time.sleep(backoff)
            continue

        resp.raise_for_status()
        return resp.json()

    resp.raise_for_status()
    return resp.json()


def format_nexus_response(data: dict) -> str:
    """Format a Nexus KnowQL response into text for the LLM."""
    output = data.get("output", {})
    answer = output.get("answer", "")
    citations = output.get("citations", [])

    parts: list[str] = []

    if isinstance(answer, list):
        for item in answer:
            if isinstance(item, dict):
                for k, v in item.items():
                    parts.append(f"{k}: {v}")
                parts.append("")
            else:
                parts.append(str(item))
    elif isinstance(answer, dict):
        if "raw" in answer:
            parts.append(answer["raw"])
        else:
            for k, v in answer.items():
                parts.append(f"{k}: {v}")
    else:
        parts.append(str(answer))

    if citations:
        parts.append("\nCited sources:")
        for i, c in enumerate(citations, 1):
            fname = c.get("file", {}).get("name", "unknown")
            parts.append(f"  [c{i}] {fname}")

    return "\n".join(parts)
