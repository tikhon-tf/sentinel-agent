"""Act 1: Agentic RAG retrieval — iterative query-expand-retrieve-rerank loop."""
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


def expand_queries(clause: RegulationClause) -> list[str]:
    """Generate multiple search queries from a single regulation clause (Act 1 pattern)."""
    base = f"{clause.title} {clause.description}"
    return [
        base,
        f"{clause.regulation} {clause.title} policy procedure",
        f"{clause.title} controls safeguards implementation",
        f"{clause.reference} compliance requirements SOP",
    ]


def retrieve_rag(
    clause: RegulationClause,
    top_k: int = 10,
    namespaces: list[str] | None = None,
) -> tuple[list[SOPChunk], dict]:
    """
    Act 1: Agentic RAG retrieval.
    Multiple query expansions, multiple retrieval rounds, top-k per round, RRF-style fusion.
    Returns chunks and metrics tracking retrieval steps/tokens.
    """
    index = _get_index()
    namespaces = namespaces or RELEVANT_BUSINESS_UNITS

    queries = expand_queries(clause)
    all_embeddings = embed_texts(queries)

    seen_ids: set[str] = set()
    scored_chunks: dict[str, tuple[SOPChunk, float]] = {}
    total_steps = 0

    for query_embedding in all_embeddings:
        for ns in namespaces:
            total_steps += 1
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=ns,
                include_metadata=True,
            )

            for match in results.matches:
                mid = match.id
                if mid in seen_ids:
                    old_score = scored_chunks[mid][1]
                    scored_chunks[mid] = (scored_chunks[mid][0], old_score + match.score)
                    continue

                seen_ids.add(mid)
                meta = match.metadata or {}
                chunk = SOPChunk(
                    sop_id=meta.get("sop_id", mid.split("::")[0]),
                    title=meta.get("title", ""),
                    business_unit=meta.get("business_unit", ns),
                    chunk_text=meta.get("text", ""),
                    section=meta.get("section", ""),
                    score=match.score,
                )
                scored_chunks[mid] = (chunk, match.score)

    ranked = sorted(scored_chunks.values(), key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, _ in ranked[:top_k]]

    metrics = {
        "retrieval_steps": total_steps,
        "queries_expanded": len(queries),
        "total_candidates": len(scored_chunks),
        "returned": len(top_chunks),
    }

    return top_chunks, metrics


def retrieve_for_clause_rag(
    clause: RegulationClause,
) -> dict[str, list[SOPChunk]]:
    """Retrieve and group chunks by SOP for a clause using agentic RAG."""
    chunks, _ = retrieve_rag(clause, top_k=20)

    by_sop: dict[str, list[SOPChunk]] = {}
    for chunk in chunks:
        by_sop.setdefault(chunk.sop_id, []).append(chunk)

    return by_sop
