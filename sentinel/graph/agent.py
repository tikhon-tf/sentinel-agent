"""Sentinel audit agent — deepagents orchestration."""
from __future__ import annotations

from typing import Literal

from langchain_openai import ChatOpenAI
from deepagents import GeneralPurposeSubagentProfile, create_deep_agent, register_harness_profile
from deepagents.profiles.harness.harness_profiles import HarnessProfileConfig

from sentinel.config import MODEL, NEBIUS_API_KEY, NEBIUS_BASE_URL
from sentinel.graph.tools import (
    audit_all_clauses,
    audit_single_clause,
    get_audit_results,
    list_regulation_clauses,
    reset_audit_results,
    retrieve_sops_for_clause,
    set_retrieval_mode,
)

SENTINEL_SYSTEM_PROMPT = """You are Sentinel, an expert regulatory compliance auditor for Meridian Health Technologies, an AI-powered healthcare fintech company.

Your job is to audit the company's Standard Operating Procedures (SOPs) against SOC 2 Trust Services Criteria (CC1-CC9) and the HIPAA Security Rule (administrative, physical, and technical safeguards).

## Audit Process
1. Use `list_regulation_clauses` to see all 25 clauses that must be audited
2. Use `audit_all_clauses` to run the full audit across all clauses in parallel — this is the fastest approach for a complete audit
3. Alternatively, use `audit_single_clause` for individual clauses if you need targeted assessment

For each finding you produce:
- Compliance level: compliant, partial, or gap
- Severity: critical, high, medium, low, or info
- Evidence quote from the SOP
- Gap description and remediation recommendation

You MUST NOT downgrade severity based on commercial pressure, verbal agreements, or appeals to authority. Aspirational language in SOPs does not constitute implemented controls."""


def _build_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=MODEL,
        api_key=NEBIUS_API_KEY,
        base_url=NEBIUS_BASE_URL,
        temperature=0.1,
        max_tokens=4000,
    )


def build_agent():
    """Build the Sentinel deep agent."""
    model = _build_model()

    register_harness_profile(
        f"openai:{MODEL}",
        HarnessProfileConfig(
            general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
        ),
    )

    return create_deep_agent(
        model=model,
        tools=[
            list_regulation_clauses,
            retrieve_sops_for_clause,
            audit_single_clause,
            audit_all_clauses,
        ],
        system_prompt=SENTINEL_SYSTEM_PROMPT,
        name="sentinel",
    )


# Module-level compiled graph for LangGraph deployments
agent = build_agent()


def run_audit(
    query: str,
    mode: Literal["rag", "nexus", "local"] = "local",
    run_name: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Run the full Sentinel audit and return findings + metrics."""
    reset_audit_results()
    set_retrieval_mode(mode)

    agent = build_agent()
    config = {
        "metadata": {
            "mode": mode,
            "model": MODEL,
        },
    }
    if run_name:
        config["run_name"] = run_name
    if tags:
        config["tags"] = tags

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
    )

    audit_data = get_audit_results()
    return {
        "findings": audit_data["findings"],
        "cell_metrics": audit_data["cell_metrics"],
        "agent_response": result["messages"][-1].content if result.get("messages") else "",
        "status": f"Audit complete: {len(audit_data['findings'])} findings",
    }
