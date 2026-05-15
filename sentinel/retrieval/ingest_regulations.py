"""Ingest regulation text files into Pinecone for RAG-based compliance grounding."""
from __future__ import annotations

import re
from pathlib import Path

from sentinel.config import (
    EMBEDDING_DIMENSION,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    REGULATIONS_DIR,
)
from sentinel.retrieval.ingest import embed_texts

REGULATION_MAP = {
    "hipaa_45cfr_part160": "HIPAA",
    "hipaa_45cfr_part162": "HIPAA",
    "hipaa_45cfr_part164": "HIPAA",
    "soc2": "SOC 2",
    "gdpr": "GDPR",
    "eu_ai_act": "EU AI Act",
    "nist_ai_rmf": "NIST AI RMF",
    "nist_ai_600": "NIST AI RMF",
    "california_sb53": "California SB 53",
    "california_sb942": "California SB 942",
    "california_ab853": "California AB 853",
    "sr_11_7": "SR 11-7",
    "sr_26_2": "SR 11-7",
}


EDITION_PATTERNS = {
    "_2017": "2017",
    "_2020": "2020",
    "_2024": "2024",
    "_draft1_2022": "2022-draft1",
    "_draft2_2022": "2022-draft2",
    "_2021_commission_proposal": "2021-proposal",
    "_2026": "2026",
}


def _detect_regulation(filename: str) -> str:
    for prefix, reg in REGULATION_MAP.items():
        if prefix in filename:
            return reg
    return "Unknown"


def _detect_edition(filename: str) -> str:
    for pattern, edition in EDITION_PATTERNS.items():
        if pattern in filename:
            return edition
    return "current"


def _chunk_txt(filepath: Path, chunk_size: int = 1200, overlap: int = 200) -> list[dict]:
    """Chunk a .txt regulation file by section headers (§ or === markers)."""
    text = filepath.read_text(encoding="utf-8")
    regulation = _detect_regulation(filepath.stem)
    edition = _detect_edition(filepath.stem)

    sections = re.split(
        r"(?=^  § |\n={40,}|\n-{40,})",
        text,
        flags=re.MULTILINE,
    )

    chunks = []
    for section in sections:
        section = section.strip()
        if not section or len(section) < 20:
            continue

        header = ""
        first_line = section.split("\n", 1)[0].strip()
        if first_line.startswith("§") or first_line.startswith("="):
            header = first_line.strip("= -§").strip()

        if len(section) <= chunk_size:
            chunks.append({
                "text": section,
                "section": header,
                "regulation": regulation,
                "edition": edition,
                "source": filepath.name,
            })
        else:
            words = section.split()
            words_per_chunk = chunk_size // 5
            start = 0
            part = 0
            while start < len(words):
                end = start + words_per_chunk
                chunk_text = " ".join(words[start:end])
                if header and part > 0:
                    chunk_text = f"§ {header} (continued)\n\n{chunk_text}"
                chunks.append({
                    "text": chunk_text,
                    "section": header,
                    "regulation": regulation,
                    "edition": edition,
                    "source": filepath.name,
                })
                part += 1
                start = end - overlap // 5

    return chunks


def _chunk_md(filepath: Path, chunk_size: int = 1200, overlap: int = 200) -> list[dict]:
    """Chunk a .md regulation file by article/section headers."""
    text = filepath.read_text(encoding="utf-8")
    regulation = _detect_regulation(filepath.stem)
    edition = _detect_edition(filepath.stem)

    sections = re.split(r"(?=^### )", text, flags=re.MULTILINE)

    chunks = []
    for section in sections:
        section = section.strip()
        if not section or len(section) < 20:
            continue

        header = ""
        first_line = section.split("\n", 1)[0].strip()
        if first_line.startswith("###"):
            header = first_line.lstrip("# ").strip()

        if len(section) <= chunk_size:
            chunks.append({
                "text": section,
                "section": header,
                "regulation": regulation,
                "edition": edition,
                "source": filepath.name,
            })
        else:
            words = section.split()
            words_per_chunk = chunk_size // 5
            start = 0
            part = 0
            while start < len(words):
                end = start + words_per_chunk
                chunk_text = " ".join(words[start:end])
                if header and part > 0:
                    chunk_text = f"### {header} (continued)\n\n{chunk_text}"
                chunks.append({
                    "text": chunk_text,
                    "section": header,
                    "regulation": regulation,
                    "edition": edition,
                    "source": filepath.name,
                })
                part += 1
                start = end - overlap // 5

    return chunks


def chunk_regulation(filepath: Path) -> list[dict]:
    if filepath.suffix == ".md":
        return _chunk_md(filepath)
    return _chunk_txt(filepath)


def ingest_regulations():
    """Ingest all regulation text files into Pinecone."""
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key=PINECONE_API_KEY)
    existing = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pc.Index(PINECONE_INDEX_NAME)

    files = sorted(REGULATIONS_DIR.glob("*.txt")) + sorted(REGULATIONS_DIR.glob("*.md"))
    files = [f for f in files if f.name != "README.md"]

    all_chunks = []
    for filepath in files:
        chunks = chunk_regulation(filepath)
        for i, chunk in enumerate(chunks):
            chunk["id"] = f"reg::{filepath.stem}::chunk-{i:04d}"
        all_chunks.extend(chunks)
        print(f"  {filepath.name}: {len(chunks)} chunks")

    if not all_chunks:
        print("No regulation chunks to ingest.")
        return 0

    print(f"\nEmbedding {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]
    embeddings = embed_texts(texts)

    vectors = []
    for chunk, embedding in zip(all_chunks, embeddings):
        vectors.append({
            "id": chunk["id"],
            "values": embedding,
            "metadata": {
                "text": chunk["text"][:4000],
                "section": chunk["section"],
                "regulation": chunk["regulation"],
                "edition": chunk.get("edition", "current"),
                "source": chunk["source"],
            },
        })

    namespace = "regulations"
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)

    print(f"\nIngested {len(vectors)} regulation chunks into namespace '{namespace}'")
    return len(vectors)


if __name__ == "__main__":
    ingest_regulations()
