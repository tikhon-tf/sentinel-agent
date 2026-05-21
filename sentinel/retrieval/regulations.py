"""Retrieve regulation text from Pinecone for compliance grounding."""
from __future__ import annotations

from pinecone import Pinecone

from sentinel.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from sentinel.retrieval.ingest import embed_texts


_pc: Pinecone | None = None
_index = None

NAMESPACE = "regulations"


def _get_index():
    global _pc, _index
    if _index is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = _pc.Index(PINECONE_INDEX_NAME)
    return _index


def retrieve_regulation_text(
    query: str,
    regulations: list[str] | None = None,
    top_k: int = 20,
) -> list[dict]:
    """Retrieve regulation text chunks relevant to a query.

    Args:
        query: search query (e.g. SOP title + regulation names)
        regulations: optional filter — only return chunks from these regulations
        top_k: max chunks to return

    Returns:
        list of dicts with keys: text, section, regulation, source, score
    """
    index = _get_index()
    embedding = embed_texts([query])[0]

    filter_dict = None
    if regulations:
        filter_dict = {"regulation": {"$in": regulations}}

    results = index.query(
        vector=embedding,
        top_k=top_k,
        namespace=NAMESPACE,
        include_metadata=True,
        filter=filter_dict,
    )

    chunks = []
    for match in results.matches:
        meta = match.metadata or {}
        chunks.append({
            "text": meta.get("text", ""),
            "section": meta.get("section", ""),
            "regulation": meta.get("regulation", ""),
            "source": meta.get("source", ""),
            "score": match.score,
        })

    return chunks


def retrieve_for_sop(
    sop_title: str,
    sop_regulations: list[str] | None = None,
    top_k: int = 25,
) -> list[dict]:
    """Retrieve regulation text relevant to a specific SOP.

    If sop_regulations is provided, filters to those regulations.
    If None, retrieves from all regulations (letting the LLM decide relevance).
    """
    reg_names = _normalize_regulation_names(sop_regulations) if sop_regulations else None

    if reg_names:
        query = f"{' '.join(reg_names)} requirements for: {sop_title}. "
    else:
        query = f"Regulatory compliance requirements for: {sop_title}. "
    query += "Find the specific regulatory controls, safeguards, and compliance requirements."

    return retrieve_regulation_text(query, regulations=reg_names, top_k=top_k)


def _normalize_regulation_names(raw_names: list[str]) -> list[str]:
    """Map SOP regulation tags to Pinecone regulation metadata values."""
    mapping = {
        "soc 2": "SOC 2",
        "soc2": "SOC 2",
        "hipaa": "HIPAA",
        "hipaa security rule": "HIPAA",
        "gdpr": "GDPR",
        "eu ai act": "EU AI Act",
        "nist ai rmf": "NIST AI RMF",
        "sr 11-7": "SR 11-7",
        "california": "California SB 53",
    }
    result = []
    for name in raw_names:
        lower = name.lower().strip()
        matched = mapping.get(lower)
        if matched:
            result.append(matched)
        else:
            for key, val in mapping.items():
                if key in lower or lower in key:
                    result.append(val)
                    break
    return list(set(result)) if result else list(set(mapping.values()))


def format_regulation_context(chunks: list[dict], max_chars: int = 12000) -> str:
    """Format retrieved regulation chunks into a text block for the LLM prompt.

    Section headers (e.g. ``### HIPAA``) are only emitted for regulations that
    actually contribute at least one non-empty content chunk to the rendered
    block. Emitting a bare header when no excerpt text follows previously
    misled the LLM into treating header presence as evidence that the
    regulation exists in the knowledge base (and, in the empty-excerpt case,
    that it is the *only* regulation available). See issue:
    "sentinel_act0 hallucinates 'HIPAA is the only regulation available'
    from empty excerpts".
    """
    if not chunks:
        return ""

    by_regulation: dict[str, list[dict]] = {}
    for chunk in chunks:
        reg = chunk.get("regulation", "Unknown")
        by_regulation.setdefault(reg, []).append(chunk)

    parts: list[str] = []
    total = 0
    for reg, reg_chunks in sorted(by_regulation.items()):
        header_str = f"\n### {reg}\n"
        block_parts: list[str] = []
        block_total = 0
        for chunk in reg_chunks:
            text = chunk.get("text", "")
            if not text or not text.strip():
                # Skip empty/whitespace-only chunks — they contribute no
                # content and would otherwise leave only the header behind.
                continue
            if total + len(header_str) + block_total + len(text) > max_chars:
                break
            section = chunk.get("section", "")
            section_header = f"**{section}**\n" if section else ""
            block_parts.append(f"{section_header}{text}\n")
            block_total += len(section_header) + len(text)

        if not block_parts:
            # No content lines under this regulation — drop the entire
            # block (including the ``### <Regulation>`` header) so the
            # model doesn't read header presence as KB inventory.
            continue

        parts.append(header_str)
        parts.extend(block_parts)
        total += len(header_str) + block_total

    return "\n".join(parts)
