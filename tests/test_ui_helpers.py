"""Regression tests for Streamlit UI helper functions."""
from __future__ import annotations

import pytest


class TestFormatUsage:
    def _format(self, *args, **kwargs):
        from ui.app import _format_usage
        return _format_usage(*args, **kwargs)

    def test_basic_format(self):
        result = self._format(1000, 500, "deepseek-ai/DeepSeek-V4-Pro")
        assert "1,500" in result
        assert "1,000 in" in result
        assert "500 out" in result
        assert "$" in result

    def test_deepseek_pricing(self):
        result = self._format(1_000_000, 1_000_000, "deepseek-ai/DeepSeek-V4-Pro")
        assert "$5.2500" in result  # 1M * $1.75 + 1M * $3.50

    def test_openai_pricing(self):
        result = self._format(1_000_000, 1_000_000, "gpt-5.5")
        assert "$35.0000" in result  # 1M * $5.00 + 1M * $30.00

    def test_unknown_model_uses_default(self):
        result = self._format(1_000_000, 1_000_000, "unknown-model")
        assert "$5.2500" in result  # default pricing: $1.75 + $3.50

    def test_zero_tokens(self):
        result = self._format(0, 0)
        assert "0" in result
        assert "$0.0000" in result

    def test_latency_included(self):
        result = self._format(100, 50, latency=3.7)
        assert "Latency: 3.7s" in result

    def test_latency_zero_excluded(self):
        result = self._format(100, 50, latency=0.0)
        assert "Latency" not in result


class TestParseSubagentUsage:
    def _parse(self, *args, **kwargs):
        from ui.app import _parse_subagent_usage
        return _parse_subagent_usage(*args, **kwargs)

    def test_standard_format(self):
        text = "SOP-001: 5 findings (3C/1P/1G). Sub-agent tokens: 12,500 (8,000 in / 4,500 out)"
        in_tok, out_tok = self._parse(text)
        assert in_tok == 8000
        assert out_tok == 4500

    def test_no_match(self):
        assert self._parse("No token info here") == (0, 0)

    def test_large_numbers(self):
        text = "Sub-agent tokens: 1,234,567 (1,000,000 in / 234,567 out)"
        in_tok, out_tok = self._parse(text)
        assert in_tok == 1_000_000
        assert out_tok == 234_567


class TestParseAuditTable:
    def _parse(self, *args, **kwargs):
        from ui.app import _parse_audit_table
        return _parse_audit_table(*args, **kwargs)

    def test_no_audit_marker(self):
        assert self._parse("some random text") is None

    def test_with_audit_complete_but_no_findings(self):
        result = self._parse("Audit complete: 0 findings")
        assert result is None or result == []

    def test_valid_audit_output(self):
        text = (
            "Audit complete: 3 findings\n"
            "SOP-001: 2 findings (1C/0P/1G) 1C/0P/1G\n"
            "SOP-002: 1 findings (0C/1P/0G) 0C/1P/0G\n"
        )
        result = self._parse(text)
        assert result is not None
        assert len(result) == 2
        assert result[0]["sop"] == "SOP-001"
        assert result[0]["gap"] == 1
        assert result[1]["partial"] == 1


class TestFormatToolStatus:
    def _format(self, *args, **kwargs):
        from ui.app import _format_tool_status
        return _format_tool_status(*args, **kwargs)

    def test_known_tool(self):
        result = self._format({"name": "list_sops", "args": {}})
        assert "Searching SOPs" in result

    def test_unknown_tool(self):
        result = self._format({"name": "some_new_tool", "args": {}})
        assert "some_new_tool" in result

    def test_missing_name(self):
        result = self._format({"name": "", "args": {}})
        assert isinstance(result, str)
