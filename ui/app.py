"""Sentinel Audit Agent — Streamlit UI."""
from __future__ import annotations

import os
import re
import threading
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()  # also check cwd and parent dirs

import streamlit as st
from langgraph_sdk import get_sync_client
from sentinel.config import OPENAI_MODEL, MODEL, PRICING

DEFAULT_URL = os.environ.get(
    "LANGGRAPH_URL",
    "https://sentinel-agent-c4dfa65772015432b388f980262380a8.us.langgraph.app",
)
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY", "")
AGENTS = {
    "Nebius + Nexus + Tavily": {"graph_id": "sentinel", "model": MODEL},
    "Agent + RAG": {"graph_id": "sentinel_act1", "model": OPENAI_MODEL},
}

st.set_page_config(
    page_title="Sentinel Compliance Auditor",
    page_icon="<shield>",
    layout="wide",
)

TOOL_LABELS = {
    "list_sops": "Searching SOPs...",
    "list_regulations": "Listing regulations in knowledge base...",
    "retrieve_regulation_text_tool": "Retrieving regulation text...",
    "audit_single_sop": "Auditing SOP...",
    "audit_all_sops": "Running full audit across all SOPs...",
}


def _get_client():
    url = st.session_state.get("langgraph_url", DEFAULT_URL)
    kwargs = {"url": url}
    if LANGSMITH_API_KEY and "localhost" not in url:
        kwargs["api_key"] = LANGSMITH_API_KEY
    elif "localhost" not in url and not LANGSMITH_API_KEY:
        st.error(
            "LANGSMITH_API_KEY is required to connect to the cloud deployment. "
            "Set it in your .env file or environment, or use `make ui-local` for local dev."
        )
        st.stop()
    return get_sync_client(**kwargs)


def get_or_create_thread():
    client = _get_client()
    if "thread_id" not in st.session_state:
        thread = client.threads.create()
        st.session_state.thread_id = thread["thread_id"]
    return st.session_state.thread_id


def stream_events(thread_id: str, message: str, graph_id: str = "sentinel"):
    """Yield (event_type, data) tuples from a background thread.

    Uses both 'messages-tuple' (for streaming tokens) and 'values' (for
    usage_metadata, which is only available in values snapshots — LangGraph
    checkpoints do not preserve it in thread state).
    """
    import queue

    q: queue.Queue[tuple | None] = queue.Queue()

    def _produce():
        try:
            client = _get_client()
            for event in client.runs.stream(
                thread_id=thread_id,
                assistant_id=graph_id,
                input={"messages": [{"role": "user", "content": message}]},
                stream_mode=["messages-tuple", "values"],
            ):
                if event.event == "messages" and event.data:
                    msg = event.data[0] if isinstance(event.data, list) else event.data
                    if not isinstance(msg, dict):
                        continue
                    msg_type = msg.get("type", "")
                    content = msg.get("content", "")
                    tool_calls = msg.get("tool_calls", [])

                    if msg_type in ("AIMessageChunk", "AIMessage", "ai"):
                        if tool_calls and tool_calls[0].get("name"):
                            q.put(("tool_call", tool_calls[0]))
                        elif isinstance(content, str) and content:
                            q.put(("token", content))
                    elif msg_type in ("tool", "ToolMessage", "ToolMessageChunk") and content:
                        q.put(("tool_result", content))

                elif event.event == "values" and isinstance(event.data, dict):
                    usage_snapshot = []
                    for msg in event.data.get("messages", []):
                        if not isinstance(msg, dict):
                            continue
                        usage = msg.get("usage_metadata")
                        if usage and (usage.get("input_tokens") or usage.get("output_tokens")):
                            usage_snapshot.append(usage)
                    if usage_snapshot:
                        q.put(("usage_snapshot", usage_snapshot))
        except Exception:
            pass
        finally:
            q.put(None)

    thread = threading.Thread(target=_produce, daemon=True)
    thread.start()

    while True:
        try:
            item = q.get(timeout=0.1)
        except queue.Empty:
            continue
        if item is None:
            break
        yield item


DEFAULT_PRICING = {"input": 1.75, "output": 3.50}


def _format_usage(input_tokens: int, output_tokens: int, model: str = MODEL, latency: float = 0.0) -> str:
    total = input_tokens + output_tokens
    prices = PRICING.get(model, DEFAULT_PRICING)
    cost = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
    parts = [f"Tokens: {total:,} ({input_tokens:,} in / {output_tokens:,} out)", f"Cost: ${cost:.4f}"]
    if latency > 0:
        parts.append(f"Latency: {latency:.1f}s")
    return " · ".join(parts)


