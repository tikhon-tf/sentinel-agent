# CLAUDE.md — Sentinel Agent

## What this project is

Sentinel is a regulatory compliance auditor agent that audits 200 synthetic SOPs for a fictional healthcare fintech (Meridian Health Technologies) against 9 regulation frameworks (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California SB 53/SB 942/AB 853). Regulation text is stored in a Pinecone knowledge base and retrieved dynamically during auditing. Built for the Nebius Blueprint for Agents demo (Nebius Inflection, June 9, 2026).

## Quick reference

```bash
make install              # Install into .venv (includes dev, deep, demo, rag, ui extras)
make ingest               # Ingest SOPs into Pinecone
make ingest-regulations   # Ingest regulation texts into Pinecone (namespace: regulations)
make act1                 # Act 1: Claude Opus 4.7 + Pinecone agentic RAG
make act2                 # Act 2: DeepSeek-V4-Pro + Pinecone Nexus one-shot
make act3                 # Act 3: Snowglobe adversarial simulation
make demo                 # All three acts sequentially
make dev                  # LangGraph dev server on port 2024
make ui                   # Streamlit UI on port 8501
make deploy               # Deploy to LangGraph Cloud (remote Docker build)
```

## Architecture decisions

### Regulation knowledge base (not hardcoded clauses)
Regulation texts live in `data/regulations/` as `.txt` and `.md` files. They are chunked, embedded (Qwen3-Embedding-8B on Nebius, 4096 dimensions), and stored in Pinecone namespace `regulations`. During auditing, relevant regulation text is retrieved per-SOP via semantic search with metadata filtering by regulation name. This replaced an earlier system of 25 hardcoded `RegulationClause` objects.

Key modules:
- `sentinel/retrieval/ingest_regulations.py` — chunks .txt/.md files, embeds, upserts into Pinecone
- `sentinel/retrieval/regulations.py` — retrieves regulation text from Pinecone for a given SOP
- `scripts/extract_pdf_text.py` — extracts text from regulation PDFs (pymupdf) for ingestion

### Sub-agent architecture (not single-shot LLM calls)
Each SOP is audited by a dedicated LangGraph ReAct sub-agent (`audit_single_sop` in `tools.py`). The sub-agent has its own tool loop with access to Pinecone (regulation retrieval), Tavily (web search), and the SOP text. It determines which regulations apply based on the SOP's content and business unit, iteratively queries the knowledge base for each applicable regulation, then outputs structured JSON findings. `audit_all_sops` fans out 200 sub-agents through a 10-wide `ThreadPoolExecutor`. Do not revert to single-shot LLM calls.

Sub-agent tools (built per-invocation in `_build_subagent_tools()`):
- `retrieve_regulation` — semantic search on Pinecone `regulations` namespace with optional regulation filter
- `search_web` — Tavily advanced search for latest guidance/enforcement
- `read_sop` — returns the full SOP text (closure over the loaded content)

### Dual-model support
- **Act 1**: Claude Opus 4.7 via Anthropic's OpenAI-compatible endpoint (`https://api.anthropic.com/v1/`)
- **Act 2 + deployment default**: DeepSeek-V4-Pro on Nebius AI Studio (`https://api.studio.nebius.com/v1/`)
- Provider switching is handled by `set_provider()` in `llm.py` and `_build_model()` in `agent.py`
- The agent graph (`sentinel/graph/agent.py:agent`) always uses Nebius (DeepSeek) — that's the deployed default

### deepagents optional dependency
`deepagents` is an optional dep (`[deep]` extra). It's lazy-imported in `agent.py` inside `_build_deep_agent()`. If the import fails, we fall back to `langgraph.prebuilt.create_react_agent`. This is required because deepagents pulls heavy transitive deps (grpcio, google-genai) that conflict with LangGraph Cloud's constraint file.

### Lazy imports for cloud compatibility
`tavily` (in sub-agent tools in `tools.py`), `pinecone` (in `retrieval/ingest.py`, `retrieval/regulations.py`, `tools.py`), and `openai` (in `retrieval/ingest.py`) are imported lazily inside functions, not at module level. This prevents import failures in the LangGraph Cloud container where these packages may not be installed or configured. Do not move these to top-level imports.

## Key modules

