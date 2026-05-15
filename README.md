# Sentinel — Regulatory Compliance Auditor Agent

Sentinel is an AI-powered compliance auditor that assesses enterprise SOPs against SOC 2 Trust Services Criteria and the HIPAA Security Rule. Built for the [Nebius Blueprint for Agents](https://nebius.com/) project.

It audits 200 SOPs across 25 regulation clauses, producing structured findings with compliance levels, severity ratings, evidence citations, and remediation recommendations.

## Architecture

```
User Query
    |
    v
+-------------------+
|  Deep Agent       |  deepagents + LangGraph
|  (DeepSeek-V4-Pro)|
+-------------------+
    |
    v
+-------------------+     +-------------------+
|  Retrieval        | --> |  Per-Cell Reasoner |
|  Local / Pinecone |     |  (audit_cell)      |
+-------------------+     +-------------------+
    |                          |
    v                          v
  SOPs (200 docs)        Audit Findings (JSON/CSV)
```

**Model:** DeepSeek-V4-Pro on Nebius AI Studio
**Orchestration:** deepagents (`create_deep_agent`) on LangGraph
**Retrieval:** Local keyword matching or Pinecone vector search (Qwen3-Embedding-8B)
**Grounding:** Tavily live regulation search
**Observability:** LangSmith tracing
**Deployment:** LangGraph Deployments

## Three-Act Demo

| Act | Description | Command |
|-----|-------------|---------|
| **Act 1** | Agentic RAG prototype — shows where naive retrieval breaks | `make act1` |
| **Act 2** | Production stack with structured one-shot retrieval | `make act2` |
| **Act 3** | Snowglobe adversarial simulation — red-teams the auditor | `make act3` |

Act 1 and Act 2 can also run with Pinecone vector search:

```bash
make ingest          # Embed and upsert 200 SOPs into Pinecone
make act1-pinecone   # Act 1 with multi-step RAG retrieval
make act2-pinecone   # Act 2 with Nexus one-shot retrieval
```

## Quickstart

### Prerequisites

- Python 3.11+
- API keys: Nebius, Pinecone (optional), Tavily (optional), LangSmith (optional)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

### Run the demo

```bash
make act1    # ~15 min, ~$0.30 on Nebius
make act2    # ~15 min, ~$0.30 on Nebius
make act3    # ~2 min, ~$0.01 on Nebius
make demo    # All three acts sequentially
```

### Deploy as LangGraph server

```bash
make dev     # Local dev server on port 2024 (hot reload)
make ui      # Streamlit UI on port 8501 (requires dev server running)
make build   # Build production Docker image
```

## Project Structure

```
sentinel_agent/
├── sentinel/                  # Core agent package
│   ├── config.py              # API keys, model config, paths
│   ├── models.py              # Pydantic models, regulation clauses (25 total)
│   ├── llm.py                 # Per-cell reasoner (DeepSeek-V4-Pro)
│   ├── graph/
│   │   ├── agent.py           # Deep agent (create_deep_agent entrypoint)
│   │   ├── tools.py           # LangChain tools for retrieval + auditing
│   │   ├── nodes.py           # LangGraph node functions
│   │   └── state.py           # State definitions
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
│   ├── act1_prototype.py      # Act 1 entry point
│   ├── act2_production.py     # Act 2 entry point
│   └── act3_simulation.py     # Act 3 entry point
├── ui/
│   └── app.py                 # Streamlit chat UI
├── data/
│   ├── sops/                  # 200 generated SOPs (10 business units)
│   ├── company_profile.md     # Meridian Health Technologies background
│   └── compliance_matrix.json # Ground truth (420 audit cells)
├── scripts/
│   ├── generate_sops.py       # SOP generation (DeepSeek-V4-Pro)
│   ├── sop_taxonomy.py        # 200 SOP definitions + compliance profiles
│   └── company_context.py     # Company profile + business units
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

This naturally touches SOC 2, HIPAA, and the other target regulations.

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

## Output

Each act produces:
- **CSV register** — one row per finding with all fields
- **JSON findings** — structured findings array
- **JSON metrics** — tokens, latency, cost, counts
- **Console output** — executive summary, heatmap, top gaps

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEBIUS_API_KEY` | Yes | Nebius AI Studio API key |
| `PINECONE_API_KEY` | For Pinecone mode | Pinecone vector DB key |
| `TAVILY_API_KEY` | Optional | Live regulation grounding |
| `LANGSMITH_API_KEY` | Optional | LangSmith tracing (auto-enabled) |
| `SNOWGLOBE_API_KEY` | Optional | Adversarial simulation |

## Cost

All inference runs on Nebius AI Studio (DeepSeek-V4-Pro):
- Full audit (200 findings): ~$0.30
- Full audit (400 findings with deepagents): ~$0.60
- Act 3 simulation: ~$0.01
- SOP ingestion (5,522 embeddings): ~$0.02
