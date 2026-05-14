PYTHON = .venv/bin/python

.PHONY: install ingest act1 act2 act3 demo all

install:
	$(PYTHON) -m pip install -e .

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