| Module | Purpose |
|--------|---------|
| `sentinel/graph/agent.py` | ReAct agent definition, `build_agent()`, `run_audit()` entry point |
| `sentinel/graph/tools.py` | LangChain `@tool` definitions: `audit_single_sop` (sub-agent), `audit_all_sops`, `list_sops`, `list_regulations`, `retrieve_regulation_text_tool`; sub-agent builder `_build_subagent_tools()` |
| `sentinel/llm.py` | OpenAI client provider switching (`set_provider()`, `get_client()`, `get_model()`) |
| `sentinel/models.py` | Pydantic models (`AuditFinding`, `SOPChunk`, `AuditMetrics`), enums (`ComplianceLevel`, `Severity`) |
| `sentinel/config.py` | API keys, model names, paths, pricing, business unit list |
| `sentinel/retrieval/local.py` | SOP loading: `list_all_sops()`, `load_sop_by_id()`, `load_sop_chunks()` |
| `sentinel/retrieval/regulations.py` | Pinecone regulation text retrieval: `retrieve_regulation_text()`, `retrieve_for_sop()`, `format_regulation_context()` |
| `sentinel/retrieval/ingest_regulations.py` | Regulation text chunker + Pinecone ingestion (`REGULATION_MAP`, `EDITION_PATTERNS`, edition metadata) |
| `sentinel/retrieval/ingest.py` | SOP markdown parser (`parse_sop()`), chunker, Pinecone ingestion |
| `sentinel/simulation/snowglobe.py` | Adversarial red-team scenarios (Act 3) |
| `sentinel/output/heatmap.py` | Rich console heatmap rendering |
| `sentinel/output/register.py` | CSV/JSON/metrics output |
| `ui/app.py` | Streamlit chat UI with streaming, per-response and session token/cost tracking |
| `demo/act{1,2,3}_*.py` | Three-act demo scripts |

## LangGraph Cloud deployment

- Config: `langgraph.json` — points to `sentinel/graph/agent.py:agent` as the graph entry
- Uses Python 3.12, Wolfi Linux image, reads `.env` for secrets
- Cloud URL: `https://sentinel-agent-c4dfa65772015432b388f980262380a8.us.langgraph.app`
- The `.dockerignore` excludes `demo/`, `scripts/`, `ui/`, `tests/` from the cloud image
- `setuptools` is configured with `include = ["sentinel*"]` in `pyproject.toml` to avoid packaging `demo/` and `scripts/` as top-level packages

## Data

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

## MCP integrations

- **LangSmith**: Remote MCP server configured in `.mcp.json` (`https://api.smith.langchain.com/mcp`). Uses OAuth — authenticate via browser on first use. Provides access to LangSmith traces, runs, and datasets from Claude Code.

## Environment variables

Required: `NEBIUS_API_KEY`. Optional: `ANTHROPIC_API_KEY` (Act 1), `PINECONE_API_KEY` (vector modes), `TAVILY_API_KEY` (grounding), `LANGSMITH_API_KEY` (tracing + cloud auth), `SNOWGLOBE_API_KEY` (Act 3). See `.env.example`.

## Patterns to follow

- The outer agent (Sentinel) uses `langchain_openai.ChatOpenAI` via `_build_model()` in `agent.py`
- Sub-agents (`audit_single_sop`) also use `ChatOpenAI` directly — they do NOT go through `llm.py`
- Tools in `sentinel/graph/tools.py` are decorated with `@tool` from `langchain_core.tools`
- Audit results are accumulated in the module-level `_audit_results` dict in `tools.py`
- SOP lookup (`load_sop_by_id`) supports exact ID, exact title, and fuzzy substring matching
- The sub-agent determines which regulations apply — there is no predefined SOP-to-regulation mapping
- Regulation retrieval uses metadata filters (`regulation`, `edition`) on the Pinecone `regulations` namespace
- The `list_regulations` tool queries Pinecone with per-regulation metadata filters (not a single semantic query) to ensure all regulation types are represented
- JSON parsing from sub-agent responses scans messages in reverse, strips markdown code fences, repairs truncated arrays, and maps unexpected enum values (`_COMPLIANCE_LEVEL_MAP`, `_SEVERITY_MAP`)
- All `ChatOpenAI` instances must set `stream_usage=True` — without it, custom `base_url` providers (Nebius, Anthropic) don't send `stream_options: {include_usage: true}` and `usage_metadata` is always `None` in thread state
- Token pricing is centralized in `PRICING` dict in `config.py` — the UI reads it for cost display
- Sub-agent token usage is tracked in `_audit_results` and included in tool result strings as `Sub-agent tokens: X (X in / X out)` — the UI parses this to include sub-agent costs in the displayed totals
- The LangGraph SDK (via `messages-tuple` stream mode) serializes messages with short-form types: `"ai"` / `"AIMessageChunk"` for AI messages, `"tool"` for ToolMessages, `"human"` for user messages. Do not use substring matching (e.g. `"ToolMessage" in msg_type`) — use explicit set membership (`msg_type in ("tool", "ToolMessage", "ToolMessageChunk")`)
