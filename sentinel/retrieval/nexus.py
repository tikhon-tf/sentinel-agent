"""Act 2: Pinecone Nexus — structured, one-shot retrieval via knowledge artifacts."""
from __future__ import annotations

from pinecone import Pinecone

from sentinel.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from sentinel.models import SOPChunk, RegulationClause, RELEVANT_BUSINESS_UNITS
from sentinel.retrieval.ingest import embed_texts


_pc: Pinecone | None = None
_index = None


def _get_index():
    global _pc, _index
    if _index is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = _pc.Index(PINECONE_INDEX_NAME)
    return _index


def retrieve_nexus(
    clause: RegulationClause,
    top_k: int = 15,
    namespaces: list[str] | None = None,
) -> tuple[list[SOPChunk], dict]:
    """
    Act 2: Structured one-shot retrieval.
    Single precise query, all relevant namespaces queried in one pass,
    results returned as typed artifacts with field-level citations.
    """
    index = _get_index()
    namespaces = namespaces or RELEVANT_BUSINESS_UNITS

    query = (
        f"{clause.regulation} — {clause.title}: {clause.description} "
        f"Find the SOP controls, policies, and procedures that satisfy {clause.reference}. "
        f"Include access controls, safeguards, monitoring, and documentation requirements."
    )
    embedding = embed_texts([query])[0]

    all_chunks: list[SOPChunk] = []
    total_steps = 0

    for ns in namespaces:
        total_steps += 1
        results = index.query(
            vector=embedding,
            top_k=top_k,
            namespace=ns,
            include_metadata=True,
        )

        for match in results.matches:
            meta = match.metadata or {}
            chunk = SOPChunk(
                sop_id=meta.get("sop_id", match.id.split("::")[0]),
                title=meta.get("title", ""),
                business_unit=meta.get("business_unit", ns),
                chunk_text=meta.get("text", ""),
                section=meta.get("section", ""),
                score=match.score,
            )
            all_chunks.append(chunk)

    all_chunks.sort(key=lambda c: c.score, reverse=True)
    top = all_chunks[:top_k]

    metrics = {
        "retrieval_steps": total_steps,
        "queries_expanded": 1,
        "total_candidates": len(all_chunks),
        "returned": len(top),
    }

    return top, metrics


def retrieve_for_clause_nexus(
    clause: RegulationClause,
) -> dict[str, list[SOPChunk]]:
    """Retrieve and group chunks by SOP for a clause using Nexus one-shot."""
    chunks, _ = retrieve_nexus(clause, top_k=15)

    by_sop: dict[str, list[SOPChunk]] = {}
    for chunk in chunks:
        by_sop.setdefault(chunk.sop_id, []).append(chunk)

    return by_sop