def _parse_subagent_usage(tool_result: str) -> tuple[int, int]:
    """Extract sub-agent token counts from tool result string."""
    match = re.search(r"Sub-agent tokens:\s*([\d,]+)\s*\(([\d,]+)\s*in\s*/\s*([\d,]+)\s*out\)", tool_result)
    if match:
        return int(match.group(2).replace(",", "")), int(match.group(3).replace(",", ""))
    return 0, 0


def _format_tool_status(tool_call: dict) -> str:
    name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    template = TOOL_LABELS.get(name, f"Calling {name}...")
    try:
        return template.format(**args)
    except KeyError:
        return template.split("{")[0].rstrip() + "..."


def _parse_audit_table(tool_result: str) -> list[dict] | None:
    """Try to extract structured findings from an audit_all_sops result."""
    if "Audit complete:" not in tool_result:
        return None

    findings = []
    for line in tool_result.split("\n"):
        line = line.strip()
        if not line or line.startswith("Audit complete") or line.startswith("Compliant") or line.startswith("Partial") or line.startswith("Gap") or line.startswith("Per-SOP"):
            continue
        match = re.match(r"([\w/.:-]+):\s+(\d+)\s+findings?\s+.*?(\d+)C/(\d+)P/(\d+)G", line)
        if match:
            findings.append({
                "sop": match.group(1),
                "findings": int(match.group(2)),
                "compliant": int(match.group(3)),
                "partial": int(match.group(4)),
                "gap": int(match.group(5)),
            })
    return findings if findings else None


def render_audit_results(tool_result: str):
    """Render tool results with structured formatting when possible."""
    findings = _parse_audit_table(tool_result)
    if findings:
        total_c = sum(f["compliant"] for f in findings)
        total_p = sum(f["partial"] for f in findings)
        total_g = sum(f["gap"] for f in findings)
        total = total_c + total_p + total_g

        cols = st.columns(4)
        cols[0].metric("Total Findings", total)
        cols[1].metric("Compliant", total_c)
        cols[2].metric("Partial", total_p)
        cols[3].metric("Gaps", total_g)

        import pandas as pd
        df = pd.DataFrame(findings)
        df.columns = ["SOP", "Findings", "Compliant", "Partial", "Gap"]

        def _color_row(row):
            if row["Gap"] > 0:
                return ["background-color: #fecaca"] * len(row)
            if row["Partial"] > 0:
                return ["background-color: #fef3c7"] * len(row)
            return ["background-color: #d1fae5"] * len(row)

        st.dataframe(
            df.style.apply(_color_row, axis=1),
            use_container_width=True,
            hide_index=True,
        )
        return

    if len(tool_result) > 200:
        with st.expander("Tool output", expanded=False):
            st.text(tool_result)


def _active_agent() -> dict:
    label = st.session_state.get("agent_select", list(AGENTS.keys())[0])
    return AGENTS[label]


def render_sidebar():
    with st.sidebar:
        st.markdown("## Sentinel")
        st.caption("Regulatory Compliance Auditor")
        st.divider()

        st.radio("Agent", list(AGENTS.keys()), key="agent_select")

        st.divider()
        st.markdown("### Quick Audits")
        if st.button("Full SOC 2 + HIPAA Audit", use_container_width=True):
            st.session_state.pending_message = (
                "Audit Meridian Health Technologies' internal Information Security and PHI Handling "
                "SOPs against SOC 2 Trust Services Criteria (CC1 through CC9) and the HIPAA Security "
                "Rule (45 CFR 164.308 administrative safeguards, 164.310 physical safeguards, "
                "164.312 technical safeguards). For each finding, report: the compliance level "
                "(compliant, partial, or gap), the exact criterion or safeguard violated, a quoted "
                "piece of evidence from the SOP, a recommended remediation, and a severity rating."
            )

        if st.button("Audit 2 SOPs", use_container_width=True):
            st.session_state.pending_message = "Audit SOP-AIML-004 and SOP-AIML-008"

        if st.button("List Regulations", use_container_width=True):
            st.session_state.pending_message = "List all regulations available in the knowledge base."

        if st.button("Audit All SOPs", use_container_width=True):
            st.session_state.pending_message = "Run the full audit across all SOPs against their tagged regulations."

        if st.button("Audit HIPAA SOPs", use_container_width=True):
            st.session_state.pending_message = (
                "Audit all SOPs tagged with HIPAA regulations — focus on Security Rule technical "
                "and administrative safeguards (45 CFR 164.308, 164.310, 164.312)."
            )

        st.divider()

        if st.button("New Conversation", use_container_width=True):
            for key in ["thread_id", "messages", "total_input_tokens", "total_output_tokens", "_prev_outer_in", "_prev_outer_out"]:
                st.session_state.pop(key, None)
            st.rerun()

        session_in = st.session_state.get("total_input_tokens", 0)
        session_out = st.session_state.get("total_output_tokens", 0)
        if session_in + session_out > 0:
            st.divider()
            st.markdown("### Session Usage")
            active_model = _active_agent()["model"]
            prices = PRICING.get(active_model, DEFAULT_PRICING)
            session_cost = (session_in * prices["input"] + session_out * prices["output"]) / 1_000_000
            st.metric("Total Tokens", f"{session_in + session_out:,}")
            st.caption(f"{session_in:,} in / {session_out:,} out · ${session_cost:.4f}")

        st.divider()
        st.text_input(
            "LangGraph API URL",
            value=DEFAULT_URL,
            key="langgraph_url",
            help="Cloud deployment or http://localhost:2024 for local dev",
        )

        st.divider()
        active_model = _active_agent()["model"]
        if active_model == OPENAI_MODEL:
            st.caption("Powered by GPT-5.5 on OpenAI")
        else:
            st.caption("Powered by DeepSeek-V4-Pro on Nebius")
        st.caption("Orchestrated by deepagents + LangGraph")


