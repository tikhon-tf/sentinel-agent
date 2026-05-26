# CLAUDE.md — Sentinel Agent

## What this project is

Sentinel is a regulatory compliance auditor agent that audits 200 synthetic SOPs for a fictional healthcare fintech (Meridian Health Technologies) against 9 regulation frameworks (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California SB 53/SB 942/AB 853). Act 1 retrieves regulation text from a Pinecone vector index via agentic RAG; Act 2 retrieves from Pinecone Nexus KnowQL (grounded, cited answers in one shot). Built for the Nebius Blueprint for Agents demo (Nebius Inflection, June 9, 2026).

## Quick reference

```bash
make install              # Install into .venv (includes dev, deep, demo, rag, ui extras)
make ingest               # Ingest SOPs into Pinecone
make ingest-regulations   # Ingest regulation texts into Pinecone (namespace: regulations)
make act1                 # Act 1: GPT-5.5 + Pinecone agentic RAG
make act2                 # Act 2: DeepSeek-V4-Pro + Nexus KnowQL one-shot
make act3                 # Act 3: Snowglobe adversarial simulation
make act4                 # Act 4: actuation — file Jira tickets for compliance gaps
make demo                 # All four acts sequentially
make test                 # Run regression tests (111 tests, no API keys needed)
make dev                  # LangGraph dev server on port 2024
make ui                   # Streamlit UI on port 8501
make deploy               # Deploy to LangGraph Cloud (remote Docker build)
```

## Architecture decisions

### Regulation knowledge base (not hardcoded clauses)
Regulation texts live in `data/regulations/` as `.txt` and `.md` files. Two retrieval backends are supported:

**Pinecone RAG (Act 1):** Regulation texts are chunked, embedded (Qwen3-Embedding-8B on Nebius, 4096 dimensions), and stored in Pinecone namespace `regulations`. Sub-agents retrieve raw text chunks via semantic search with metadata filtering by regulation name. Multiple retrieval calls per regulation, per SOP.

**Nexus KnowQL (Act 2):** The same regulation corpus is pre-loaded into a Pinecone Nexus context (`sentinel-regs-test`, 50 source documents). Sub-agents query the Nexus `/knowql` endpoint with natural-language questions and receive grounded, cited answers in one shot. Nexus handles retrieval, synthesis, and citation internally — no embedding or chunk management needed on our side. Auth is JWT-based (exchange `NEXUS_API_KEY` for a short-lived token, cached ~30 days). The Nexus corpus is a superset of the Pinecone index — it also includes NIST SP 800-series, OWASP, FDA/21 CFR, PCI DSS, and EU directives.

Key modules:
- `sentinel/retrieval/nexus.py` — Nexus KnowQL client: JWT auth with thread-safe caching, `query_nexus()`, retry on 401/429/409, `format_nexus_response()`
- `sentinel/retrieval/regulations.py` — Pinecone regulation text retrieval (Act 1): `retrieve_regulation_text()`, `retrieve_for_sop()`, `format_regulation_context()`
- `sentinel/retrieval/ingest_regulations.py` — chunks .txt/.md files, embeds, upserts into Pinecone
- `scripts/extract_pdf_text.py` — extracts text from regulation PDFs (pymupdf) for ingestion

### Sub-agent architecture (not single-shot LLM calls)
Each SOP is audited by a dedicated ReAct sub-agent (`audit_single_sop` in `tools.py`) built with `langchain.agents.create_agent`. The sub-agent has its own tool loop with access to a regulation knowledge base, Tavily (web search), and the SOP text. It determines which regulations apply based on the SOP's content and business unit, queries the knowledge base for each applicable regulation, then outputs structured JSON findings. `audit_all_sops` fans out 200 sub-agents through a `ThreadPoolExecutor` (configurable via `MAX_AUDIT_WORKERS`, default 200). Do not revert to single-shot LLM calls.

Sub-agent tools (built per-invocation in `_build_subagent_tools(use_nexus=...)`):
- `retrieve_regulation_rag` (Act 1, `use_nexus=False`) — semantic search on Pinecone `regulations` namespace with optional regulation filter
- `retrieve_regulation_nexus` (Act 2, `use_nexus=True`) — Nexus KnowQL natural-language query returning grounded, cited answers
- `search_web` — Tavily advanced search for latest guidance/enforcement
- `read_sop` — returns the full SOP text (closure over the loaded content)

