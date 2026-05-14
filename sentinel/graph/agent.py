"""Sentinel audit agent — LangGraph orchestration."""
from __future__ import annotations

from typing import Literal

from langgraph.graph import END, StateGraph

from sentinel.graph.nodes import (
    audit_clause,
    compile_results,
    decompose_query,
    ground_regulations,
    route_to_clauses,
)
from sentinel.graph.state import AuditState, ClauseAuditState


def build_graph():
    """Build the Sentinel audit LangGraph."""
    graph = StateGraph(AuditState)

    graph.add_node("decompose", decompose_query)
    graph.add_node("ground", ground_regulations)
    graph.add_node("audit_clause", audit_clause)
    graph.add_node("compile", compile_results)

    graph.set_entry_point("decompose")
    graph.add_edge("decompose", "ground")
    graph.add_conditional_edges("ground", route_to_clauses, ["audit_clause"])
    graph.add_edge("audit_clause", "compile")
    graph.add_edge("compile", END)

    return graph.compile()


def run_audit(
    query: str,
    mode: Literal["rag", "nexus", "local"] = "local",
) -> AuditState:
    """Run the full Sentinel audit and return the final state."""
    app = build_graph()

    initial_state: AuditState = {
        "query": query,
        "mode": mode,
        "clauses": [],
        "regulation_context": {},
        "findings": [],
        "cell_metrics": [],
        "status": "Starting audit...",
    }

    final_state = app.invoke(initial_state)
    return final_state
