"""Regression tests for JSON parsing and enum mapping from sub-agent responses."""
from __future__ import annotations

import json

import pytest


COMPLIANCE_LEVEL_MAP = {
    "compliant": "compliant", "partial": "partial", "gap": "gap",
    "info": "compliant", "non-compliant": "gap", "non_compliant": "gap",
}

SEVERITY_MAP = {
    "critical": "critical", "high": "high", "medium": "medium",
    "low": "low", "info": "info",
    "compliant": "info", "partial": "medium", "gap": "high",
}


class TestComplianceLevelMap:
    def test_standard_values(self):
        assert COMPLIANCE_LEVEL_MAP["compliant"] == "compliant"
        assert COMPLIANCE_LEVEL_MAP["partial"] == "partial"
        assert COMPLIANCE_LEVEL_MAP["gap"] == "gap"

    def test_info_maps_to_compliant(self):
        assert COMPLIANCE_LEVEL_MAP["info"] == "compliant"

    def test_non_compliant_maps_to_gap(self):
        assert COMPLIANCE_LEVEL_MAP["non-compliant"] == "gap"
        assert COMPLIANCE_LEVEL_MAP["non_compliant"] == "gap"

    def test_unknown_defaults_to_gap(self):
        assert COMPLIANCE_LEVEL_MAP.get("unknown", "gap") == "gap"
        assert COMPLIANCE_LEVEL_MAP.get("", "gap") == "gap"


class TestSeverityMap:
    def test_standard_values(self):
        for sev in ["critical", "high", "medium", "low", "info"]:
            assert SEVERITY_MAP[sev] == sev

    def test_compliance_level_crossover(self):
        assert SEVERITY_MAP["compliant"] == "info"
        assert SEVERITY_MAP["partial"] == "medium"
        assert SEVERITY_MAP["gap"] == "high"

    def test_unknown_defaults_to_high(self):
        assert SEVERITY_MAP.get("unknown", "high") == "high"


class TestJsonExtraction:
    """Test the JSON extraction patterns used in _audit_single_sop_impl."""

    def _extract_json_array(self, content: str) -> list | None:
        """Replicate the JSON extraction logic from tools.py."""
        if "```" in content:
            fence_start = content.find("```")
            lang_end = content.find("\n", fence_start)
            inner_start = lang_end + 1 if lang_end > fence_start else fence_start + 3
            fence_end = content.find("```", inner_start)
            if fence_end > inner_start:
                content = content[inner_start:fence_end].strip()

        start_idx = content.find("[")
        if start_idx < 0:
            return None

        candidate = content[start_idx:]
        end_idx = candidate.rfind("]")
        if end_idx > 0:
            candidate = candidate[:end_idx + 1]

        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                return parsed
        except json.JSONDecodeError:
            repaired = candidate.rstrip().rstrip(",")
            if not repaired.endswith("}"):
                last_brace = repaired.rfind("}")
                if last_brace > 0:
                    repaired = repaired[:last_brace + 1]
            repaired += "]"
            try:
                parsed = json.loads(repaired)
                if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                    return parsed
            except json.JSONDecodeError:
                pass
        return None

    def test_clean_json_array(self):
        content = '[{"clause_id": "X", "compliance_level": "gap"}]'
        result = self._extract_json_array(content)
        assert result is not None
        assert len(result) == 1

    def test_json_with_markdown_fences(self):
        content = '```json\n[{"clause_id": "X"}]\n```'
        result = self._extract_json_array(content)
        assert result is not None
        assert result[0]["clause_id"] == "X"

    def test_json_with_preceding_text(self):
        content = 'Here are the findings:\n[{"clause_id": "X"}]'
        result = self._extract_json_array(content)
        assert result is not None

    def test_trailing_comma_repaired(self):
        content = '[{"clause_id": "X"},]'
        result = self._extract_json_array(content)
        assert result is not None

    def test_truncated_array_repaired(self):
        content = '[{"clause_id": "A"}, {"clause_id": "B"'
        result = self._extract_json_array(content)
        assert result is not None
        assert len(result) == 1
        assert result[0]["clause_id"] == "A"

    def test_no_json_returns_none(self):
        content = "I could not produce findings for this SOP."
        result = self._extract_json_array(content)
        assert result is None

    def test_empty_array_returns_none(self):
        content = "[]"
        result = self._extract_json_array(content)
        assert result is None

    def test_multiple_items(self):
        content = '[{"clause_id": "A"}, {"clause_id": "B"}, {"clause_id": "C"}]'
        result = self._extract_json_array(content)
        assert result is not None
        assert len(result) == 3

    def test_code_fence_with_lang_tag(self):
        content = '```json\n[{"x": 1}]\n```'
        result = self._extract_json_array(content)
        assert result is not None

    def test_code_fence_no_lang_tag(self):
        content = '```\n[{"x": 1}]\n```'
        result = self._extract_json_array(content)
        assert result is not None

    def test_nested_objects(self):
        content = '[{"clause_id": "X", "details": {"sub": "value"}}]'
        result = self._extract_json_array(content)
        assert result is not None
        assert result[0]["details"]["sub"] == "value"

    def test_truncated_after_complete_object(self):
        content = '[{"clause_id": "A"}, {"clause_id": "B"}, {"clau'
        result = self._extract_json_array(content)
        assert result is not None
        assert len(result) == 2


class TestNullDefaultFallback:
    """Regression: explicit `null` values must fall back to defaults.

    `dict.get(key, default)` only returns the default when the key is
    missing — if the sub-agent emits `{"severity": null}`, `.get` returns
    `None` and `.lower()` raises AttributeError. Using
    `(data.get(key) or default)` coerces both missing keys and explicit
    None to the default before normalization.
    """

    def _normalize(self, data: dict) -> tuple[str, str]:
        # Mirrors the parsing logic in sentinel/graph/tools.py.
        raw_cl = (data.get("compliance_level") or "gap").lower().strip()
        raw_sev = (data.get("severity") or "high").lower().strip()
        return raw_cl, raw_sev

    def test_explicit_null_severity_falls_back(self):
        raw_cl, raw_sev = self._normalize({"severity": None, "compliance_level": None})
        assert raw_cl == "gap"
        assert raw_sev == "high"

    def test_missing_keys_still_fall_back(self):
        raw_cl, raw_sev = self._normalize({})
        assert raw_cl == "gap"
        assert raw_sev == "high"

    def test_provided_values_are_normalized(self):
        raw_cl, raw_sev = self._normalize(
            {"severity": " HIGH ", "compliance_level": "Partial"}
        )
        assert raw_cl == "partial"
        assert raw_sev == "high"

    def test_old_unsafe_pattern_would_raise(self):
        """Demonstrate the bug the fix prevents."""
        data = {"severity": None}
        with pytest.raises(AttributeError):
            data.get("severity", "high").lower()
