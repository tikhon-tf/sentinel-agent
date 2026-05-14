from __future__ import annotations

import json
import time

from openai import OpenAI

from sentinel.config import MODEL, MODEL_MAX_TOKENS, NEBIUS_API_KEY, NEBIUS_BASE_URL
from sentinel.models import AuditFinding, ComplianceLevel, Severity, SOPChunk, RegulationClause


_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(base_url=NEBIUS_BASE_URL, api_key=NEBIUS_API_KEY)
    return _client


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
                model=MODEL,
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
