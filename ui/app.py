"""Sentinel Audit Agent — Streamlit UI."""
from __future__ import annotations

import json
import os
import queue
import random
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
    "Act 0 — Naive RAG (DeepSeek)": {"graph_id": "sentinel_act0", "model": MODEL},
    "Act 1 — Agent + RAG (OpenAI)": {"graph_id": "sentinel_act1", "model": OPENAI_MODEL},
    "Act 1-alt — OpenAI + Tavily (agentic)": {"graph_id": "sentinel_act1_alt", "model": OPENAI_MODEL},
    "Act 2 — Nebius + Tavily (agentic)": {"graph_id": "sentinel", "model": MODEL},
}

PARALLEL_AGENTS = [
    {"label": "Naive RAG (DeepSeek)", "graph_id": "sentinel_act0", "model": MODEL, "tagline": "1 retrieval + 1 LLM call, no tools"},
    {"label": "Agentic (OpenAI + Tavily)", "graph_id": "sentinel_act1_alt", "model": OPENAI_MODEL, "tagline": "ReAct + Pinecone + web"},
    {"label": "Agentic (Nebius + Tavily)", "graph_id": "sentinel", "model": MODEL, "tagline": "ReAct + Pinecone + web"},
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "eval" / "qa_dataset.jsonl"
RESULTS_PATH = PROJECT_ROOT / "data" / "eval" / "results" / "comparison_3way_20260521.json"
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "nebius-logo.svg"

st.set_page_config(
    page_title="Sentinel Compliance Auditor",
    page_icon="<shield>",
    layout="wide",
)

# Nebius design tokens (from forge.eu-north1.osmo.nebius.cloud CSS).
NEBIUS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --nebius-lime: #DAFF33;
    --nebius-lime-dim: #B8DD1F;
    --nebius-amber: #FFAC3C;
    --nebius-green: #5ECF71;
    --nebius-red: #FF5958;
    --nebius-bg: #021621;
    --nebius-surface: #052B42;
    --nebius-surface-hi: #083149;
    --nebius-border: rgba(240, 248, 255, 0.10);
    --nebius-text: #F0F8FF;
    --nebius-muted: #9CA3AF;
}

html, body, [class*="st-"], .stMarkdown, .stChatMessage, p, span, div, label, input, textarea, button {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

code, pre, .stCode, [data-testid="stMarkdownContainer"] code {
    font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
}

/* Primary buttons — Nebius lime accent */
.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: var(--nebius-lime) !important;
    color: #021621 !important;
    border: 1px solid var(--nebius-lime) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: background 120ms ease, transform 120ms ease;
}
.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: var(--nebius-lime-dim) !important;
    border-color: var(--nebius-lime-dim) !important;
}

/* Secondary buttons — outlined */
.stButton > button:not([kind="primary"]),
.stDownloadButton > button:not([kind="primary"]) {
    background: transparent !important;
    color: var(--nebius-text) !important;
    border: 1px solid var(--nebius-border) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: background 120ms ease, border-color 120ms ease;
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--nebius-surface) !important;
    border-color: rgba(218, 255, 51, 0.40) !important;
}

/* Inputs, selectboxes, textareas */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
[data-testid="stChatInput"] {
    background-color: var(--nebius-surface) !important;
    border: 1px solid var(--nebius-border) !important;
    border-radius: 8px !important;
    color: var(--nebius-text) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--nebius-lime) !important;
    box-shadow: 0 0 0 1px var(--nebius-lime) !important;
}

/* Containers with border={true} — card style */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--nebius-border) !important;
    border-radius: 12px !important;
    background: rgba(5, 43, 66, 0.50);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid var(--nebius-border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--nebius-muted) !important;
    font-weight: 500 !important;
    padding: 12px 18px !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--nebius-text) !important;
    border-bottom: 2px solid var(--nebius-lime) !important;
}

