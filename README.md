# Sentinel — Regulatory Compliance Auditor Agent

Sentinel is an AI-powered compliance auditor that assesses 200 enterprise SOPs against 9 regulation frameworks (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California SB 53/SB 942/AB 853). Regulation text is stored in a Pinecone knowledge base and retrieved dynamically during auditing. Built for the [Nebius Blueprint for Agents](https://nebius.com/) demo (Nebius Inflection, June 9, 2026).

## Architecture

```
User Query
    |
    v
+------------------------+
|  Sentinel ReAct Agent  |  LangGraph (+ deepagents when available)
|  (DeepSeek-V4-Pro)     |
+------------------------+
    |
    +---> audit_all_sops (10-wide ThreadPoolExecutor)
              |
              v  (per SOP)
         +-------------------+
         |  Sub-Agent        |  LangGraph ReAct
         |  (audit_single_   |
         |   sop)            |
         +-------------------+
              |
              +---> retrieve_regulation (Pinecone semantic search)
              +---> search_web (Tavily live search)
              +---> read_sop (SOP text)
              |
              v
         Structured JSON Findings
```

**Model:** DeepSeek-V4-Pro on Nebius AI Studio (Act 2 + deployment), Claude Opus 4.7 on Anthropic (Act 1)
**Orchestration:** LangGraph ReAct agent with per-SOP sub-agents, optional deepagents upgrade
**Retrieval:** Pinecone vector search (Qwen3-Embedding-8B embeddings, 4096 dimensions)
**Grounding:** Tavily live regulation search
**Observability:** LangSmith tracing with cost tracking + [LangSmith MCP](https://docs.langchain.com/langsmith/langsmith-remote-mcp) integration
**Deployment:** LangGraph Cloud + Streamlit UI

## Three-Act Demo

| Act | Description | Model | Command |
|-----|-------------|-------|---------|
| **Act 1** | Agentic RAG prototype — same sub-agent architecture, shows baseline | Claude Opus 4.7 | `make act1` |
| **Act 2** | Production stack — DeepSeek on Nebius with full retrieval | DeepSeek-V4-Pro | `make act2` |
| **Act 3** | Snowglobe adversarial simulation — red-teams the auditor | DeepSeek-V4-Pro | `make act3` |

## Quickstart

### Prerequisites

- Python 3.11+
- API keys: Nebius, Anthropic (Act 1), Pinecone, Tavily (optional), LangSmith (optional)

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

### Ingest data

```bash
make ingest               # SOPs into Pinecone
make ingest-regulations   # Regulation texts into Pinecone (namespace: regulations)
```

### Run the demo

```bash
make act1    # Claude Opus 4.7 + Pinecone RAG
make act2    # DeepSeek-V4-Pro + Pinecone
make act3    # Adversarial simulation
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

Sentinel fans out by SOP using a sub-agent architecture. Each SOP is audited by a dedicated LangGraph ReAct sub-agent that:

1. Reads the full SOP text
2. Determines which regulations apply based on content and business unit
3. Iteratively queries the Pinecone knowledge base for each applicable regulation
4. Optionally searches the web for latest guidance
5. Outputs structured JSON findings with compliance levels, severity, evidence, and remediation

`audit_all_sops` fans out 200 sub-agents through a 10-wide `ThreadPoolExecutor`.

Key tools:
- `audit_all_sops` — full audit across all 200 SOPs in parallel
- `audit_single_sop` — audit one SOP via a dedicated sub-agent
- `list_sops` — search and discover SOPs by title, ID, or business unit
- `list_regulations` — list all regulations in the knowledge base
- `retrieve_regulation_text_tool` — look up specific regulation requirements

## Project Structure

```
sentinel_agent/
├── sentinel/                  # Core agent package
│   ├── config.py              # API keys, model config, pricing, paths
│   ├── models.py              # Pydantic models (AuditFinding, SOPChunk, AuditMetrics)
│   ├── llm.py                 # OpenAI client provider switching
│   ├── graph/
│   │   ├── agent.py           # ReAct agent (deepagents fallback to LangGraph)
│   │   └── tools.py           # LangChain tools: sub-agent auditing + retrieval
│   ├── retrieval/
│   │   ├── local.py           # SOP file loading and search
│   │   ├── regulations.py     # Pinecone regulation text retrieval
│   │   ├── ingest.py          # SOP -> Pinecone ingestion
│   │   └── ingest_regulations.py  # Regulation text -> Pinecone ingestion
│   ├── simulation/
│   │   └── snowglobe.py       # Adversarial scenarios (Act 3)
│   └── output/
│       ├── heatmap.py         # Rich console heatmap + summary
│       └── register.py        # CSV/JSON/metrics output
├── demo/
│   ├── act1_prototype.py      # Act 1: Claude Opus 4.7 + RAG
│   ├── act2_production.py     # Act 2: DeepSeek-V4-Pro
│   └── act3_simulation.py     # Act 3: Adversarial
├── ui/
│   └── app.py                 # Streamlit chat UI with streaming + cost tracking
├── scripts/
│   ├── generate_sops.py       # SOP generation (one-time)
│   ├── extract_pdf_text.py    # PDF -> text extraction for regulations
│   └── sop_taxonomy.py        # SOP definitions + metadata
├── data/
│   ├── sops/                  # 200 generated SOPs (10 business units)
│   ├── regulations/           # 9 regulation frameworks (txt, md, pdf, xml)
│   ├── company_profile.md     # Meridian Health Technologies background
│   └── compliance_matrix.json # Ground truth
├── .mcp.json                  # MCP server config (LangSmith)
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

9 regulation frameworks with full text in the Pinecone knowledge base:

- **HIPAA Security Rule** — Administrative (164.308), Physical (164.310), Technical (164.312) safeguards
- **SOC 2 Trust Services Criteria** — CC1 through CC9
- **GDPR** — Data protection, privacy rights, cross-border transfers
- **EU AI Act** — High-risk AI system requirements, conformity assessments
- **NIST AI RMF** — AI risk management framework
- **SR 11-7** — Model risk management (banking/fintech)
- **California AI Laws** — SB 53, SB 942, AB 853

Historical editions are included for temporal analysis (e.g., HIPAA 2017/2020/2024, EU AI Act proposal vs. final).

## SOP Dataset

200 SOPs across 10 business units with deliberately varied compliance levels:
- ~40% Compliant (thorough, specific, cites regulation articles)
- ~35% Partial (vague language, incomplete controls)
- ~25% Gap (missing key requirements, weak controls)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEBIUS_API_KEY` | Yes | Nebius AI Studio API key |
| `ANTHROPIC_API_KEY` | For Act 1 | Anthropic API key (Claude Opus 4.7) |
| `PINECONE_API_KEY` | Yes | Pinecone vector DB key |
| `TAVILY_API_KEY` | Optional | Live regulation grounding |
| `LANGSMITH_API_KEY` | Optional | LangSmith tracing + cloud auth |
| `SNOWGLOBE_API_KEY` | Optional | Adversarial simulation (Act 3) |
| `LANGGRAPH_URL` | Optional | Override UI backend URL |

## Cost

| Operation | Model | Estimated Cost |
|-----------|-------|---------------|
| Full audit (Act 2) | DeepSeek-V4-Pro ($1.75/$3.50 per M tokens) | ~$0.30 |
| Full audit (Act 1) | Claude Opus 4.7 ($5/$25 per M tokens) | ~$8.00 |
| Act 3 simulation | DeepSeek-V4-Pro | ~$0.01 |
| SOP ingestion | Qwen3-Embedding-8B | ~$0.02 |

Token usage and cost (including sub-agent usage) are displayed per-response and per-session in the Streamlit UI.

## MCP Integrations

A [LangSmith remote MCP server](https://docs.langchain.com/langsmith/langsmith-remote-mcp) is configured in `.mcp.json` for accessing LangSmith traces, runs, and datasets from Claude Code. Uses OAuth authentication — a browser login flow runs on first use.
