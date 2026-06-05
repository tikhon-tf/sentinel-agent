"""Tests for the audit retry classifier."""
from __future__ import annotations

from sentinel.graph.tools import _is_transient


def test_transient_rate_limit_is_retried():
    assert _is_transient("Nebius 429 rate-limited") is True


def test_transient_connection_error_is_retried():
    assert _is_transient("httpx.ConnectError: connection reset by peer") is True


def test_transient_timeout_is_retried():
    assert _is_transient("Read timeout while contacting provider") is True


def test_truncation_is_not_retried():
    assert _is_transient(
        "SOP-AIML-009 FAILED — sub-agent did not produce structured findings "
        "(finish_reason=length, truncated at output cap)"
    ) is False


def test_recursion_limit_is_not_retried():
    assert _is_transient(
        "SOP-ISEC-008 FAILED — GraphRecursionError: recursion limit of 50 reached"
    ) is False


def test_parse_failure_is_not_retried():
    assert _is_transient(
        "SOP-RISK-002 FAILED — failed to parse sub-agent findings: invalid JSON"
    ) is False
