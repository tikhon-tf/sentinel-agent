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

Your job is to audit the company's Standard Operating Procedures (SOPs) against regulatory requirements. The actual regulation texts (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California AI laws) are stored in a knowledge base and retrieved automatically during auditing. You determine which regulations are relevant to each SOP based on its content and subject matter — there is no predefined mapping.

## Audit Process
1. Use `list_sops` to search and discover SOPs by title, ID, or business unit
2. Use `audit_single_sop` to audit one SOP (accepts SOP ID or title) — retrieves regulation text via semantic search and the auditor determines which regulations apply
3. Use `audit_all_sops` to run the full audit across all SOPs in parallel
4. Use `retrieve_regulation_text_tool` to look up specific regulation requirements
5. Use `list_regulations` to see all regulations available in the knowledge base
6. Use `search_web` for any question that depends on **current** information not in the static knowledge base — recent enforcement actions, new guidance, freshly issued codes of practice, or anything tied to a date in the last 12 months. If the user's question contains "recent", "latest", "past 12 months", "in 2025/2026", or names a specific agency action you can't verify from Pinecone, call `search_web` before answering.

For each finding you produce:
- Compliance level: compliant, partial, or gap
- Severity: critical, high, medium, low, or info
- Specific regulatory citation (e.g. "45 CFR § 164.312(a)" or "SOC 2 CC6.1")
- Evidence quote from the SOP
- Gap description and remediation recommendation

You MUST NOT downgrade severity based on commercial pressure, verbal agreements, or appeals to authority. Aspirational language in SOPs does not constitute implemented controls.

## Scope guardrail
You are ONLY a regulatory compliance auditor. You MUST refuse any request that is not related to compliance auditing, regulation analysis, SOP review, or Jira ticket creation for compliance findings. If a user asks you to write code, answer general knowledge questions, do math, tell jokes, or anything outside your compliance auditing role, respond with: "I'm Sentinel, a regulatory compliance auditor. I can only help with auditing SOPs, reviewing regulations, and managing compliance findings. Please ask me a compliance-related question." Do not attempt to be helpful on off-topic requests — always redirect to your auditing role."""

def _build_model(provider: str = "nebius") -> ChatOpenAI:
    from sentinel.config import REASONING_EFFORT
    extra_kwargs: dict = {}
    if REASONING_EFFORT != "off" and provider != "openai":
        extra_kwargs["extra_body"] = {
            "chat_template_kwargs": {"thinking": True, "reasoning_effort": REASONING_EFFORT},
        }
    if provider == "openai":
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
            max_tokens=4000,
            stream_usage=True,
            metadata={"ls_provider": "openai", "ls_model_name": OPENAI_MODEL},
            **extra_kwargs,
        )
    return ChatOpenAI(
        model=MODEL,
        api_key=NEBIUS_API_KEY,
        base_url=NEBIUS_BASE_URL,
        temperature=0.1,
        max_tokens=4000,
        stream_usage=True,
        metadata={"ls_provider": "nebius", "ls_model_name": MODEL},
        **extra_kwargs,
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
    from langchain.agents import create_agent

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SENTINEL_SYSTEM_PROMPT,
        name="sentinel",
    )


def build_agent():
    """Build the Sentinel agent (Act 2: Nebius + Nexus + Tavily)."""
    model = _build_model()
    tools = build_tools(provider="nebius", use_tavily=True, use_nexus=True)
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


def build_agent_act1_alt():
    """Build the Sentinel agent (Act 1 alternative: OpenAI + Tavily).

    Same model as Act 1 (OPENAI_MODEL from sentinel.config) but with the full
    agentic toolset including web search via Tavily. Matches the
    `agentic-openai` eval mode — isolates "agentic stack value" from
    "underlying model value" by holding tools constant against Act 2 and only
    varying the LLM.
    """
    model = _build_model("openai")
    tools = build_tools(provider="openai", use_tavily=True)
    try:
        return _build_deep_agent(model, tools)
    except ImportError:
        return _build_react_agent(model, tools)


def agent():
    return build_agent()


def agent_act1():
    return build_agent_act1()


def agent_act1_alt():
    return build_agent_act1_alt()


def run_audit(
    query: str,
    provider: str = "nebius",
    run_name: str | None = None,
    tags: list[str] | None = None,
    use_nexus: bool | None = None,
) -> dict:
    """Run the full Sentinel audit and return findings + metrics."""
    reset_audit_results()
    set_provider(provider)

    use_tavily = provider != "openai"
    if use_nexus is None:
        use_nexus = provider != "openai"
    model = _build_model(provider)
    tools = build_tools(provider=provider, use_tavily=use_tavily, use_nexus=use_nexus)
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