The sub-agent system prompt is also selected based on `use_nexus`: `_AUDIT_SUBAGENT_PROMPT_RAG` (keyword-style queries, multiple retrieval calls) vs `_AUDIT_SUBAGENT_PROMPT_NEXUS` (natural-language questions, structural locators, cross-framework synthesis, awareness of the 50-doc Nexus corpus).

### Dual-model, dual-retrieval support
- **Act 1**: GPT-5.4-mini via OpenAI API (`https://api.openai.com/v1`) + Pinecone RAG
- **Act 2 + deployment default**: DeepSeek on Nebius AI Studio (`https://api.studio.nebius.com/v1/`) + Nexus KnowQL
- Provider switching is handled by `set_provider()` in `llm.py` and `_build_model()` in `agent.py`
- Retrieval backend is selected by the `use_nexus` flag threaded through `build_tools()` → `_audit_single_sop_impl()` → `_build_subagent_tools()`
- The agent graph (`sentinel/graph/agent.py:agent`) always uses Nebius (DeepSeek) + Nexus — that's the deployed default

### deepagents optional dependency
`deepagents` is an optional dep (`[deep]` extra). It's lazy-imported in `agent.py` inside `_build_deep_agent()`. If the import fails, we fall back to `langchain.agents.create_agent`. This is required because deepagents pulls heavy transitive deps (grpcio, google-genai) that conflict with LangGraph Cloud's constraint file.

### Jira actuation (Act 4)
When an audit finding is a gap or partial at medium+ severity, the `create_jira_ticket` tool files a ticket on the team's Kanban board. The tool is available to the outer Sentinel agent alongside the audit tools. The Jira client (`sentinel/actuation/jira_client.py`) uses the REST API v3 with basic auth (email + API token). Ticket description is rendered in Atlassian Document Format (ADF). Labels include `sentinel`, `compliance-finding`, severity, regulation slug, and SOP slug. Configuration via `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`, and optionally `JIRA_DEFAULT_ISSUE_TYPE` (default: Task).

`demo/act4_actuation.py` runs two hardcoded audit cases (HIPAA access control, GDPR breach notification) — calls the model directly (not through the agent graph), parses the JSON finding, and invokes `create_jira_ticket` for ticketable findings.

### Lazy imports for cloud compatibility
`tavily` (in sub-agent tools in `tools.py`), `pinecone` (in `retrieval/ingest.py`, `retrieval/regulations.py`, `tools.py`), `openai` (in `retrieval/ingest.py`), and `httpx` (in `actuation/jira_client.py`, `retrieval/nexus.py`) are imported lazily inside functions, not at module level. This prevents import failures in the LangGraph Cloud container where these packages may not be installed or configured. Do not move these to top-level imports.

## Key modules

