"""Audit register — compile findings into structured output."""
from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path

from sentinel.models import AuditFinding, AuditMetrics, ComplianceLevel, Severity


def compute_metrics(findings: list[AuditFinding], cell_metrics: list[dict]) -> AuditMetrics:
    """Compute aggregate audit metrics from findings."""
    clause_ids = set(f.clause_id for f in findings)
    sop_ids = set(f.sop_id for f in findings if f.sop_id != "NONE")

    total_tokens = sum(m.get("input_tokens", 0) + m.get("output_tokens", 0) for m in cell_metrics)
    total_latency = sum(m.get("latency", 0) for m in cell_metrics)
    total_steps = sum(m.get("retrieval_steps", 0) for m in cell_metrics)

    return AuditMetrics(
        total_clauses=len(clause_ids),
        total_sops_audited=len(sop_ids),
        total_findings=len(findings),
        compliant_count=sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT),
        partial_count=sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL),
        gap_count=sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP),
        critical_count=sum(1 for f in findings if f.severity == Severity.CRITICAL),
        high_count=sum(1 for f in findings if f.severity == Severity.HIGH),
        medium_count=sum(1 for f in findings if f.severity == Severity.MEDIUM),
        low_count=sum(1 for f in findings if f.severity == Severity.LOW),
        total_tokens=total_tokens,
        total_retrieval_steps=total_steps,
        avg_latency_per_cell=total_latency / len(findings) if findings else 0,
        total_latency=total_latency,
        total_cost=total_tokens * 0.60 / 1_000_000,
    )


def findings_to_csv(findings: list[AuditFinding]) -> str:
    """Export findings as CSV."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Clause ID", "Clause Title", "Regulation", "SOP ID", "SOP Title",
        "Business Unit", "Compliance Level", "Severity", "Evidence Quote",
        "Gap Description", "Remediation", "Reasoning",
    ])
    for f in findings:
        writer.writerow([
            f.clause_id, f.clause_title, f.regulation, f.sop_id, f.sop_title,
            f.business_unit, f.compliance_level.value, f.severity.value,
            f.evidence_quote, f.gap_description, f.remediation, f.reasoning,
        ])
    return output.getvalue()


def findings_to_json(findings: list[AuditFinding]) -> str:
    """Export findings as JSON."""
    return json.dumps([f.model_dump() for f in findings], indent=2, default=str)


def save_register(
    findings: list[AuditFinding],
    cell_metrics: list[dict],
    output_dir: Path,
    prefix: str = "audit",
):
    """Save the full audit register: CSV, JSON, and metrics."""
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / f"{prefix}_register.csv"
    csv_path.write_text(findings_to_csv(findings), encoding="utf-8")

    json_path = output_dir / f"{prefix}_findings.json"
    json_path.write_text(findings_to_json(findings), encoding="utf-8")

    metrics = compute_metrics(findings, cell_metrics)
    metrics_path = output_dir / f"{prefix}_metrics.json"
    metrics_path.write_text(metrics.model_dump_json(indent=2), encoding="utf-8")

    return csv_path, json_path, metrics_path, metrics
