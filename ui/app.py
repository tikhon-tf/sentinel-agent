"""Sentinel Audit Agent — Streamlit UI."""
from __future__ import annotations

import asyncio
import json

import streamlit as st
from langgraph_sdk import get_client

LANGGRAPH_URL = "http://localhost:2024"
GRAPH_ID = "sentinel"

st.set_page_config(
    page_title="Sentinel Compliance Auditor",
    page_icon="<shield>",
    layout="wide",
)

SEVERITY_COLORS = {
    "critical": "#dc2626",
    "high": "#ea580c",
    "medium": "#ca8a04",
    "low": "#2563eb",
    "info": "#6b7280",
}

COMPLIANCE_COLORS = {
    "gap": "#dc2626",
    "partial": "#ca8a04",
    "compliant": "#16a34a",
}


async def get_or_create_thread():
    client = get_client(url=LANGGRAPH_URL)
    if "thread_id" not in st.session_state:
        thread = await client.threads.create()
        st.session_state.thread_id = thread["thread_id"]
    return st.session_state.thread_id


async def stream_response(thread_id: str, message: str):
    client = get_client(url=LANGGRAPH_URL)
    chunks = []
    async for event in client.runs.stream(
        thread_id=thread_id,
        assistant_id=GRAPH_ID,
        input={"messages": [{"role": "user", "content": message}]},
        stream_mode="messages-tuple",
    ):
        if event.event == "messages" and event.data:
            msg_type, msg_data = event.data
            if msg_type == "ai" and isinstance(msg_data, dict):
                content = msg_data.get("content", "")
                if isinstance(content, str) and content:
                    chunks.append(content)
                    yield "".join(chunks)


async def get_thread_messages(thread_id: str):
    client = get_client(url=LANGGRAPH_URL)
    state = await client.threads.get_state(thread_id)
    return state.get("values", {}).get("messages", [])


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

        if st.button("List Regulation Clauses", use_container_width=True):
            st.session_state.pending_message = "List all regulation clauses that need to be audited."

        if st.button("Audit CC6 (Access Controls)", use_container_width=True):
            st.session_state.pending_message = "Audit clause CC6 — Logical and Physical Access Controls."

        if st.button("Audit HIPAA Technical Safeguards", use_container_width=True):
            st.session_state.pending_message = (
                "Audit clauses HIPAA-TECH-1 through HIPAA-TECH-5 (technical safeguards)."
            )

        st.divider()

        if st.button("New Conversation", use_container_width=True):
            for key in ["thread_id", "messages"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.divider()
        st.caption("Powered by DeepSeek-V4-Pro on Nebius")
        st.caption("Orchestrated by deepagents + LangGraph")


def render_findings_table(findings: list[dict]):
    if not findings:
        return

    gap_count = sum(1 for f in findings if f.get("compliance_level") == "gap")
    partial_count = sum(1 for f in findings if f.get("compliance_level") == "partial")
    compliant_count = sum(1 for f in findings if f.get("compliance_level") == "compliant")
    total = len(findings)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Findings", total)
    col2.metric("Gaps", gap_count, delta=f"{100*gap_count//max(total,1)}%", delta_color="inverse")
    col3.metric("Partial", partial_count, delta=f"{100*partial_count//max(total,1)}%", delta_color="off")
    col4.metric("Compliant", compliant_count, delta=f"{100*compliant_count//max(total,1)}%", delta_color="normal")

    critical = sum(1 for f in findings if f.get("severity") == "critical")
    high = sum(1 for f in findings if f.get("severity") == "high")
    medium = sum(1 for f in findings if f.get("severity") == "medium")

    severity_cols = st.columns(3)
    severity_cols[0].metric("Critical", critical)
    severity_cols[1].metric("High", high)
    severity_cols[2].metric("Medium", medium)


def main():
    render_sidebar()

    st.title("Sentinel Compliance Auditor")
    st.caption("AI-powered regulatory audit for SOC 2 and HIPAA Security Rule")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pending = st.session_state.pop("pending_message", None)
    user_input = st.chat_input("Ask Sentinel to audit a regulation clause, review an SOP, or run a full audit...")

    prompt = pending or user_input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")

            thread_id = asyncio.run(get_or_create_thread())

            full_response = ""
            try:
                async def _stream():
                    nonlocal full_response
                    async for text in stream_response(thread_id, prompt):
                        full_response = text
                        placeholder.markdown(text + " |")
                asyncio.run(_stream())
            except Exception:
                if not full_response:
                    messages = asyncio.run(get_thread_messages(thread_id))
                    for m in reversed(messages):
                        content = m.get("content", "") if isinstance(m, dict) else getattr(m, "content", "")
                        msg_type = m.get("type", "") if isinstance(m, dict) else getattr(m, "type", "")
                        if msg_type == "ai" and content:
                            full_response = content
                            break

            if not full_response:
                full_response = "Audit is running. Check the output files for results."

            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
