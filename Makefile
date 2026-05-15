PYTHON = .venv/bin/python

.PHONY: install ingest act1 act2 act3 demo all dev up build deploy ui

install:
	$(PYTHON) -m pip install -e ".[dev,deep,demo,rag]"

ingest:
	$(PYTHON) -m sentinel.retrieval.ingest

act1:
	$(PYTHON) -m demo.act1_prototype --mode local

act2:
	$(PYTHON) -m demo.act2_production --mode local

act3:
	$(PYTHON) -m demo.act3_simulation

# Run act1 and act2 with Pinecone (requires PINECONE_API_KEY)
act1-pinecone:
	$(PYTHON) -m demo.act1_prototype --mode rag

act2-pinecone:
	$(PYTHON) -m demo.act2_production --mode nexus

# Full demo sequence
demo: act1 act2 act3

# Full pipeline: ingest SOPs, then run all three acts
all: ingest act1-pinecone act2-pinecone act3

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
	.venv/bin/streamlit run ui/app.py --server.port 8501

ui-local:
	LANGGRAPH_URL=http://localhost:2024 .venv/bin/streamlit run ui/app.py --server.port 8501
