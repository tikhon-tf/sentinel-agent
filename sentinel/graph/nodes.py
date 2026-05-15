"""LangGraph node functions for the Sentinel audit agent."""
from __future__ import annotations

from langgraph.types import Send

from sentinel.graph.state import AuditState, ClauseAuditState
from sentinel.grounding.tavily_search import ground_all_clauses
from sentinel.llm import audit_cell
from sentinel.models import ALL_CLAUSES


def decompose_query(state: AuditState) -> dict:
    """Decompose the audit query into regulation clauses."""
    return {
        "clauses": ALL_CLAUSES,
        "status": f"Decomposed into {len(ALL_CLAUSES)} regulation clauses",
    }


def ground_regulations(state: AuditState) -> dict:
    """Fetch live regulation text for each clause via Tavily."""
    clauses = state["clauses"]
    contexts = ground_all_clauses(clauses)
    return {
        "regulation_context": contexts,
        "status": f"Grounded {len(contexts)} clauses with live regulation text",
    }


def route_to_clauses(state: AuditState) -> list[Send]:
    """Fan-out: dispatch one audit task per regulation clause."""
    clauses = state["clauses"]
    mode = state["mode"]
    reg_ctx = state.get("regulation_context", {})

    sends = []
    for clause in clauses:
        sends.append(
            Send(
                "audit_clause",
                ClauseAuditState(
                    clause=clause,
                    mode=mode,
                    regulation_context=reg_ctx.get(clause.clause_id, ""),
                    findings=[],
                    cell_metrics=[],
                ),
            )
        )
    return sends


def audit_clause(state: ClauseAuditState) -> dict:
    """Audit a single regulation clause against retrieved SOPs.

    NOTE: A full audit run (``run_audit``) already invokes this node once for
    every clause via ``route_to_clauses`` and accumulates every structured
    ``AuditFinding`` into ``AuditState['findings']``. Do NOT call this again
    per-clause after a full run has completed — the detailed findings are
    already in the returned state. Re-invoke this node only when re-running
    or focusing on a single clause.
    """
    clause = RegulationClause(**state["clause"]) if isinstance(state["clause"], dict) else state["clause"]
    mode = state["mode"]
    reg_context = state.get("regulation_context", "")

    if mode == "rag":
        from sentinel.retrieval.vector_search import retrieve_for_clause_rag
        sop_groups = retrieve_for_clause_rag(clause)
    elif mode == "nexus":
        from sentinel.retrieval.nexus import retrieve_for_clause_nexus
        sop_groups = retrieve_for_clause_nexus(clause)
    else:
        from sentinel.retrieval.local import retrieve_local
        sop_groups = retrieve_local(clause)

    findings = []
    metrics = []

    if not sop_groups:
        from sentinel.models import AuditFinding, ComplianceLevel, Severity
        findings.append(AuditFinding(
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
        ))
        metrics.append({"clause_id": clause.clause_id, "sops_checked": 0, "input_tokens": 0, "output_tokens": 0, "latency": 0})
        return {"findings": findings, "cell_metrics": metrics}

    for sop_id, chunks in sop_groups.items():
        finding, cell_metrics = audit_cell(clause, chunks, reg_context)
        findings.append(finding)
        metrics.append({
            "clause_id": clause.clause_id,
            "sop_id": sop_id,
            **cell_metrics,
        })

    return {"findings": findings, "cell_metrics": metrics}


def compile_results(state: AuditState) -> dict:
    """Compile all findings into the final audit state.

    Returns the complete list of structured per-clause ``AuditFinding`` objects
    alongside the aggregate status string. A single ``run_audit`` call
    produces the full audit — callers should NOT iterate ``audit_clause`` per
    clause after this node runs to "recover" details; those details are
    already present in ``findings`` and ``cell_metrics``.
    """
    findings = state.get("findings", [])
    clauses = state.get("clauses", [])
    return {
        "status": (
            f"Audit complete: {len(findings)} findings across {len(clauses)} clauses. "
            f"All per-clause findings are available in state['findings']; "
            f"no further per-clause audits are needed."
        ),
    }