def main():
    render_sidebar()

    st.title("Sentinel Compliance Auditor")
    st.caption("AI-powered regulatory audit for HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF & more")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        if not msg["content"]:
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("audit_result"):
                render_audit_results(msg["audit_result"])
            if msg.get("usage"):
                st.caption(msg["usage"])

    pending = st.session_state.pop("pending_message", None)
    user_input = st.chat_input("Ask Sentinel to audit a regulation clause, review an SOP, or run a full audit...")

    prompt = pending or user_input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": "", "audit_result": ""})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            thread_id = get_or_create_thread()
            agent_cfg = _active_agent()
            text_placeholder = st.empty()
            status_placeholder = st.empty()
            results_container = st.container()
            usage_placeholder = st.empty()

            collected_text = []
            last_tool_result = ""
            last_usage_snapshot = []
            subagent_in = 0
            subagent_out = 0
            t_start = time.time()

            for event_type, data in stream_events(thread_id, prompt, agent_cfg["graph_id"]):
                if event_type == "token":
                    collected_text.append(data)
                    text_placeholder.markdown("".join(collected_text))
                    status_placeholder.empty()
                elif event_type == "tool_call":
                    status_placeholder.info(_format_tool_status(data))
                elif event_type == "tool_result":
                    last_tool_result = data
                    status_placeholder.empty()
                    sa_in, sa_out = _parse_subagent_usage(data)
                    subagent_in += sa_in
                    subagent_out += sa_out
                    with results_container:
                        render_audit_results(data)
                elif event_type == "usage_snapshot":
                    last_usage_snapshot = data

            status_placeholder.empty()
            full_response = "".join(collected_text)
            if not full_response:
                full_response = "Audit complete. See results above."
                text_placeholder.markdown(full_response)

            outer_in = sum(u.get("input_tokens", 0) for u in last_usage_snapshot)
            outer_out = sum(u.get("output_tokens", 0) for u in last_usage_snapshot)
            prev_in = st.session_state.get("_prev_outer_in", 0)
            prev_out = st.session_state.get("_prev_outer_out", 0)
            run_outer_in = max(outer_in - prev_in, 0)
            run_outer_out = max(outer_out - prev_out, 0)
            run_in = run_outer_in + subagent_in
            run_out = run_outer_out + subagent_out
            run_total = run_in + run_out
            elapsed = time.time() - t_start
            usage_info = _format_usage(run_in, run_out, agent_cfg["model"], latency=elapsed)
            if run_total > 0:
                usage_placeholder.caption(usage_info)
                st.session_state["_prev_outer_in"] = outer_in
                st.session_state["_prev_outer_out"] = outer_out
                st.session_state["total_input_tokens"] = st.session_state.get("total_input_tokens", 0) + run_in
                st.session_state["total_output_tokens"] = st.session_state.get("total_output_tokens", 0) + run_out

            st.session_state.messages[-1] = {
                "role": "assistant",
                "content": full_response,
                "audit_result": last_tool_result,
                "usage": usage_info if run_total > 0 else "",
            }


if __name__ == "__main__":
    main()