/* Dataframes */
.stDataFrame, [data-testid="stDataFrame"] {
    border: 1px solid var(--nebius-border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--nebius-surface);
    border: 1px solid var(--nebius-border);
    border-radius: 12px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] {
    color: var(--nebius-lime) !important;
    font-weight: 600 !important;
}

/* Chat messages */
.stChatMessage {
    background: var(--nebius-surface) !important;
    border: 1px solid var(--nebius-border) !important;
    border-radius: 12px !important;
}

/* Code blocks */
.stCodeBlock, pre code {
    background: var(--nebius-surface-hi) !important;
    border: 1px solid var(--nebius-border) !important;
    border-radius: 8px !important;
}

/* Expanders */
.streamlit-expanderHeader, [data-testid="stExpander"] details summary {
    background: var(--nebius-surface) !important;
    border-radius: 8px !important;
}

/* Info / success / warning / error banners */
.stAlert {
    border-radius: 8px !important;
    border-width: 1px !important;
}

/* Dividers — softer */
hr {
    border-color: var(--nebius-border) !important;
}

/* Title accent bar */
h1:first-of-type::before {
    content: "";
    display: inline-block;
    width: 4px;
    height: 1.1em;
    background: var(--nebius-lime);
    margin-right: 12px;
    vertical-align: -3px;
    border-radius: 2px;
}
</style>
"""

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


def _stream_producer(
    thread_id: str,
    message: str,
    graph_id: str,
    q: "queue.Queue[tuple | None]",
    url: str | None = None,
    api_key: str | None = None,
):
    """Stream LangGraph events into a queue. Producer for one agent run.

    url/api_key may be passed explicitly so background threads never touch
    st.session_state (which can stall or fail under Streamlit's thread context).
    """
    try:
        if url is None:
            client = _get_client()
        else:
            kwargs = {"url": url}
            if api_key:
                kwargs["api_key"] = api_key
            client = get_sync_client(**kwargs)
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
    except Exception as exc:
        q.put(("error", str(exc)))
    finally:
        q.put(None)


def stream_events(thread_id: str, message: str, graph_id: str = "sentinel"):
    """Yield (event_type, data) tuples from a single background stream."""
    q: queue.Queue[tuple | None] = queue.Queue()
    thread = threading.Thread(
        target=_stream_producer, args=(thread_id, message, graph_id, q), daemon=True
    )
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
        match = re.match(r"(SOP-[A-Z]+-\d+)\s+\([^)]*\):\s+(\d+)\s+findings?\s+.*?(\d+)C/(\d+)P/(\d+)G", line)
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


def render_chat_controls():
    """Top-of-tab controls: agent picker, URL, new-conversation, quick audits."""
    top = st.columns([3, 3, 1])
    with top[0]:
        st.selectbox("Agent", list(AGENTS.keys()), key="agent_select")
    with top[1]:
        st.text_input(
            "LangGraph API URL",
            value=DEFAULT_URL,
            key="langgraph_url",
            help="Cloud deployment or http://localhost:2024 for local dev",
        )
    with top[2]:
        st.markdown("&nbsp;")
        if st.button("New conversation", use_container_width=True):
            for key in ["thread_id", "messages", "total_input_tokens", "total_output_tokens", "_prev_outer_in", "_prev_outer_out"]:
                st.session_state.pop(key, None)
            st.rerun()

    qa_cols = st.columns(5)
    if qa_cols[0].button("Full SOC 2 + HIPAA Audit", use_container_width=True):
        st.session_state.pending_message = (
            "Audit Meridian Health Technologies' internal Information Security and PHI Handling "
            "SOPs against SOC 2 Trust Services Criteria (CC1 through CC9) and the HIPAA Security "
            "Rule (45 CFR 164.308 administrative safeguards, 164.310 physical safeguards, "
            "164.312 technical safeguards). For each finding, report: the compliance level "
            "(compliant, partial, or gap), the exact criterion or safeguard violated, a quoted "
            "piece of evidence from the SOP, a recommended remediation, and a severity rating."
        )
    if qa_cols[1].button("Audit 2 SOPs", use_container_width=True):
        st.session_state.pending_message = "Full audit SOP-AIML-004 and SOP-DGP-004"
    if qa_cols[2].button("List Regulations", use_container_width=True):
        st.session_state.pending_message = "List all regulations available in the knowledge base."
    if qa_cols[3].button("Audit All SOPs", use_container_width=True):
        st.session_state.pending_message = "Run the full audit across all SOPs against their tagged regulations."
    if qa_cols[4].button("Audit HIPAA SOPs", use_container_width=True):
        st.session_state.pending_message = (
            "Audit all SOPs tagged with HIPAA regulations — focus on Security Rule technical "
            "and administrative safeguards (45 CFR 164.308, 164.310, 164.312)."
        )

    # Status line: model + session usage
    active = _active_agent()
    bits = [
        "Powered by GPT-5.5 on OpenAI" if active["model"] == OPENAI_MODEL else "Powered by DeepSeek-V4-Pro on Nebius",
        "Naive RAG (single retrieval + single LLM call, no tools)" if active["graph_id"] == "sentinel_act0"
        else "Orchestrated by deepagents + LangGraph",
    ]
    session_in = st.session_state.get("total_input_tokens", 0)
    session_out = st.session_state.get("total_output_tokens", 0)
    if session_in + session_out > 0:
        prices = PRICING.get(active["model"], DEFAULT_PRICING)
        session_cost = (session_in * prices["input"] + session_out * prices["output"]) / 1_000_000
        bits.append(
            f"Session: {session_in + session_out:,} tokens "
            f"({session_in:,} in / {session_out:,} out) · ${session_cost:.4f}"
        )
    st.caption(" · ".join(bits))
    st.divider()


def render_chat_tab():
    render_chat_controls()
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
            last_tool_call_name = ""
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
                    last_tool_call_name = data.get("name", "")
                elif event_type == "tool_result":
                    last_tool_result = data
                    status_placeholder.empty()
                    if last_tool_call_name in ("audit_all_sops", "audit_single_sop"):
                        sa_in, sa_out = _parse_subagent_usage(data)
                        if last_tool_call_name == "audit_all_sops":
                            subagent_in = sa_in
                            subagent_out = sa_out
                        else:
                            subagent_in += sa_in
                            subagent_out += sa_out
                    last_tool_call_name = ""
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


@st.cache_data
def _load_dataset() -> list[dict]:
    if not DATASET_PATH.exists():
        return []
    return [json.loads(line) for line in DATASET_PATH.read_text().splitlines() if line.strip()]


def _pick_question(category: str | None = None) -> dict | None:
    data = _load_dataset()
    if not data:
        return None
    pool = [q for q in data if not category or q.get("category") == category]
    return random.choice(pool) if pool else None


def _run_parallel(question_text: str, agents: list[dict]) -> dict:
    """Spawn one producer per agent, drain queues, update placeholders live.

    Returns a dict keyed by agent index with the final result text + usage.
    """
    # Snapshot URL + api key in MAIN thread so background producers never touch
    # st.session_state (which can block under Streamlit's thread context and
    # serialize what should be parallel network I/O).
    url = st.session_state.get("langgraph_url", DEFAULT_URL)
    api_key = LANGSMITH_API_KEY if (LANGSMITH_API_KEY and "localhost" not in url) else None
    if "localhost" not in url and not LANGSMITH_API_KEY:
        st.error(
            "LANGSMITH_API_KEY is required to connect to the cloud deployment. "
            "Set it in your .env file or environment, or use `make ui-local` for local dev."
        )
        st.stop()

    def _new_client():
        kwargs = {"url": url}
        if api_key:
            kwargs["api_key"] = api_key
        return get_sync_client(**kwargs)

    # Create one fresh LangGraph thread per agent — do this in parallel so the
    # 3 POST /threads round-trips don't add ~150ms of sequential warm-up.
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents)) as ex:
        futures = [ex.submit(lambda: _new_client().threads.create()) for _ in agents]
        try:
            thread_ids = [f.result()["thread_id"] for f in futures]
        except Exception as exc:
            st.error(f"Failed to create LangGraph thread: {exc}")
            return {}

    cols = st.columns(len(agents))
    placeholders = []
    for i, (col, agent) in enumerate(zip(cols, agents)):
        with col:
            st.markdown(f"**{agent['label']}**")
            st.caption(agent["tagline"])
            status = st.empty()
            # Scrollable, fixed-height container for streamed text so the
            # page doesn't grow as the agent answers.
            text_box = st.container(height=480, border=True)
            with text_box:
                text = st.empty()
            metrics = st.empty()
            placeholders.append({"status": status, "text": text, "metrics": metrics})

    queues = [queue.Queue() for _ in agents]
    threads = []
    for tid, agent, q in zip(thread_ids, agents, queues):
        t = threading.Thread(
            target=_stream_producer,
            args=(tid, question_text, agent["graph_id"], q, url, api_key),
            daemon=True,
        )
        t.start()
        threads.append(t)

    state = [
        {
            "text": [],
            "tool_result": "",
            "usage": [],
            "subagent_in": 0,
            "subagent_out": 0,
            "last_tool": "",
            "done": False,
            "start": time.time(),
            "end": None,
            "error": None,
        }
        for _ in agents
    ]

    done_count = 0
    while done_count < len(agents):
        progressed = False
        for i, q in enumerate(queues):
            if state[i]["done"]:
                continue
            try:
                item = q.get_nowait()
            except queue.Empty:
                continue
            progressed = True
            if item is None:
                state[i]["done"] = True
                state[i]["end"] = time.time()
                done_count += 1
                placeholders[i]["status"].empty()
                _render_agent_metrics(placeholders[i]["metrics"], state[i], agents[i]["model"])
                continue
            etype, data = item
            if etype == "token":
                state[i]["text"].append(data)
                placeholders[i]["text"].markdown("".join(state[i]["text"]))
                placeholders[i]["status"].empty()
            elif etype == "tool_call":
                placeholders[i]["status"].info(_format_tool_status(data))
                state[i]["last_tool"] = data.get("name", "")
            elif etype == "tool_result":
                state[i]["tool_result"] = data
                placeholders[i]["status"].empty()
                if state[i]["last_tool"] in ("audit_all_sops", "audit_single_sop"):
                    sa_in, sa_out = _parse_subagent_usage(data)
                    if state[i]["last_tool"] == "audit_all_sops":
                        state[i]["subagent_in"] = sa_in
                        state[i]["subagent_out"] = sa_out
                    else:
                        state[i]["subagent_in"] += sa_in
                        state[i]["subagent_out"] += sa_out
                state[i]["last_tool"] = ""
            elif etype == "usage_snapshot":
                state[i]["usage"] = data
            elif etype == "error":
                state[i]["error"] = data
            # Live latency tick
            _render_agent_metrics(placeholders[i]["metrics"], state[i], agents[i]["model"], live=True)
        if not progressed:
            # Tick latency display for all in-flight agents so the user sees time moving.
            for i in range(len(agents)):
                if not state[i]["done"]:
                    _render_agent_metrics(placeholders[i]["metrics"], state[i], agents[i]["model"], live=True)
            time.sleep(0.05)

    for i in range(len(agents)):
        if not state[i]["text"]:
            placeholders[i]["text"].markdown("_(no streamed text — see tool output below)_")
        if state[i]["error"]:
            placeholders[i]["status"].error(f"Error: {state[i]['error']}")

    return {i: state[i] for i in range(len(agents))}


def _render_agent_metrics(placeholder, agent_state: dict, model: str, live: bool = False):
    outer_in = sum(u.get("input_tokens", 0) for u in agent_state["usage"])
    outer_out = sum(u.get("output_tokens", 0) for u in agent_state["usage"])
    in_tok = outer_in + agent_state["subagent_in"]
    out_tok = outer_out + agent_state["subagent_out"]
    end = agent_state["end"] or time.time()
    elapsed = end - agent_state["start"]
    prices = PRICING.get(model, DEFAULT_PRICING)
    cost = (in_tok * prices["input"] + out_tok * prices["output"]) / 1_000_000
    status = "running" if (live and not agent_state["done"]) else "done"
    placeholder.markdown(
        f"`{status}` &nbsp; **{elapsed:.1f}s** &nbsp; · &nbsp; "
        f"{in_tok + out_tok:,} tokens ({in_tok:,} in / {out_tok:,} out) &nbsp; · &nbsp; "
        f"**${cost:.4f}**"
    )


def render_parallel_tab():
    st.markdown(
        "Pick a random question from the 120-question eval dataset and run it through "
        "all three configurations side-by-side."
    )

    data = _load_dataset()
    if not data:
        st.warning(f"Dataset not found at `{DATASET_PATH}`.")
        return

    categories = sorted({q["category"] for q in data})
    top = st.columns([2, 1, 1])
    with top[0]:
        cat = st.selectbox("Category (optional)", ["(any)"] + categories, key="parallel_category")
    with top[1]:
        run = st.button("Run single question", type="primary", use_container_width=True)
    with top[2]:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state.pop("parallel_question", None)
        st.session_state.pop("parallel_results", None)
        st.rerun()

    if run:
        category = None if cat == "(any)" else cat
        question = _pick_question(category)
        if not question:
            st.error("No questions found for that category.")
            return
        st.session_state["parallel_question"] = question
        st.session_state.pop("parallel_results", None)

    question = st.session_state.get("parallel_question")
    if not question:
        st.info("Click **Run single question** to draw a random question and dispatch it to all three agents in parallel.")
        return

    with st.container(border=True):
        cols = st.columns([3, 1])
        cols[0].markdown(f"**Question ({question['id']}, _{question['category']}_, {question.get('difficulty','?')}):**")
        cols[0].markdown(f"> {question['question']}")
        meta_bits = []
        if question.get("regulations_involved"):
            meta_bits.append("Reg: " + ", ".join(question["regulations_involved"]))
        if question.get("sop_id"):
            meta_bits.append(f"SOP: {question['sop_id']}")
        if question.get("edition"):
            meta_bits.append(f"Edition: {question['edition']}")
        if question.get("expected_compliance_level"):
            meta_bits.append(f"GT: {question['expected_compliance_level']}")
        cols[1].caption(" · ".join(meta_bits) if meta_bits else "")
        with st.expander("Reference answer / expected citations", expanded=False):
            st.markdown(f"**Expected:** {question.get('expected_answer','')}")
            if question.get("expected_citations"):
                st.markdown("**Citations:**")
                for c in question["expected_citations"]:
                    st.markdown(f"- {c.get('regulation','')} {c.get('section','')}")

    # Build prompt — if the question references an SOP, ask the agent to read it.
    prompt = question["question"]
    if question.get("sop_id"):
        prompt = f"For {question['sop_id']}: {prompt}"

    st.markdown("---")
    results = _run_parallel(prompt, PARALLEL_AGENTS)
    st.session_state["parallel_results"] = results


def _judge_score(category: str, mode_data: dict, kind: str) -> str:
    """Format a per-category judge score cell."""
    per = mode_data.get("per_category", {}).get(category, {})
    if kind == "correctness":
        v = per.get("judge_correctness_avg")
    elif kind == "citations":
        v = per.get("judge_citations_avg")
    elif kind == "binary":
        v = per.get("binary_accuracy")
    else:
        v = None
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


def render_results_tab():
    if not RESULTS_PATH.exists():
        st.warning(f"No results file found at `{RESULTS_PATH}`.")
        return

    data = json.loads(RESULTS_PATH.read_text())
    naive = data.get("naive", {})
    nebius = data.get("agentic", {})
    openai_a = data.get("agentic-openai", {})

    st.markdown(
        "**120-question evaluation** of naive RAG vs the agentic stack on two models. "
        "Same dataset, same prompts, same retrieval primitive. The agentic configs differ only in the underlying chat model."
    )

    # Headline metrics
    st.markdown("### Headline metrics")
    cols = st.columns(3)
    for col, label, mode in zip(
        cols,
        ["Naive RAG (DeepSeek)", "Agentic (Nebius)", "Agentic (OpenAI)"],
        [naive, nebius, openai_a],
    ):
        with col:
            st.markdown(f"**{label}**")
            binmet = mode.get("compliance_binary", {})
            st.metric("Non-compliant recall", f"{binmet.get('recall_non_compliant', 0):.2f}")
            st.metric("Binary accuracy", f"{binmet.get('accuracy', 0):.2f}")
            st.metric("Total cost", f"${mode.get('total_cost_usd', 0):.2f}")
            st.metric("Avg latency / Q", f"{mode.get('latency_avg_s', 0):.1f}s")

    st.markdown("### Per-category correctness (LLM-as-judge, 0–2)")
    import pandas as pd
    categories = ["factual_single_hop", "multi_regulation", "edition_aware", "negation_gap", "web_grounded"]
    rows = []
    for cat in categories:
        n = naive.get("per_category", {}).get(cat, {}).get("n", "—")
        rows.append({
            "Category": cat,
            "n": n,
            "Naive": _judge_score(cat, naive, "correctness"),
            "Agentic (Nebius)": _judge_score(cat, nebius, "correctness"),
            "Agentic (OpenAI)": _judge_score(cat, openai_a, "correctness"),
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.markdown("### Per-category citation quality (LLM-as-judge, 0–2)")
    rows = []
    for cat in categories:
        n = naive.get("per_category", {}).get(cat, {}).get("n", "—")
        rows.append({
            "Category": cat,
            "n": n,
            "Naive": _judge_score(cat, naive, "citations"),
            "Agentic (Nebius)": _judge_score(cat, nebius, "citations"),
            "Agentic (OpenAI)": _judge_score(cat, openai_a, "citations"),
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.markdown("### SOP compliance — binary scoring")
    sop_rows = []
    for label, mode in [("naive", naive), ("agentic (Nebius)", nebius), ("agentic (OpenAI)", openai_a)]:
        b = mode.get("compliance_binary", {})
        sop_rows.append({
            "Mode": label,
            "Accuracy": f"{b.get('accuracy', 0):.3f}",
            "Non-compliant recall": f"{b.get('recall_non_compliant', 0):.3f}",
            "Non-compliant precision": f"{b.get('precision_non_compliant', 0):.3f}",
            "Compliant recall": f"{b.get('recall_compliant', 0):.3f}",
            "Macro F1": f"{b.get('macro_f1', 0):.3f}",
            "TP / FP / TN / FN": f"{b.get('tp_non_compliant',0)}/{b.get('fp_non_compliant',0)}/{b.get('tn_compliant',0)}/{b.get('fn_non_compliant',0)}",
        })
    st.dataframe(pd.DataFrame(sop_rows), hide_index=True, use_container_width=True)

    st.markdown("### Cost & latency")
    cost_rows = []
    for label, mode in [("naive", naive), ("agentic (Nebius)", nebius), ("agentic (OpenAI)", openai_a)]:
        cost_rows.append({
            "Mode": label,
            "Model": mode.get("model", ""),
            "Total cost": f"${mode.get('total_cost_usd', 0):.2f}",
            "Input tokens": f"{mode.get('input_tokens', 0):,}",
            "Output tokens": f"{mode.get('output_tokens', 0):,}",
            "Wall time (min)": f"{mode.get('latency_total_s', 0)/60:.1f}",
            "Avg/Q (s)": f"{mode.get('latency_avg_s', 0):.1f}",
        })
    st.dataframe(pd.DataFrame(cost_rows), hide_index=True, use_container_width=True)

    st.markdown("### Short summary")
    st.markdown(
        """
- **The agentic stack never misses a real compliance issue** (100% non-compliant recall, 0 catastrophic compliant↔gap errors) — regardless of underlying model.
- **Naive RAG misses 12% of real issues**, with 5 catastrophic compliant↔gap confusions.
- **Agentic dominates every freeform category** by 0.86–1.35 correctness points (out of 2). Citation quality is strictly higher.
- **Model choice is a cost-quality knob, not a capability boundary:** OpenAI cites better (+0.10 to +0.50) and is 30% faster, but costs 3.4× more. Nebius is slightly better on edition-aware and web-grounded.
- **Cost premium ≈ 8.7× (Nebius) or ≈ 30× (OpenAI) over naive RAG.** False alarms are recoverable; missed issues are not.
        """
    )

    with st.expander("Metric definitions", expanded=False):
        st.markdown(
            """
**LLM-as-judge metrics (freeform categories)**

A separate `ChatOpenAI` grader call (Nebius DeepSeek, shared across modes) scores each candidate 0–2 on two axes.

- **Correctness (0/1/2)** — `0` = wrong/missing; `1` = partially correct or vague; `2` = fully correct.
- **Citation quality (0/1/2)** — `0` = no specific citation; `1` = some citations but missing/wrong sections; `2` = cites the expected regulation(s) and section(s).

**SOP compliance — binary** — `partial` and `gap` collapse to `non_compliant`; `non_compliant` is the positive class.

- **Accuracy** — `(TP + TN) / total`.
- **Non-compliant recall** — `TP / (TP + FN)`. *Of all SOPs that are truly non-compliant, how many did we catch?* The audit-safety metric — 1.0 means zero missed issues.
- **Non-compliant precision** — `TP / (TP + FP)`. Inverse of the false-alarm rate.
- **Compliant recall** — `TN / (TN + FP)`. Of truly compliant SOPs, how many we cleared.
- **Macro F1** — `(F1_non_compliant + F1_compliant) / 2`.

**Cost / latency**

- **Total cost (USD)** — `(input × $in + output × $out) / 1M` using model-specific pricing. Sum across answer + judge calls.
- **Wall time** — total elapsed seconds with N workers concurrent.
- **Avg per question** — total wall time / question count.
            """
        )

    with st.expander("Category definitions", expanded=False):
        st.markdown(
            """
- **`factual_single_hop`** — direct retrieval of one regulation clause. *Sanity baseline: naive can do it.*
- **`multi_regulation`** — synthesis across two or more frameworks. *Naive fails — single retrieval misses cross-framework chunks.*
- **`edition_aware`** — distinguishing historical versions of the same regulation. *Naive conflates editions; agent uses metadata filter.*
- **`sop_compliance`** — structured compliance judgment (compliant/partial/gap) against `compliance_matrix.json`. *The demo's headline task.*
- **`web_grounded`** — questions requiring current information (enforcement actions, recent guidance). *Naive structurally fails — no web access.*
- **`negation_gap`** — identifying what's missing from an SOP. *Gap detection — the hardest, most valuable audit task.*
            """
        )


def main():
    st.markdown(NEBIUS_CSS, unsafe_allow_html=True)

    # Header: Nebius wordmark + page title
    header_cols = st.columns([1, 6])
    with header_cols[0]:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=120)
    with header_cols[1]:
        st.title("Sentinel Compliance Auditor")
        st.caption("AI-powered regulatory audit for HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF & more")

    chat_tab, parallel_tab, results_tab = st.tabs(
        ["Chat", "Run parallel test", "Test results"]
    )
    with chat_tab:
        render_chat_tab()
    with parallel_tab:
        render_parallel_tab()
    with results_tab:
        render_results_tab()


if __name__ == "__main__":
    main()
