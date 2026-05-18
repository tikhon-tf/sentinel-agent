"""Regression tests for audit register: metrics, CSV, and JSON output."""
from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path

import pytest

from sentinel.models import AuditFinding, AuditMetrics, ComplianceLevel, Severity
from sentinel.output.register import compute_metrics, findings_to_csv, findings_to_json, save_register


class TestComputeMetrics:
    def test_counts(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        assert m.total_findings == 3
        assert m.compliant_count == 1
        assert m.partial_count == 1
        assert m.gap_count == 1

    def test_severity_counts(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        assert m.high_count == 1
        assert m.medium_count == 1
        assert m.low_count == 0
        assert m.critical_count == 0

    def test_token_aggregation(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        expected_tokens = (500 + 200) + (600 + 300) + (400 + 150)
        assert m.total_tokens == expected_tokens

    def test_latency_aggregation(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        assert m.total_latency == pytest.approx(7.4)
        assert m.avg_latency_per_cell == pytest.approx(7.4 / 3)

    def test_retrieval_steps(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        assert m.total_retrieval_steps == 6

    def test_unique_clause_and_sop_ids(self, mixed_findings, sample_cell_metrics):
        m = compute_metrics(mixed_findings, sample_cell_metrics)
        assert m.total_clauses == 3
        assert m.total_sops_audited == 3

    def test_empty_findings(self):
        m = compute_metrics([], [])
        assert m.total_findings == 0
        assert m.avg_latency_per_cell == 0.0
        assert m.total_tokens == 0

    def test_duplicate_clause_ids(self, compliant_finding, sample_cell_metrics):
        findings = [compliant_finding, compliant_finding]
        m = compute_metrics(findings, sample_cell_metrics)
        assert m.total_clauses == 1
        assert m.total_findings == 2

    def test_sop_id_none_excluded(self, compliant_finding, sample_cell_metrics):
        f = compliant_finding.model_copy(update={"sop_id": "NONE"})
        m = compute_metrics([f], sample_cell_metrics)
        assert m.total_sops_audited == 0


class TestFindingsToCSV:
    def test_header_row(self, mixed_findings):
        csv_str = findings_to_csv(mixed_findings)
        reader = csv.reader(StringIO(csv_str))
        header = next(reader)
        assert "Clause ID" in header
        assert "Compliance Level" in header
        assert "Severity" in header
        assert len(header) == 12

    def test_row_count(self, mixed_findings):
        csv_str = findings_to_csv(mixed_findings)
        reader = csv.reader(StringIO(csv_str))
        rows = list(reader)
        assert len(rows) == 4  # 1 header + 3 findings

    def test_enum_values_serialized(self, gap_finding):
        csv_str = findings_to_csv([gap_finding])
        assert "gap" in csv_str
        assert "high" in csv_str

    def test_empty_findings(self):
        csv_str = findings_to_csv([])
        reader = csv.reader(StringIO(csv_str))
        rows = list(reader)
        assert len(rows) == 1  # header only

    def test_commas_in_evidence_escaped(self):
        f = AuditFinding(
            clause_id="X", clause_title="X", regulation="X",
            sop_id="X", sop_title="X", business_unit="X",
            compliance_level=ComplianceLevel.GAP, severity=Severity.HIGH,
            evidence_quote='The policy states "access is granted, reviewed, and revoked."',
        )
        csv_str = findings_to_csv([f])
        reader = csv.reader(StringIO(csv_str))
        rows = list(reader)
        assert len(rows) == 2
        assert "access is granted, reviewed, and revoked." in rows[1][8]


class TestFindingsToJSON:
    def test_valid_json(self, mixed_findings):
        json_str = findings_to_json(mixed_findings)
        data = json.loads(json_str)
        assert isinstance(data, list)
        assert len(data) == 3

    def test_fields_present(self, gap_finding):
        json_str = findings_to_json([gap_finding])
        data = json.loads(json_str)
        item = data[0]
        assert item["clause_id"] == "HIPAA-TECH-2"
        assert item["compliance_level"] == "gap"
        assert item["severity"] == "high"

    def test_empty_findings(self):
        json_str = findings_to_json([])
        assert json.loads(json_str) == []


class TestSaveRegister:
    def test_creates_files(self, mixed_findings, sample_cell_metrics, tmp_path):
        csv_path, json_path, metrics_path, metrics = save_register(
            mixed_findings, sample_cell_metrics, tmp_path, prefix="test"
        )
        assert csv_path.exists()
        assert json_path.exists()
        assert metrics_path.exists()
        assert csv_path.name == "test_register.csv"
        assert json_path.name == "test_findings.json"
        assert metrics_path.name == "test_metrics.json"

    def test_metrics_file_valid_json(self, mixed_findings, sample_cell_metrics, tmp_path):
        _, _, metrics_path, _ = save_register(
            mixed_findings, sample_cell_metrics, tmp_path
        )
        data = json.loads(metrics_path.read_text())
        assert data["total_findings"] == 3

    def test_creates_output_dir(self, mixed_findings, sample_cell_metrics, tmp_path):
        nested = tmp_path / "deep" / "nested"
        save_register(mixed_findings, sample_cell_metrics, nested)
        assert nested.exists()
