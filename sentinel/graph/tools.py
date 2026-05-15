"""LangChain tools wrapping Sentinel's retrieval and auditing functions."""
from __future__ import annotations

import json
from typing import Literal

from langchain_core.tools import tool

from sentinel.grounding.tavily_search import ground_clause
from sentinel.llm import audit_cell
from sentinel.models import (
    ALL_CLAUSES,
    AuditFinding,
    ComplianceLevel,
    RegulationClause,
    Severity,
    SOPChunk,
)

_audit_results: dict = {"findings": [], "cell_metrics": []}
_retrieval_mode: str = "local"


def set_retrieval_mode(mode: str) -> None:
    _audit_results["mode"] = mode
    global _retrieval_mode
    _retrieval_mode = mode


def get_audit_results() -> dict:
    return _audit_results


def reset_audit_results() -> None:
    _audit_results["findings"] = []
    _audit_results["cell_metrics"] = []


@tool
def list_regulation_clauses() -> str:
    """List all regulation clauses that must be audited. Returns clause IDs, titles, and references for SOC 2 (CC1-CC9) and HIPAA Security Rule safeguards."""
    lines = []
    for c in ALL_CLAUSES:
        lines.append(f"- {c.clause_id}: {c.title} ({c.regulation}) — {c.reference}")
    return f"{len(ALL_CLAUSES)} clauses to audit:\n" + "\n".join(lines)


@tool
def retrieve_sops_for_clause(clause_id: str) -> str:
    """Retrieve relevant SOP documents for a given regulation clause ID (e.g. 'CC1', 'HIPAA-ADM-1'). Returns SOP chunks grouped by SOP ID."""
    clause = _find_clause(clause_id)
    if clause is None:
        return f"Unknown clause ID: {clause_id}"

    mode = _retrieval_mode
    if mode == "rag":
        from sentinel.retrieval.vector_search import retrieve_for_clause_rag
        sop_groups = retrieve_for_clause_rag(clause)
    elif mode == "nexus":
        from sentinel.retrieval.nexus import retrieve_for_clause_nexus
        sop_groups = retrieve_for_clause_nexus(clause)
    else:
        from sentinel.retrieval.local import retrieve_local
        sop_groups = retrieve_local(clause)

    if not sop_groups:
        return f"No SOPs found for {clause_id}: {clause.title}"

    parts = []
    for sop_id, chunks in sop_groups.items():
        sop_title = chunks[0].title if chunks else sop_id
        bu = chunks[0].business_unit if chunks else "N/A"
        chunk_texts = "\n---\n".join(
            f"[{c.section}] {c.chunk_text[:500]}" for c in chunks[:3]
        )
        parts.append(f"## {sop_id} — {sop_title} ({bu})\n{chunk_texts}")

    return f"Found {len(sop_groups)} SOPs for {clause_id}:\n\n" + "\n\n".join(parts)


@tool
def audit_single_clause(clause_id: str) -> str:
    """Run the full audit for one regulation clause: retrieve SOPs, assess compliance, and record findings. Use this for each clause that needs auditing."""
    clause = _find_clause(clause_id)
    if clause is None:
        return f"Unknown clause ID: {clause_id}"

    reg_context = ground_clause(clause)

    mode = _retrieval_mode
    if mode == "rag":
        from sentinel.retrieval.vector_search import retrieve_for_clause_rag
        sop_groups = retrieve_for_clause_rag(clause)
    elif mode == "nexus":
        from sentinel.retrieval.nexus import retrieve_for_clause_nexus
        sop_groups = retrieve_for_clause_nexus(clause)
    else:
        from sentinel.retrieval.local import retrieve_local
        sop_groups = retrieve_local(clause)

    if not sop_groups:
        finding = AuditFinding(
            clause_id=clause.clause_id,
            clause_title=clause.title,
            regulation=clause.regulation,
            sop_id="NONE",
            sop_title="No applicable SOP found",
            business_unit="N/A",
            compliance_level=ComplianceLevel.GAP,
            severity=Severity.CRITICAL,
            evidence_quote="",
            gap_description=f"No SOP found addressing {clause.title} ({clause.reference})",
            remediation=f"Create a dedicated SOP addressing {clause.reference}",
            reasoning="No relevant SOP content was retrieved for this regulation clause.",
        )
        _audit_results["findings"].append(finding)
        _audit_results["cell_metrics"].append({
            "clause_id": clause.clause_id,
            "sops_checked": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "latency": 0,
        })
        return f"{clause_id}: GAP (critical) — No applicable SOP found"

    results = []
    for sop_id, chunks in sop_groups.items():
        try:
            finding, cell_metrics = audit_cell(clause, chunks, reg_context)
        except Exception as e:
            finding = AuditFinding(
                clause_id=clause.clause_id,
                clause_title=clause.title,
                regulation=clause.regulation,
                sop_id=sop_id,
                sop_title=chunks[0].title if chunks else sop_id,
                business_unit=chunks[0].business_unit if chunks else "N/A",
                compliance_level=ComplianceLevel.GAP,
                severity=Severity.HIGH,
                evidence_quote="",
                gap_description=f"LLM assessment failed: {e}",
                remediation="Manual review required",
                reasoning="Automated assessment failed due to API error.",
            )
            cell_metrics = {"input_tokens": 0, "output_tokens": 0, "latency": 0}
        _audit_results["findings"].append(finding)
        _audit_results["cell_metrics"].append({
            "clause_id": clause.clause_id,
            "sop_id": sop_id,
            **cell_metrics,
        })
        results.append(
            f"  {sop_id}: {finding.compliance_level.value} ({finding.severity.value}) — {finding.gap_description or 'Compliant'}"
        )

    return f"{clause_id} ({clause.title}): audited {len(sop_groups)} SOPs\n" + "\n".join(results)


