from __future__ import annotations

from openai import OpenAI

from sentinel.config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    MODEL,
    NEBIUS_API_KEY,
    NEBIUS_BASE_URL,
)


_clients: dict[str, OpenAI] = {}
_provider: str = "nebius"


def set_provider(provider: str) -> None:
    global _provider
    _provider = provider


def get_client() -> OpenAI:
    if _provider not in _clients:
        if _provider == "anthropic":
            _clients[_provider] = OpenAI(
                base_url="https://api.anthropic.com/v1/",
                api_key=ANTHROPIC_API_KEY,
            )
        else:
            _clients[_provider] = OpenAI(
                base_url=NEBIUS_BASE_URL,
                api_key=NEBIUS_API_KEY,
            )
    return _clients[_provider]


def get_model() -> str:
    return ANTHROPIC_MODEL if _provider == "anthropic" else MODEL
