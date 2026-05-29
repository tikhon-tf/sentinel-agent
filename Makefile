PYTHON = .venv/bin/python

.PHONY: install ingest act1 act2 act3 act4 demo all dev up build deploy forge-ui forge-ui-local test eval eval-naive eval-agentic eval-agentic-openai eval-all eval-smoke

install:
	$(PYTHON) -m pip install -e ".[dev,deep,demo,rag]"

ingest:
	$(PYTHON) -m sentinel.retrieval.ingest

ingest-regulations:
	$(PYTHON) -m sentinel.retrieval.ingest_regulations

act1:
	$(PYTHON) -m demo.act1_prototype --mode rag

act2:
	$(PYTHON) -m demo.act2_production --mode nexus

act3:
	$(PYTHON) -m demo.act3_simulation

act4:
	$(PYTHON) -m demo.act4_actuation

# Full demo sequence
demo: act1 act2 act3 act4

# Full pipeline: ingest SOPs, then run all four acts
all: ingest act1 act2 act3 act4

# LangGraph deployment
dev:
	.venv/bin/langgraph dev --no-browser --allow-blocking --no-reload --n-jobs-per-worker 20

up:
	langgraph up --wait

build:
	langgraph build -t sentinel-agent:latest

deploy:
	langgraph deploy

# Forge UI (FastAPI + static prototype). Talks to LangGraph at $LANGGRAPH_URL (default localhost:2024).
forge-ui:
	$(PYTHON) -m uvicorn ui_forge.server:app --host 0.0.0.0 --port 8080

forge-ui-local:
	LANGGRAPH_URL=http://localhost:2024 $(PYTHON) -m uvicorn ui_forge.server:app --host 0.0.0.0 --port 8080 --reload

test:
	$(PYTHON) -m pytest tests/ -v

# Naive RAG vs agentic Q&A eval. Pass EVAL_ARGS to override (e.g. --limit, --category, --no-judge).
eval:
	$(PYTHON) scripts/run_qa_eval.py --mode both $(EVAL_ARGS)

eval-naive:
	$(PYTHON) scripts/run_qa_eval.py --mode naive $(EVAL_ARGS)

eval-agentic:
	$(PYTHON) scripts/run_qa_eval.py --mode agentic $(EVAL_ARGS)

eval-agentic-openai:
	$(PYTHON) scripts/run_qa_eval.py --mode agentic-openai $(EVAL_ARGS)

# Run all three baselines: naive + agentic (Nebius) + agentic-openai.
eval-all:
	$(PYTHON) scripts/run_qa_eval.py --mode all $(EVAL_ARGS)

eval-smoke:
	$(PYTHON) scripts/run_qa_eval.py --mode both --limit 2 --no-judge
