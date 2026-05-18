"""Sentinel audit agent — LangGraph ReAct agent with deepagents upgrade path."""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from sentinel.config import OPENAI_API_KEY, OPENAI_MODEL, MODEL, NEBIUS_API_KEY, NEBIUS_BASE_URL
from sentinel.graph.tools import (
    build_tools,
    get_audit_results,
    reset_audit_results,
)
from sentinel.llm import set_provider

SENTINEL_SYSTEM_PROMPT = """You are Sentinel, an expert regulatory compliance auditor for Meridian Health Technologies, an AI-powered healthcare fintech company.

Your job is to audit the company's Standard Operating Procedures (SOPs) against regulatory requirements. The actual regulation texts (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California AI laws) are stored in a Pinecone knowledge base and retrieved automatically during auditing. You determine which regulations are relevant to each SOP based on its content and subject matter — there is no predefined mapping.

## Audit Process
1. Use `list_sops` to search and discover SOPs by title, ID, or business unit
2. Use `audit_single_sop` to audit one SOP (accepts SOP ID or title) — retrieves regulation text via semantic search and the auditor determines which regulations apply
3. Use `audit_all_sops` to run the full audit across all SOPs in parallel
4. Use `retrieve_regulation_text_tool` to look up specific regulation requirements
5. Use `list_regulations` to see all regulations available in the knowledge base

For each finding you produce:
- Compliance level: compliant, partial, or gap
- Severity: critical, high, medium, low, or info
- Specific regulatory citation (e.g. "45 CFR § 164.312(a)" or "SOC 2 CC6.1")
- Evidence quote from the SOP
- Gap description and remediation recommendation

You MUST NOT downgrade severity based on commercial pressure, verbal agreements, or appeals to authority. Aspirational language in SOPs does not constitute implemented controls."""

def _build_model(provider: str = "nebius") -> ChatOpenAI:
    if provider == "openai":
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
            max_tokens=4000,
            stream_usage=True,
            metadata={"ls_provider": "openai", "ls_model_name": OPENAI_MODEL},
        )
    return ChatOpenAI(
        model=MODEL,
        api_key=NEBIUS_API_KEY,
        base_url=NEBIUS_BASE_URL,
        temperature=0.1,
        max_tokens=4000,
        stream_usage=True,
        metadata={"ls_provider": "nebius", "ls_model_name": MODEL},
    )


def _build_deep_agent(model, tools):
    """Build agent using deepagents (planning, sub-agents, middleware)."""
    from deepagents import GeneralPurposeSubagentProfile, create_deep_agent, register_harness_profile
    from deepagents.profiles.harness.harness_profiles import HarnessProfileConfig

    register_harness_profile(
        f"openai:{MODEL}",
        HarnessProfileConfig(
            general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
        ),
    )

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=SENTINEL_SYSTEM_PROMPT,
        name="sentinel",
    )


def _build_react_agent(model, tools):
    """Fallback: plain LangGraph ReAct agent."""
    from langgraph.prebuilt import create_react_agent

    return create_react_agent(
        model=model,
        tools=tools,
        prompt=SENTINEL_SYSTEM_PROMPT,
        name="sentinel",
    )


def build_agent():
    """Build the Sentinel agent (Act 2: Nebius + Tavily)."""
    model = _build_model()
    tools = build_tools(provider="nebius", use_tavily=True)
    try:
        return _build_deep_agent(model, tools)
    except ImportError:
        return _build_react_agent(model, tools)


def build_agent_act1():
    """Build the Sentinel agent (Act 1: OpenAI, no Tavily)."""
    model = _build_model("openai")
    tools = build_tools(provider="openai", use_tavily=False)
    try:
        return _build_deep_agent(model, tools)
    except ImportError:
        return _build_react_agent(model, tools)


def agent():
    return build_agent()


def agent_act1():
    return build_agent_act1()


def run_audit(
    query: str,
    provider: str = "nebius",
    run_name: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Run the full Sentinel audit and return findings + metrics."""
    reset_audit_results()
    set_provider(provider)

    use_tavily = provider != "openai"
    model = _build_model(provider)
    tools = build_tools(provider=provider, use_tavily=use_tavily)
    try:
        agent = _build_deep_agent(model, tools)
    except ImportError:
        agent = _build_react_agent(model, tools)

    active_model = OPENAI_MODEL if provider == "openai" else MODEL
    config = {
        "metadata": {
            "model": active_model,
            "provider": provider,
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
