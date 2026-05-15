PYTHON = .venv/bin/python

.PHONY: install ingest act1 act2 act3 demo all dev up build deploy ui

install:
	$(PYTHON) -m pip install -e ".[dev,deep,demo,rag,ui]"

ingest:
	$(PYTHON) -m sentinel.retrieval.ingest

act1:
	$(PYTHON) -m demo.act1_prototype --mode rag

act2:
	$(PYTHON) -m demo.act2_production --mode nexus

act3:
	$(PYTHON) -m demo.act3_simulation

# Full demo sequence
demo: act1 act2 act3

# Full pipeline: ingest SOPs, then run all three acts
all: ingest act1 act2 act3

# LangGraph deployment
dev:
	.venv/bin/langgraph dev --no-browser --allow-blocking --no-reload

up:
	langgraph up --wait

build:
	langgraph build -t sentinel-agent:latest

deploy:
	langgraph deploy

ui:
	$(PYTHON) -m streamlit run ui/app.py --server.port 8501

ui-local:
	LANGGRAPH_URL=http://localhost:2024 $(PYTHON) -m streamlit run ui/app.py --server.port 8501
