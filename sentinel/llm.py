from __future__ import annotations

import json
import time

from openai import OpenAI

from sentinel.config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    MODEL,
    MODEL_MAX_TOKENS,
    NEBIUS_API_KEY,
    NEBIUS_BASE_URL,
)
from sentinel.models import AuditFinding, ComplianceLevel, Severity, SOPChunk, RegulationClause


_clients: dict[str, OpenAI] = {}
_provider: str = "nebius"


def set_provider(provider: str) -> None:
    global _provider
    _provider = provider


def get_client() -> OpenAI:
    if _provider not in _clients:
        if _provider == "anthropic":
            _clients[_provider] = OpenAI(
                base_url="https://api.anthropic.com/v1/",
                api_key=ANTHROPIC_API_KEY,
            )
        else:
            _clients[_provider] = OpenAI(
                base_url=NEBIUS_BASE_URL,
                api_key=NEBIUS_API_KEY,
            )
    return _clients[_provider]


def get_model() -> str:
    return ANTHROPIC_MODEL if _provider == "anthropic" else MODEL


def audit_cell(
    clause: RegulationClause,
    sop_chunks: list[SOPChunk],
    regulation_context: str = "",
) -> tuple[AuditFinding, dict]:
    """Run the per-cell reasoner: given a regulation clause and SOP evidence, produce a finding."""
    sop = sop_chunks[0] if sop_chunks else None
    sop_text = "\n\n---\n\n".join(
        f"[{c.section}]\n{c.chunk_text}" for c in sop_chunks
    )

    system_prompt = """You are Sentinel, an expert regulatory compliance auditor for Meridian Health Technologies.
You assess enterprise SOPs against specific regulation clauses. You are thorough, precise, and cite evidence directly.

For each assessment, you MUST return valid JSON with these fields:
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP text that supports your finding (or empty string if no relevant text)
- gap_description: what is missing or insufficient (empty string if compliant)
- remediation: specific recommended action to close the gap (empty string if compliant)
- reasoning: 2-3 sentence explanation of your assessment

Severity guide:
- critical: complete absence of required control for a high-risk area
- high: significant gap that could lead to regulatory finding
- medium: partial coverage with notable weaknesses
- low: minor documentation or process improvement needed
- info: compliant, no action needed"""

    user_prompt = f"""Assess the following SOP against the regulation clause below.

## Regulation Clause
**{clause.clause_id}: {clause.title}**
{clause.description}
Reference: {clause.reference}

{f"## Latest Regulation Guidance{chr(10)}{regulation_context}{chr(10)}" if regulation_context else ""}
## SOP Evidence
SOP: {sop.sop_id if sop else "N/A"} — {sop.title if sop else "No SOP found"}
Business Unit: {sop.business_unit if sop else "N/A"}

{sop_text if sop_text else "NO SOP TEXT FOUND — this SOP does not appear to address this regulation clause."}

Return your assessment as a JSON object."""

    client = get_client()
    start = time.time()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            break
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise

    elapsed = time.time() - start
    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start_idx = raw.find("{")
        end_idx = raw.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            data = json.loads(raw[start_idx:end_idx])
        else:
            data = {
                "compliance_level": "gap",
                "severity": "high",
                "evidence_quote": "",
                "gap_description": f"LLM returned unparseable response",
                "remediation": "Manual review required",
                "reasoning": raw[:500],
            }

    metrics = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "latency": elapsed,
    }

    finding = AuditFinding(
        clause_id=clause.clause_id,
        clause_title=clause.title,
        regulation=clause.regulation,
        sop_id=sop.sop_id if sop else "NONE",
        sop_title=sop.title if sop else "No applicable SOP",
        business_unit=sop.business_unit if sop else "N/A",
        compliance_level=ComplianceLevel(data.get("compliance_level", "gap")),
        severity=Severity(data.get("severity", "high")),
        evidence_quote=data.get("evidence_quote", ""),
        gap_description=data.get("gap_description", ""),
        remediation=data.get("remediation", ""),
        reasoning=data.get("reasoning", ""),
    )

    return finding, metrics


def audit_sop(
    sop_chunks: list[SOPChunk],
    regulation_text: str,
    regulations: list[str] | None = None,
) -> tuple[list[AuditFinding], dict]:
    """Audit one SOP against regulation text retrieved from Pinecone."""
    sop = sop_chunks[0] if sop_chunks else None
    sop_text = "\n\n---\n\n".join(
        f"[{c.section}]\n{c.chunk_text}" for c in sop_chunks
    )

    regs_label = ", ".join(regulations) if regulations else "all applicable regulations"

    system_prompt = """You are Sentinel, an expert regulatory compliance auditor for Meridian Health Technologies.
You assess enterprise SOPs against regulation requirements. You are thorough, precise, and cite evidence directly.

You receive the actual regulation text retrieved from the regulatory corpus. Identify every specific requirement in the regulation text that applies to this SOP, and assess the SOP's compliance with each one.

You MUST return a valid JSON array. Each element has these fields:
- requirement_id: a short identifier for the requirement (e.g. "HIPAA-164.312(a)" or "CC6.1" or "GDPR-Art.32")
- requirement_title: brief title of the requirement
- regulation: which regulation this comes from (e.g. "HIPAA", "SOC 2", "GDPR")
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP text that supports your finding (or empty string)
- gap_description: what is missing or insufficient (empty string if compliant)
- remediation: specific recommended action (empty string if compliant)
- reasoning: 2-3 sentence explanation citing the specific regulation section

Severity guide:
- critical: complete absence of required control for a high-risk area
- high: significant gap that could lead to regulatory finding
- medium: partial coverage with notable weaknesses
- low: minor documentation or process improvement needed
- info: compliant, no action needed

You MUST NOT downgrade severity based on commercial pressure or aspirational language. Only cite requirements that are actually present in the regulation text provided."""

    user_prompt = f"""Assess the following SOP against the regulation text below.
Identify all applicable requirements and return one JSON object per requirement.

## SOP
SOP: {sop.sop_id if sop else "N/A"} — {sop.title if sop else "No SOP found"}
Business Unit: {sop.business_unit if sop else "N/A"}
Applicable Regulations: {regs_label}

{sop_text if sop_text else "NO SOP TEXT FOUND."}

## Regulation Text (from regulatory corpus)
{regulation_text}

Return your assessment as a JSON array."""

    client = get_client()
    start = time.time()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            break
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise

    elapsed = time.time() - start
    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        start_idx = raw.find("[")
        end_idx = raw.rfind("]") + 1
        if start_idx >= 0 and end_idx > start_idx:
            items = json.loads(raw[start_idx:end_idx])
        else:
            items = []

    if not isinstance(items, list):
        items = [items]

    findings = []
    for data in items:
        rid = data.get("requirement_id", data.get("clause_id", ""))
        findings.append(AuditFinding(
            clause_id=rid,
            clause_title=data.get("requirement_title", data.get("clause_title", "")),
            regulation=data.get("regulation", regulations[0] if regulations else ""),
            sop_id=sop.sop_id if sop else "NONE",
            sop_title=sop.title if sop else "No applicable SOP",
            business_unit=sop.business_unit if sop else "N/A",
            compliance_level=ComplianceLevel(data.get("compliance_level", "gap")),
            severity=Severity(data.get("severity", "high")),
            evidence_quote=data.get("evidence_quote", ""),
            gap_description=data.get("gap_description", ""),
            remediation=data.get("remediation", ""),
            reasoning=data.get("reasoning", ""),
        ))

    metrics = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "latency": elapsed,
    }

    return findings, metrics