@tool
def audit_all_clauses() -> str:
    """Run the full audit across ALL regulation clauses at once. This audits all 25 clauses (9 SOC 2 + 16 HIPAA) against relevant SOPs. Use this when asked to perform a complete audit."""
    import concurrent.futures

    def _audit_one(clause: RegulationClause) -> str:
        reg_context = ground_clause(clause)
        mode = _retrieval_mode

        if mode == "rag":
            from sentinel.retrieval.vector_search import retrieve_for_clause_rag
            sop_groups = retrieve_for_clause_rag(clause)
        elif mode == "nexus":
            from sentinel.retrieval.nexus import retrieve_for_clause_nexus
            sop_groups = retrieve_for_clause_nexus(clause)
        else:
            from sentinel.retrieval.local import retrieve_local
            sop_groups = retrieve_local(clause)

        if not sop_groups:
            finding = AuditFinding(
                clause_id=clause.clause_id,
                clause_title=clause.title,
                regulation=clause.regulation,
                sop_id="NONE",
                sop_title="No applicable SOP found",
                business_unit="N/A",
                compliance_level=ComplianceLevel.GAP,
                severity=Severity.CRITICAL,
                evidence_quote="",
                gap_description=f"No SOP found addressing {clause.title} ({clause.reference})",
                remediation=f"Create a dedicated SOP addressing {clause.reference}",
                reasoning="No relevant SOP content was retrieved for this regulation clause.",
            )
            _audit_results["findings"].append(finding)
            _audit_results["cell_metrics"].append({
                "clause_id": clause.clause_id,
                "sops_checked": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": 0,
            })
            return f"{clause.clause_id}: GAP (critical) — No SOP found"

        clause_results = []
        for sop_id, chunks in sop_groups.items():
            try:
                finding, cell_metrics = audit_cell(clause, chunks, reg_context)
            except Exception as e:
                finding = AuditFinding(
                    clause_id=clause.clause_id,
                    clause_title=clause.title,
                    regulation=clause.regulation,
                    sop_id=sop_id,
                    sop_title=chunks[0].title if chunks else sop_id,
                    business_unit=chunks[0].business_unit if chunks else "N/A",
                    compliance_level=ComplianceLevel.GAP,
                    severity=Severity.HIGH,
                    evidence_quote="",
                    gap_description=f"LLM assessment failed: {e}",
                    remediation="Manual review required",
                    reasoning="Automated assessment failed due to API error.",
                )
                cell_metrics = {"input_tokens": 0, "output_tokens": 0, "latency": 0}
            _audit_results["findings"].append(finding)
            _audit_results["cell_metrics"].append({
                "clause_id": clause.clause_id,
                "sop_id": sop_id,
                **cell_metrics,
            })
            clause_results.append(f"{finding.compliance_level.value}")

        compliant = clause_results.count("compliant")
        partial = clause_results.count("partial")
        gap = clause_results.count("gap")
        return f"{clause.clause_id}: {len(sop_groups)} SOPs — {compliant}C/{partial}P/{gap}G"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_audit_one, c): c for c in ALL_CLAUSES}
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    findings = _audit_results["findings"]
    total = len(findings)
    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    summary = (
        f"Audit complete: {total} findings across {len(ALL_CLAUSES)} clauses\n"
        f"  Compliant: {compliant} ({100*compliant//max(total,1)}%)\n"
        f"  Partial:   {partial} ({100*partial//max(total,1)}%)\n"
        f"  Gap:       {gap} ({100*gap//max(total,1)}%)\n\n"
        "Per-clause breakdown:\n" + "\n".join(sorted(results))
    )
    return summary


def _find_clause(clause_id: str) -> RegulationClause | None:
    for c in ALL_CLAUSES:
        if c.clause_id == clause_id:
            return c
    return None