| Module | Purpose |
|--------|---------|
| `sentinel/graph/agent.py` | ReAct agent definition, `build_agent()`, `run_audit()` entry point |
| `sentinel/graph/tools.py` | LangChain `@tool` definitions: `audit_single_sop` (sub-agent), `audit_all_sops`, `list_sops`, `list_regulations`, `retrieve_regulation_text_tool`, `create_jira_ticket`; sub-agent builder `_build_subagent_tools(use_nexus=...)`; dual prompts `_AUDIT_SUBAGENT_PROMPT_RAG` / `_AUDIT_SUBAGENT_PROMPT_NEXUS` |
| `sentinel/llm.py` | OpenAI client provider switching (`set_provider()`, `get_client()`, `get_model()`) |
| `sentinel/models.py` | Pydantic models (`AuditFinding`, `SOPChunk`, `AuditMetrics`), enums (`ComplianceLevel`, `Severity`) |
| `sentinel/config.py` | API keys, model names, paths, pricing, business unit list |
| `sentinel/retrieval/local.py` | SOP loading: `list_all_sops()`, `load_sop_by_id()`, `load_sop_chunks()` |
| `sentinel/retrieval/nexus.py` | Nexus KnowQL client (Act 2): `query_nexus()`, `format_nexus_response()`, JWT auth with thread-safe caching, 401/429/409 retry |
| `sentinel/retrieval/regulations.py` | Pinecone regulation text retrieval (Act 1): `retrieve_regulation_text()`, `retrieve_for_sop()`, `format_regulation_context()` |
| `sentinel/retrieval/ingest_regulations.py` | Regulation text chunker + Pinecone ingestion (`REGULATION_MAP`, `EDITION_PATTERNS`, edition metadata) |
| `sentinel/retrieval/ingest.py` | SOP markdown parser (`parse_sop()`), chunker, Pinecone ingestion |
| `sentinel/simulation/snowglobe.py` | Adversarial red-team scenarios (Act 3) |
| `sentinel/actuation/jira_client.py` | Sync Jira Cloud REST client used by the `create_jira_ticket` tool (Act 4) |
| `sentinel/output/heatmap.py` | Rich console heatmap rendering |
| `sentinel/output/register.py` | CSV/JSON/metrics output |
| `ui/app.py` | Streamlit chat UI with streaming, per-response and session token/cost tracking |
| `scripts/validate_run.py` | Audit quality evaluation: compares LangSmith run output against compliance matrix |
| `demo/act{1,2,3,4}_*.py` | Four-act demo scripts |

## LangGraph Cloud deployment

- Config: `langgraph.json` — points to `sentinel/graph/agent.py:agent` as the graph entry
- Uses Python 3.12, Wolfi Linux image, reads `.env` for secrets
- Cloud URL: `https://sentinel-agent-c4dfa65772015432b388f980262380a8.us.langgraph.app`
- The `.dockerignore` excludes `demo/`, `scripts/`, `ui/`, `tests/` from the cloud image
- `setuptools` is configured with `include = ["sentinel*"]` in `pyproject.toml` to avoid packaging `demo/` and `scripts/` as top-level packages

## Data

### Quality evaluation
- `scripts/validate_run.py` fetches audit run data from LangSmith and compares against the compliance matrix
- Takes LangSmith run IDs as arguments — fetches run metadata (model, timing, tokens, cost) and audit content automatically
- Parses the `audit_all_sops` text output, classifies findings by regulation (criterion prefix matching), aggregates to worst compliance level per (SOP, regulation) pair
- Metrics: matched %, false positive % (too strict), false negative % (too lenient), failed % (missing), per-class F1, macro F1, per-regulation accuracy, directional bias, tokens, cost, latency
- Usage: `python3 scripts/validate_run.py <run_id>` (single run), `python3 scripts/validate_run.py <run_id1> <run_id2>` (side-by-side comparison), `--original` flag for original matrix
- Content extraction: tries `audit_all_sops` tool run output first, then root run outputs, then Prompt chain runs (for pending runs with null outputs)
- `data/compliance_matrix_revised.json` is a corrected copy with 16 SOC 2 level changes (15 gap→partial, 1 partial→compliant) based on manual SOP-vs-regulation review

### SOPs
- 200 SOPs across 10 business units in `data/sops/` (markdown with YAML frontmatter)
- SOP frontmatter `regulations` field is informational — the sub-agent determines applicable regulations dynamically
- 152 of 200 SOPs are tagged with SOC 2 or HIPAA (the rest cover EU AI Act, GDPR, etc.)
- Compliance matrix ground truth: `data/compliance_matrix.json`
- SOP generation scripts in `scripts/` (one-time use, not part of the agent)

### Regulations
- 9 regulation frameworks in `data/regulations/` as .txt, .md, .pdf, and .xml files
- 2,386 chunks ingested into Pinecone namespace `regulations` (from 22 .txt/.md source files)
- Historical editions: HIPAA (2017, 2020, 2024, current), NIST AI RMF (2022 drafts, final), EU AI Act (2021 proposal, final), SR 11-7 (2011 original, 2026 revised)
- Each chunk carries `regulation`, `edition`, `section`, and `source` metadata for filtered retrieval
- PDFs are extracted to .txt via `scripts/extract_pdf_text.py` (pymupdf) before ingestion
- See `data/regulations/README.md` for full file inventory and sources

