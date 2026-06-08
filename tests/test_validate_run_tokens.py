"""Token aggregation in validate_run.

Regression for the discrepancy where validate_run reported only the FIRST
audit call's tokens (re.search → first match), while the UI reported only the
LAST. Sub-agent tokens must be summed across every audit tool output in a run.
"""
from __future__ import annotations

from scripts.validate_run import _sub_agent_tokens, parse_run_stats

# A realistic audit_sops output: one aggregate "Total tokens:" line that already
# covers its sub-agents, plus per-SOP "Sub-agent tokens:" lines that must NOT be
# counted on top of the aggregate.
AUDIT_SOPS_15 = (
    "Audit complete: 15 SOPs\n"
    "  Total tokens: 18,970,972 (18,796,249 in / 174,723 out)\n"
    "  Failed: 0\n\n"
    "Per-SOP breakdown:\n"
    "SOP-CLIN-001 (Clinical Validation): 3 findings — 1C/1P/1G\n"
    "Sub-agent tokens: 1,200,000 (1,180,000 in / 20,000 out)\n"
    "SOP-CLIN-002 (Model Monitoring): 2 findings — 2C/0P/0G\n"
    "Sub-agent tokens: 1,000,000 (980,000 in / 20,000 out)\n"
)
AUDIT_SOPS_5 = (
    "Audit complete: 5 SOPs\n"
    "  Total tokens: 7,150,445 (7,086,885 in / 63,560 out)\n"
    "Per-SOP breakdown:\n"
    "SOP-CLIN-010 (Change Control): 4 findings — 2C/1P/1G\n"
    "Sub-agent tokens: 1,400,000 (1,380,000 in / 20,000 out)\n"
)
# An individual audit_single_sop output has NO aggregate line.
AUDIT_SINGLE = (
    "SOP-ISEC-008 (MFA): 5 findings — 2C/2P/1G\n"
    "Sub-agent tokens: 500,000 (450,000 in / 50,000 out)"
)


def test_single_audit_sops_counts_aggregate_not_per_sop():
    """Within one audit_sops output, count the Total aggregate, not the per-SOP lines."""
    assert _sub_agent_tokens([AUDIT_SOPS_15]) == (18_796_249, 174_723)


def test_multiple_audit_sops_calls_are_summed():
    """The reported bug: two audit_sops calls must sum, not keep only one of them."""
    assert _sub_agent_tokens([AUDIT_SOPS_15, AUDIT_SOPS_5]) == (
        18_796_249 + 7_086_885,
        174_723 + 63_560,
    )


def test_individual_audit_single_sop_counts_per_sop_line():
    """An audit_single_sop output has no Total line, so count its Sub-agent line."""
    assert _sub_agent_tokens([AUDIT_SINGLE]) == (450_000, 50_000)


def test_mixed_audit_calls_summed():
    """audit_sops (aggregate) + audit_single_sop (per-SOP) summed without double-count."""
    assert _sub_agent_tokens([AUDIT_SOPS_5, AUDIT_SINGLE]) == (
        7_086_885 + 450_000,
        63_560 + 50_000,
    )


def test_empty_inputs():
    assert _sub_agent_tokens([]) == (0, 0)
    assert _sub_agent_tokens(["", "no token lines here"]) == (0, 0)


def test_parse_run_stats_sums_outer_and_all_audit_calls():
    """End-to-end: outer trace tokens + summed sub-agent tokens across all calls.

    Mirrors the real run (019ea71b…): outer 259,922 + audit #1 18.97M +
    audit #2 7.15M ≈ 26.4M — the figure neither tool reported before the fix.
    """
    run_data = {
        "trace_input_tokens": 249_815,
        "trace_output_tokens": 10_107,
        "audit_outputs": [AUDIT_SOPS_15, AUDIT_SOPS_5],
        "model": "nvidia/Nemotron-3-Ultra-550b-a55b",
    }
    stats = parse_run_stats(None, run_data)

    assert stats["input_tokens"] == 249_815 + 18_796_249 + 7_086_885
    assert stats["output_tokens"] == 10_107 + 174_723 + 63_560
    assert stats["sub_tokens"] == (18_796_249 + 174_723) + (7_086_885 + 63_560)
    assert stats["outer_tokens"] == 249_815 + 10_107

    expected_cost = (stats["input_tokens"] / 1e6) * 1.00 + (stats["output_tokens"] / 1e6) * 3.00
    assert abs(stats["cost"] - expected_cost) < 1e-6


def test_parse_run_stats_falls_back_to_content():
    """When audit_outputs is absent, fall back to the combined content string."""
    run_data = {"trace_input_tokens": 0, "trace_output_tokens": 0, "model": "x"}
    stats = parse_run_stats(AUDIT_SINGLE, run_data)
    assert stats["input_tokens"] == 450_000
    assert stats["output_tokens"] == 50_000
