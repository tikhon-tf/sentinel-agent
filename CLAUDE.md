# CLAUDE.md — Sentinel Agent

## What this project is

Sentinel is a regulatory compliance auditor agent that audits 200 synthetic SOPs for a fictional healthcare fintech (Meridian Health Technologies) against SOC 2 Trust Services Criteria (CC1-CC9) and HIPAA Security Rule (16 safeguards). Built for the Nebius Blueprint for Agents demo (Nebius Inflection, June 9, 2026).

## Quick reference

```bash
make install          # Install into .venv (includes dev, deep, demo, rag, ui extras)
make act1             # Act 1: Claude Sonnet 4.6 + Pinecone agentic RAG
make act2             # Act 2: DeepSeek-V4-Pro + Pinecone Nexus one-shot
make act3             # Act 3: Snowglobe adversarial simulation
make demo             # All three acts sequentially
make dev              # LangGraph dev server on port 2024
make ui               # Streamlit UI on port 8501
make deploy           # Deploy to LangGraph Cloud (remote Docker build)
```

## Architecture decisions

### SOP-centric fan-out (not clause-centric)
Auditing fans out by SOP, not by clause. Each SOP is audited against all its relevant regulation clauses in a single LLM call (`audit_sop()` in `sentinel/llm.py`). This produces multiple findings per call. `audit_all_clauses` in `tools.py` runs 200 SOPs through a 10-wide `ThreadPoolExecutor`. Do not revert to per-clause fan-out.

### Dual-model support
- **Act 1**: Claude Sonnet 4.6 via Anthropic's OpenAI-compatible endpoint (`https://api.anthropic.com/v1/`)
- **Act 2 + deployment default**: DeepSeek-V4-Pro on Nebius AI Studio (`https://api.studio.nebius.com/v1/`)
- Provider switching is handled by `set_provider()` in `llm.py` and `_build_model()` in `agent.py`
- The agent graph (`sentinel/graph/agent.py:agent`) always uses Nebius (DeepSeek) — that's the deployed default

### deepagents optional dependency
`deepagents` is an optional dep (`[deep]` extra). It's lazy-imported in `agent.py` inside `_build_deep_agent()`. If the import fails, we fall back to `langgraph.prebuilt.create_react_agent`. This is required because deepagents pulls heavy transitive deps (grpcio, google-genai) that conflict with LangGraph Cloud's constraint file.

### Lazy imports for cloud compatibility
`tavily` (in `grounding/tavily_search.py`) and `pinecone`/`openai` (in `retrieval/ingest.py`) are imported lazily inside functions, not at module level. This prevents import failures in the LangGraph Cloud container where these packages may not be installed or configured. Do not move these to top-level imports.

### Retrieval modes
Three modes controlled by `RETRIEVAL_MODE` env var (default: `nexus`):
- `local` — keyword matching against local markdown files in `data/sops/`
- `rag` — Pinecone agentic RAG with query expansion (Act 1)
- `nexus` — Pinecone Nexus one-shot structured retrieval (Act 2)

## Key modules

| Module | Purpose |
|--------|---------|
| `sentinel/graph/agent.py` | ReAct agent definition, `build_agent()`, `run_audit()` entry point |
| `sentinel/graph/tools.py` | LangChain `@tool` definitions: `audit_all_clauses`, `audit_single_sop`, `audit_single_clause`, `retrieve_sops_for_clause`, `list_regulation_clauses` |
| `sentinel/llm.py` | Raw OpenAI client, `audit_cell()` (per-clause), `audit_sop()` (per-SOP multi-clause) |
| `sentinel/models.py` | Pydantic models (`AuditFinding`, `SOPChunk`, `RegulationClause`), all 25 clause definitions |
| `sentinel/config.py` | API keys, model names, paths, business unit list |
| `sentinel/retrieval/local.py` | File-based retrieval + `list_all_sops()`, `load_sop_by_id()`, `load_sop_chunks()` |
| `sentinel/retrieval/nexus.py` | Pinecone Nexus retrieval |
| `sentinel/retrieval/vector_search.py` | Pinecone agentic RAG retrieval |
| `sentinel/retrieval/ingest.py` | SOP markdown parser (`parse_sop()`), chunker, Pinecone ingestion |
| `sentinel/grounding/tavily_search.py` | Live regulation search via Tavily |
| `sentinel/simulation/snowglobe.py` | Adversarial red-team scenarios (Act 3) |
| `sentinel/output/heatmap.py` | Rich console heatmap rendering |
| `sentinel/output/register.py` | CSV/JSON/metrics output |
| `ui/app.py` | Streamlit chat UI with streaming via langgraph_sdk |
| `demo/act{1,2,3}_*.py` | Three-act demo scripts |

## LangGraph Cloud deployment

- Config: `langgraph.json` — points to `sentinel/graph/agent.py:agent` as the graph entry
- Uses Python 3.12, Wolfi Linux image, reads `.env` for secrets
- Cloud URL: `https://sentinel-agent-c4dfa65772015432b388f980262380a8.us.langgraph.app`
- The `.dockerignore` excludes `demo/`, `scripts/`, `ui/`, `tests/` from the cloud image
- `setuptools` is configured with `include = ["sentinel*"]` in `pyproject.toml` to avoid packaging `demo/` and `scripts/` as top-level packages

## Data

- 200 SOPs across 10 business units in `data/sops/` (markdown with YAML frontmatter)
- 25 regulation clauses: 9 SOC 2 (CC1-CC9) + 16 HIPAA Security Rule
- 152 of 200 SOPs are tagged with SOC 2 or HIPAA (the rest cover EU AI Act, GDPR, etc.)
- Compliance matrix ground truth: `data/compliance_matrix.json`
- SOP generation scripts in `scripts/` (one-time use, not part of the agent)

## Environment variables

Required: `NEBIUS_API_KEY`. Optional: `ANTHROPIC_API_KEY` (Act 1), `PINECONE_API_KEY` (vector modes), `TAVILY_API_KEY` (grounding), `LANGSMITH_API_KEY` (tracing + cloud auth), `SNOWGLOBE_API_KEY` (Act 3). See `.env.example`.

## Patterns to follow

- All LLM calls go through `sentinel/llm.py` (`get_client()` / `get_model()`)
- Tools in `sentinel/graph/tools.py` are decorated with `@tool` from `langchain_core.tools`
- Audit results are accumulated in the module-level `_audit_results` dict in `tools.py`
- SOP frontmatter `regulations` field determines which clauses apply via `_clauses_for_sop()`
- JSON parsing from LLM responses always strips markdown code fences and falls back to substring extraction
