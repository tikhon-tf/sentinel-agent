# Sentinel — Regulatory Compliance Auditor Agent

Sentinel is an AI-powered compliance auditor that assesses enterprise SOPs against SOC 2 Trust Services Criteria and the HIPAA Security Rule. Built for the [Nebius Blueprint for Agents](https://nebius.com/) project (Nebius Inflection, June 9, 2026).

It audits 200 SOPs across 25 regulation clauses, producing structured findings with compliance levels, severity ratings, evidence citations, and remediation recommendations.

## Architecture

```
User Query
    |
    v
+-------------------+
|  ReAct Agent      |  LangGraph (+ deepagents when available)
|  (DeepSeek-V4-Pro)|
+-------------------+
    |
    v
+-------------------+     +-------------------+
|  Retrieval        | --> |  Per-SOP Reasoner  |
|  Local / Pinecone |     |  (audit_sop)       |
+-------------------+     +-------------------+
    |                          |
    v                          v
  SOPs (200 docs)        Audit Findings (JSON/CSV)
```

**Model:** DeepSeek-V4-Pro on Nebius AI Studio (Act 2), Claude Sonnet 4.6 on Anthropic (Act 1)
**Orchestration:** LangGraph ReAct agent with optional deepagents upgrade
**Retrieval:** Local keyword matching, Pinecone vector search (Qwen3-Embedding-8B), or Pinecone Nexus
**Grounding:** Tavily live regulation search
**Observability:** LangSmith tracing
**Deployment:** LangGraph Cloud + Streamlit UI

## Three-Act Demo

| Act | Description | Model | Command |
|-----|-------------|-------|---------|
| **Act 1** | Agentic RAG prototype — shows where naive retrieval breaks | Claude Sonnet 4.6 | `make act1` |
| **Act 2** | Production stack with Nexus structured retrieval | DeepSeek-V4-Pro | `make act2` |
| **Act 3** | Snowglobe adversarial simulation — red-teams the auditor | DeepSeek-V4-Pro | `make act3` |

## Quickstart

### Prerequisites

- Python 3.11+
- API keys: Nebius, Anthropic (Act 1), Pinecone (optional), Tavily (optional), LangSmith (optional)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

### Run the demo

```bash
make act1    # Claude + Pinecone RAG — ~15 min
make act2    # DeepSeek + Pinecone Nexus — ~15 min
make act3    # Adversarial simulation — ~2 min
make demo    # All three acts sequentially
```

### Deploy

```bash
# Local development
make dev     # LangGraph dev server on port 2024
make ui      # Streamlit UI on port 8501

# Cloud deployment
make deploy  # Deploy to LangGraph Cloud
```

The cloud deployment URL is configurable in the Streamlit UI sidebar, or via:

```bash
LANGGRAPH_URL=http://localhost:2024 make ui-local
```

## Audit Approach

Sentinel fans out by SOP, not by clause. Each SOP is audited against all its relevant regulation clauses in a single LLM call, producing multiple findings at once. This gives:

- **Lower latency** — results stream back SOP-by-SOP
- **Fewer LLM calls** — 1 call per SOP instead of 1 per (clause, SOP) pair
- **10-wide parallelism** — via ThreadPoolExecutor

Key tools:
- `audit_all_clauses` — full audit across all 200 SOPs in parallel
- `audit_single_sop` — audit one SOP against all its relevant clauses
- `audit_single_clause` — targeted clause-level assessment
- `list_regulation_clauses` — list all 25 clauses

## Project Structure

```
sentinel_agent/
├── sentinel/                  # Core agent package
│   ├── config.py              # API keys, model config, paths
│   ├── models.py              # Pydantic models, regulation clauses (25 total)
│   ├── llm.py                 # Per-cell and per-SOP reasoners
│   ├── graph/
│   │   ├── agent.py           # ReAct agent (deepagents fallback to LangGraph)
│   │   └── tools.py           # LangChain tools for retrieval + auditing
│   ├── retrieval/
│   │   ├── local.py           # File-based keyword retrieval
│   │   ├── vector_search.py   # Pinecone agentic RAG (Act 1)
│   │   ├── nexus.py           # Pinecone Nexus one-shot (Act 2)
│   │   └── ingest.py          # SOP -> Pinecone ingestion
│   ├── grounding/
│   │   └── tavily_search.py   # Live regulation grounding
│   ├── simulation/
│   │   └── snowglobe.py       # Adversarial scenarios (Act 3)
│   └── output/
│       ├── heatmap.py         # Rich console heatmap + summary
│       └── register.py        # CSV/JSON/metrics output
├── demo/
│   ├── act1_prototype.py      # Act 1: Claude + RAG
│   ├── act2_production.py     # Act 2: DeepSeek + Nexus
│   └── act3_simulation.py     # Act 3: Adversarial
├── ui/
│   └── app.py                 # Streamlit chat UI with streaming
├── data/
│   ├── sops/                  # 200 generated SOPs (10 business units)
│   ├── company_profile.md     # Meridian Health Technologies background
│   └── compliance_matrix.json # Ground truth
├── langgraph.json             # LangGraph deployment config
├── pyproject.toml             # Dependencies
├── Makefile                   # Build/run targets
└── .env.example               # API key template
```

## Company Profile

**Meridian Health Technologies** is a fictional AI-powered healthcare fintech that:
- Provides AI-driven clinical decision support and diagnostic tools
- Operates healthcare payment processing, lending, and fraud detection
- Manages patient data across EU and US jurisdictions
- Deploys ML models for credit scoring and risk assessment

## Regulation Coverage

**SOC 2 Trust Services Criteria (9 clauses)**
CC1 Control Environment through CC9 Risk Mitigation

**HIPAA Security Rule (16 clauses)**
- Administrative Safeguards: Security Management, Assigned Responsibility, Workforce Security, Information Access, Training, Incidents, Contingency, Evaluation
- Physical Safeguards: Facility Access, Workstation Security, Device/Media Controls
- Technical Safeguards: Access Control, Audit Controls, Integrity, Authentication, Transmission Security

## SOP Dataset

200 SOPs across 10 business units with deliberately varied compliance levels:
- ~40% Compliant (thorough, specific, cites regulation articles)
- ~35% Partial (vague language, incomplete controls)
- ~25% Gap (missing key requirements, weak controls)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEBIUS_API_KEY` | Yes | Nebius AI Studio API key |
| `ANTHROPIC_API_KEY` | For Act 1 | Anthropic API key (Claude) |
| `PINECONE_API_KEY` | For Pinecone modes | Pinecone vector DB key |
| `TAVILY_API_KEY` | Optional | Live regulation grounding |
| `LANGSMITH_API_KEY` | Optional | LangSmith tracing + cloud auth |
| `SNOWGLOBE_API_KEY` | Optional | Adversarial simulation |
| `RETRIEVAL_MODE` | Optional | Default retrieval: `nexus`, `rag`, or `local` |
| `LANGGRAPH_URL` | Optional | Override UI backend URL |

## Cost

- Full audit (Act 2, DeepSeek-V4-Pro on Nebius): ~$0.30
- Full audit (Act 1, Claude Sonnet 4.6): ~$3.00
- Act 3 simulation: ~$0.01
- SOP ingestion (5,522 embeddings): ~$0.02
