"""Snowglobe agent wrapper — bridges Sentinel to the Snowglobe test harness."""
from snowglobe.client import CompletionRequest, CompletionFunctionOutputs

from sentinel.graph.agent import _build_model, SENTINEL_SYSTEM_PROMPT
from sentinel.graph.tools import build_tools

_agent = None


def _get_agent():
    global _agent
    if _agent is None:
        from langgraph.prebuilt import create_react_agent

        model = _build_model()
        tools = build_tools(provider="nebius", use_tavily=False)
        _agent = create_react_agent(
            model=model, tools=tools, prompt=SENTINEL_SYSTEM_PROMPT, name="sentinel",
        )
    return _agent


def completion(request: CompletionRequest) -> CompletionFunctionOutputs:
    agent = _get_agent()
    messages = request.to_openai_messages()
    result = agent.invoke(
        {"messages": messages},
        config={"tags": ["act3", "snowglobe"]},
    )
    reply = result["messages"][-1].content if result.get("messages") else ""
    return CompletionFunctionOutputs(response=reply)