## Integrations

### LangSmith MCP
Remote MCP server configured in `.mcp.json` (`https://api.smith.langchain.com/mcp`). Uses OAuth — authenticate via browser on first use. Provides access to LangSmith traces, runs, datasets, experiments, and prompt hub from Claude Code and Codex. Key tools: `fetch_runs` (inspect audit traces), `list_projects`, `list_datasets`, `run_experiment`, `get_billing_usage`.

### Jira Cloud (Act 4)
The `create_jira_ticket` tool files compliance findings as tickets via the Jira Cloud REST API v3. Client: `sentinel/actuation/jira_client.py` (sync, basic auth). Ticket descriptions use Atlassian Document Format (ADF). Labels: `sentinel`, `compliance-finding`, severity, regulation slug, SOP slug. Priority mapped from severity (critical→Highest, high→High, medium→Medium, low→Low). Config: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`.

## Environment variables

Required: `NEBIUS_API_KEY`. Optional: `OPENAI_API_KEY` (Act 1), `PINECONE_API_KEY` (Act 1 Pinecone RAG), `NEXUS_API_KEY` (Act 2 Nexus KnowQL), `TAVILY_API_KEY` (grounding), `LANGSMITH_API_KEY` (tracing + cloud auth), `SNOWGLOBE_API_KEY` (Act 3), `JIRA_BASE_URL` / `JIRA_EMAIL` / `JIRA_API_TOKEN` / `JIRA_PROJECT_KEY` (Act 4). `NEXUS_BASE_URL` and `NEXUS_CONTEXT_SLUG` can be overridden but default to the production Nexus endpoint. See `.env.example`.

## Patterns to follow

- The outer agent (Sentinel) uses `langchain_openai.ChatOpenAI` via `_build_model()` in `agent.py`
- Sub-agents (`audit_single_sop`) also use `ChatOpenAI` directly — they do NOT go through `llm.py`
- Tools in `sentinel/graph/tools.py` are decorated with `@tool` from `langchain_core.tools`
- Audit results are accumulated in the module-level `_audit_results` dict in `tools.py`
- SOP lookup (`load_sop_by_id`) supports exact ID, exact title, and fuzzy substring matching
- The sub-agent determines which regulations apply — there is no predefined SOP-to-regulation mapping
- Act 1 regulation retrieval uses metadata filters (`regulation`, `edition`) on the Pinecone `regulations` namespace; Act 2 uses Nexus KnowQL (`query_nexus()` in `retrieval/nexus.py`)
- When `use_nexus=True`, `list_regulations` returns a static corpus inventory (no API call); `retrieve_regulation_text_tool` calls Nexus; sub-agent gets `retrieve_regulation_nexus`. When `use_nexus=False`, both use Pinecone
- Nexus JWT is cached in a module-level `_token` with `threading.Lock` for thread safety across concurrent sub-agents; re-login on 401, backoff on 429 (honors `retry_after_seconds`) and 409 (exponential backoff)
- JSON parsing from sub-agent responses scans messages in reverse, strips markdown code fences, repairs truncated arrays, and maps unexpected enum values (`_COMPLIANCE_LEVEL_MAP`, `_SEVERITY_MAP`)
- All `ChatOpenAI` instances must set `stream_usage=True` — without it, custom `base_url` providers (Nebius, OpenAI) don't send `stream_options: {include_usage: true}` and `usage_metadata` is always `None` in thread state
- Token pricing is centralized in `PRICING` dict in `config.py` — the UI reads it for cost display
- Sub-agent token usage is tracked in `_audit_results` and included in tool result strings as `Sub-agent tokens: X (X in / X out)` — the UI parses this to include sub-agent costs in the displayed totals
- The LangGraph SDK (via `messages-tuple` stream mode) serializes messages with short-form types: `"ai"` / `"AIMessageChunk"` for AI messages, `"tool"` for ToolMessages, `"human"` for user messages. Do not use substring matching (e.g. `"ToolMessage" in msg_type`) — use explicit set membership (`msg_type in ("tool", "ToolMessage", "ToolMessageChunk")`)
