"""Sentinel Audit Agent — Streamlit UI."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

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


def _get_client():
    url = st.session_state.get("langgraph_url", DEFAULT_URL)
    kwargs = {"url": url}
    if LANGSMITH_API_KEY and "localhost" not in url:
        kwargs["api_key"] = LANGSMITH_API_KEY
    return get_sync_client(**kwargs)


def get_or_create_thread():
    client = _get_client()
    if "thread_id" not in st.session_state:
        thread = client.threads.create()
        st.session_state.thread_id = thread["thread_id"]
    return st.session_state.thread_id


def stream_tokens(thread_id: str, message: str):
    """Yield individual text chunks as they arrive from the agent."""
    client = _get_client()
    for event in client.runs.stream(
        thread_id=thread_id,
        assistant_id=GRAPH_ID,
        input={"messages": [{"role": "user", "content": message}]},
        stream_mode="messages-tuple",
    ):
        if event.event == "messages" and event.data:
            msg = event.data[0] if isinstance(event.data, list) else event.data
            if isinstance(msg, dict) and "AIMessage" in msg.get("type", ""):
                content = msg.get("content", "")
                if isinstance(content, str) and content:
                    yield content


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
            thread_id = get_or_create_thread()
            full_response = st.write_stream(stream_tokens(thread_id, prompt))

            if not full_response:
                full_response = "Audit is running. Check the output files for results."
                st.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
