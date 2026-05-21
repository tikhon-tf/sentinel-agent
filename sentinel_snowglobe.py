"""Snowglobe agent wrapper — bridges Sentinel to the Snowglobe test harness.

Set SNOWGLOBE_ACT=1 for GPT-5.5 (Act 1) or SNOWGLOBE_ACT=2 (default) for DeepSeek-V4-Pro (Act 2).
"""
import os

from snowglobe.client import CompletionRequest, CompletionFunctionOutputs

from sentinel.graph.agent import _build_model, SENTINEL_SYSTEM_PROMPT
from sentinel.graph.tools import build_tools

ACT = int(os.environ.get("SNOWGLOBE_ACT", "2"))

_agent = None


def _get_agent():
    global _agent
    if _agent is None:
        from langgraph.prebuilt import create_react_agent

        if ACT == 1:
            model = _build_model("openai")
            tools = build_tools(provider="openai", use_tavily=False)
        else:
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
        config={"tags": ["act3", "snowglobe", f"act{ACT}"]},
    )
    reply = result["messages"][-1].content if result.get("messages") else ""
    return CompletionFunctionOutputs(response=reply)
