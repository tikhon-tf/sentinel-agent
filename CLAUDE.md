# CLAUDE.md — Sentinel Agent

## What this project is

Sentinel is a regulatory compliance auditor agent that audits 200 synthetic SOPs for a fictional healthcare fintech (Meridian Health Technologies) against 9 regulation frameworks (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California SB 53/SB 942/AB 853). Regulation text is stored in a Pinecone knowledge base and retrieved dynamically during auditing. Built for the Nebius Blueprint for Agents demo (Nebius Inflection, June 9, 2026).

## Quick reference

```bash
make install              # Install into .venv (includes dev, deep, demo, rag, ui extras)
make ingest               # Ingest SOPs into Pinecone
make ingest-regulations   # Ingest regulation texts into Pinecone (namespace: regulations)
make act1                 # Act 1: Claude Sonnet 4.6 + Pinecone agentic RAG
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

### SOP-centric fan-out (not clause-centric)
Auditing fans out by SOP, not by clause. Each SOP is audited against all its relevant regulations in a single LLM call (`audit_sop()` in `sentinel/llm.py`). The LLM identifies applicable requirements from the retrieved regulation text and produces findings with specific regulatory citations. `audit_all_sops` in `tools.py` runs 200 SOPs through a 10-wide `ThreadPoolExecutor`. Do not revert to per-clause fan-out.

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
| `sentinel/graph/tools.py` | LangChain `@tool` definitions: `audit_all_sops`, `audit_single_sop`, `list_regulations`, `retrieve_regulation_text_tool` |
| `sentinel/llm.py` | Raw OpenAI client, `audit_sop()` (per-SOP against regulation text) |
| `sentinel/models.py` | Pydantic models (`AuditFinding`, `SOPChunk`), enums (`ComplianceLevel`, `Severity`) |
| `sentinel/config.py` | API keys, model names, paths, business unit list |
| `sentinel/retrieval/local.py` | File-based SOP retrieval + `list_all_sops()`, `load_sop_by_id()`, `load_sop_chunks()` |
| `sentinel/retrieval/regulations.py` | Pinecone regulation text retrieval: `retrieve_regulation_text()`, `retrieve_for_sop()`, `format_regulation_context()` |
| `sentinel/retrieval/ingest_regulations.py` | Regulation text chunker + Pinecone ingestion (`REGULATION_MAP`, `EDITION_PATTERNS`, edition metadata) |
| `sentinel/retrieval/ingest.py` | SOP markdown parser (`parse_sop()`), chunker, Pinecone ingestion |
| `sentinel/retrieval/nexus.py` | Pinecone Nexus retrieval |
| `sentinel/retrieval/vector_search.py` | Pinecone agentic RAG retrieval |
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

### SOPs
- 200 SOPs across 10 business units in `data/sops/` (markdown with YAML frontmatter)
- SOP frontmatter `regulations` field determines which regulations apply during audit
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

## Environment variables

Required: `NEBIUS_API_KEY`. Optional: `ANTHROPIC_API_KEY` (Act 1), `PINECONE_API_KEY` (vector modes), `TAVILY_API_KEY` (grounding), `LANGSMITH_API_KEY` (tracing + cloud auth), `SNOWGLOBE_API_KEY` (Act 3). See `.env.example`.

## Patterns to follow

- All LLM calls go through `sentinel/llm.py` (`get_client()` / `get_model()`)
- Tools in `sentinel/graph/tools.py` are decorated with `@tool` from `langchain_core.tools`
- Audit results are accumulated in the module-level `_audit_results` dict in `tools.py`
- SOP frontmatter `regulations` field determines which regulations to retrieve from Pinecone
- Regulation retrieval uses metadata filters (`regulation`, `edition`) on the `regulations` namespace
- The `list_regulations` tool queries Pinecone with per-regulation metadata filters (not a single semantic query) to ensure all regulation types are represented
- JSON parsing from LLM responses always strips markdown code fences and falls back to substring extraction
