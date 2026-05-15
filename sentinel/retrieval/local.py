"""Local file-based retrieval — fallback when Pinecone is not configured."""
from __future__ import annotations

import re
from pathlib import Path

from sentinel.config import SOPS_DIR
from sentinel.models import SOPChunk, RegulationClause, RELEVANT_BUSINESS_UNITS
from sentinel.retrieval.ingest import parse_sop


def _load_sops(business_units: list[str] | None = None) -> list[dict]:
    """Load all SOPs from disk."""
    bus = business_units or RELEVANT_BUSINESS_UNITS
    sops = []
    for bu in bus:
        bu_dir = SOPS_DIR / bu
        if not bu_dir.is_dir():
            continue
        for fp in sorted(bu_dir.glob("*.md")):
            parsed = parse_sop(fp)
            sops.append(parsed)
    return sops


def load_sop_by_id(sop_id: str) -> dict | None:
    """Load a single SOP by its sop_id or title (fuzzy match) from any business unit."""
    from sentinel.config import SOP_BUSINESS_UNITS

    query = sop_id.strip().lower()
    best_match = None
    best_score = 0

    for bu in SOP_BUSINESS_UNITS:
        bu_dir = SOPS_DIR / bu
        if not bu_dir.is_dir():
            continue
        for fp in sorted(bu_dir.glob("*.md")):
            parsed = parse_sop(fp)
            fm = parsed["frontmatter"]
            sid = fm.get("sop_id", "")
            title = fm.get("title", "")

            if sid == sop_id or sid.lower() == query:
                return parsed
            if title.lower() == query:
                return parsed

            if query in title.lower() or query in sid.lower():
                score = len(query) / max(len(title), 1)
                if score > best_score:
                    best_score = score
                    best_match = parsed

    return best_match


def list_all_sops() -> list[dict]:
    """Return metadata for all SOPs across all business units."""
    from sentinel.config import SOP_BUSINESS_UNITS
    results = []
    for bu in SOP_BUSINESS_UNITS:
        bu_dir = SOPS_DIR / bu
        if not bu_dir.is_dir():
            continue
        for fp in sorted(bu_dir.glob("*.md")):
            parsed = parse_sop(fp)
            fm = parsed["frontmatter"]
            results.append({
                "sop_id": fm.get("sop_id", fp.stem),
                "title": fm.get("title", fp.stem),
                "business_unit": fm.get("business_unit", bu),
                "regulations": fm.get("regulations", []),
            })
    return results


def load_sop_chunks(sop: dict) -> list[SOPChunk]:
    """Convert a parsed SOP dict into SOPChunk objects (one per section)."""
    fm = sop["frontmatter"]
    body = sop["body"]
    sop_id = fm.get("sop_id", "UNKNOWN")
    title = fm.get("title", "")
    business_unit = fm.get("business_unit", "")

    sections = re.split(r"(?=^## )", body, flags=re.MULTILINE)
    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        header = ""
        lines = section.split("\n", 1)
        if lines[0].startswith("## "):
            header = lines[0].lstrip("# ").strip()
        chunks.append(SOPChunk(
            sop_id=sop_id,
            title=title,
            business_unit=business_unit,
            chunk_text=section,
            section=header,
        ))
    return chunks


def _score_relevance(text: str, clause: RegulationClause) -> float:
    """Simple keyword-overlap relevance score."""
    keywords = set(
        re.findall(r"\b\w{4,}\b", f"{clause.title} {clause.description}".lower())
    )
    text_words = set(re.findall(r"\b\w{4,}\b", text.lower()))
    if not keywords:
        return 0.0
    overlap = keywords & text_words
    return len(overlap) / len(keywords)


def retrieve_local(
    clause: RegulationClause,
    business_units: list[str] | None = None,
    max_sops: int = 8,
    max_chunk_chars: int = 6000,
) -> dict[str, list[SOPChunk]]:
    """
    Retrieve relevant SOP content from local files using keyword matching.
    Groups by SOP, returns top-scoring SOPs with their content.
    """
    all_sops = _load_sops(business_units)

    scored: list[tuple[float, dict]] = []
    for sop in all_sops:
        fm = sop["frontmatter"]
        body = sop["body"]
        score = _score_relevance(body, clause)

        regs = fm.get("regulations", [])
        if isinstance(regs, list):
            for reg in regs:
                if clause.regulation.lower() in reg.lower():
                    score += 0.3
                    break

        scored.append((score, sop))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_sops = scored[:max_sops]

    by_sop: dict[str, list[SOPChunk]] = {}
    for score, sop in top_sops:
        if score < 0.1:
            continue
        fm = sop["frontmatter"]
        sop_id = fm.get("sop_id", "UNKNOWN")
        title = fm.get("title", "")
        business_unit = fm.get("business_unit", "")
        body = sop["body"]

        sections = re.split(r"(?=^## )", body, flags=re.MULTILINE)
        relevant_sections = []
        for section in sections:
            sec_score = _score_relevance(section, clause)
            if sec_score > 0.05:
                relevant_sections.append((sec_score, section))
        relevant_sections.sort(key=lambda x: x[0], reverse=True)

        chunks = []
        total_chars = 0
        for sec_score, section_text in relevant_sections:
            if total_chars >= max_chunk_chars:
                break
            header = ""
            lines = section_text.strip().split("\n", 1)
            if lines[0].startswith("## "):
                header = lines[0].lstrip("# ").strip()

            text = section_text[:max_chunk_chars - total_chars]
            chunks.append(SOPChunk(
                sop_id=sop_id,
                title=title,
                business_unit=business_unit,
                chunk_text=text.strip(),
                section=header,
                score=sec_score,
            ))
            total_chars += len(text)

        if chunks:
            by_sop[sop_id] = chunks

    return by_sop
