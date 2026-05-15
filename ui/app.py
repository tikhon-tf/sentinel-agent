"""Sentinel Audit Agent — Streamlit UI."""
from __future__ import annotations

import os
import re
import threading
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()  # also check cwd and parent dirs

import streamlit as st
from langgraph_sdk import get_sync_client

DEFAULT_URL = os.environ.get(
    "LANGGRAPH_URL",
    "https://sentinel-agent-c4dfa65772015432b388f980262380a8.us.langgraph.app",
)
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY", "")
GRAPH_ID = "sentinel"

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


def stream_events(thread_id: str, message: str):
    """Yield (event_type, data) tuples from a background thread."""
    import queue

    q: queue.Queue[tuple | None] = queue.Queue()

    def _produce():
        try:
            client = _get_client()
            for event in client.runs.stream(
                thread_id=thread_id,
                assistant_id=GRAPH_ID,
                input={"messages": [{"role": "user", "content": message}]},
                stream_mode="messages-tuple",
            ):
                if event.event == "messages" and event.data:
                    msg = event.data[0] if isinstance(event.data, list) else event.data
                    if not isinstance(msg, dict):
                        continue
                    msg_type = msg.get("type", "")
                    content = msg.get("content", "")
                    tool_calls = msg.get("tool_calls", [])

                    if "AIMessage" in msg_type:
                        if tool_calls and tool_calls[0].get("name"):
                            q.put(("tool_call", tool_calls[0]))
                        elif isinstance(content, str) and content:
                            q.put(("token", content))
                    elif "ToolMessage" in msg_type and content:
                        q.put(("tool_result", content))
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


def render_sidebar():
    with st.sidebar:
        st.markdown("## Sentinel")
        st.caption("Regulatory Compliance Auditor")
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
            for key in ["thread_id", "messages"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.divider()
        st.text_input(
            "LangGraph API URL",
            value=DEFAULT_URL,
            key="langgraph_url",
            help="Cloud deployment or http://localhost:2024 for local dev",
        )

        st.divider()
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
            text_placeholder = st.empty()
            status_placeholder = st.empty()
            results_container = st.container()

            collected_text = []
            last_tool_result = ""

            for event_type, data in stream_events(thread_id, prompt):
                if event_type == "token":
                    collected_text.append(data)
                    text_placeholder.markdown("".join(collected_text))
                    status_placeholder.empty()
                elif event_type == "tool_call":
                    status_placeholder.info(_format_tool_status(data))
                elif event_type == "tool_result":
                    last_tool_result = data
                    status_placeholder.empty()
                    with results_container:
                        render_audit_results(data)

            status_placeholder.empty()
            full_response = "".join(collected_text)
            if not full_response:
                full_response = "Audit complete. See results above."
                text_placeholder.markdown(full_response)

            st.session_state.messages[-1] = {
                "role": "assistant",
                "content": full_response,
                "audit_result": last_tool_result,
            }


if __name__ == "__main__":
    main()
