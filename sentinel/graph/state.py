"""LangGraph state definition for the Sentinel audit agent."""
from __future__ import annotations

import operator
from typing import Annotated, Literal

from typing_extensions import TypedDict

from sentinel.models import AuditFinding, AuditMetrics, RegulationClause


class AuditState(TypedDict):
    query: str
    mode: Literal["rag", "nexus", "local"]
    clauses: list[RegulationClause]
    regulation_context: dict[str, str]
    findings: Annotated[list[AuditFinding], operator.add]
    cell_metrics: Annotated[list[dict], operator.add]
    status: str


class ClauseAuditState(TypedDict):
    clause: RegulationClause
    mode: Literal["rag", "nexus", "local"]
    regulation_context: str
    findings: Annotated[list[AuditFinding], operator.add]
    cell_metrics: Annotated[list[dict], operator.add]
