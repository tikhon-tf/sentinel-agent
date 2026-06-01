PYTHON = .venv/bin/python

.PHONY: install ingest dev up build deploy ui ui-local test eval eval-naive eval-agentic eval-agentic-openai eval-agentic-openai-tavily eval-agentic-nemotron eval-all eval-smoke

install:
	$(PYTHON) -m pip install -e ".[dev,deep,demo,rag]"

ingest:
	$(PYTHON) -m sentinel.retrieval.ingest

ingest-regulations:
	$(PYTHON) -m sentinel.retrieval.ingest_regulations

# LangGraph deployment
dev:
	.venv/bin/langgraph dev --no-browser --allow-blocking --no-reload --n-jobs-per-worker 20

up:
	langgraph up --wait

build:
	langgraph build -t sentinel-agent:latest

deploy:
	langgraph deploy

# UI (FastAPI + React). Talks to LangGraph at $LANGGRAPH_URL (default localhost:2024).
ui:
	$(PYTHON) -m uvicorn ui.server:app --host 0.0.0.0 --port 8080

ui-local:
	LANGGRAPH_URL=http://localhost:2024 $(PYTHON) -m uvicorn ui.server:app --host 0.0.0.0 --port 8080 --reload

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

eval-agentic-openai-tavily:
	$(PYTHON) scripts/run_qa_eval.py --mode agentic-openai-tavily $(EVAL_ARGS)

eval-agentic-nemotron:
	$(PYTHON) scripts/run_qa_eval.py --mode agentic-nemotron $(EVAL_ARGS)

# Run all baselines.
eval-all:
	$(PYTHON) scripts/run_qa_eval.py --mode all $(EVAL_ARGS)

eval-smoke:
	$(PYTHON) scripts/run_qa_eval.py --mode both --limit 2 --no-judge
