"""LangChain tools wrapping Sentinel's retrieval and auditing functions."""
from __future__ import annotations

from langchain_core.tools import tool

from sentinel.config import PINECONE_API_KEY, RETRIEVAL_MODE
from sentinel.llm import audit_sop
from sentinel.models import (
    AuditFinding,
    ComplianceLevel,
    Severity,
)

_audit_results: dict = {"findings": [], "cell_metrics": []}
_retrieval_mode: str = RETRIEVAL_MODE


def set_retrieval_mode(mode: str) -> None:
    _audit_results["mode"] = mode
    global _retrieval_mode
    _retrieval_mode = mode


def get_audit_results() -> dict:
    return _audit_results


def reset_audit_results() -> None:
    _audit_results["findings"] = []
    _audit_results["cell_metrics"] = []


def _get_regulation_context(sop_title: str, regulations: list[str]) -> str:
    """Retrieve regulation text from Pinecone for a given SOP."""
    if not PINECONE_API_KEY:
        return ""
    try:
        from sentinel.retrieval.regulations import retrieve_for_sop, format_regulation_context
        chunks = retrieve_for_sop(sop_title, regulations)
        return format_regulation_context(chunks)
    except Exception:
        return ""


@tool
def list_regulations() -> str:
    """List all regulations available in the knowledge base. Returns regulation names and document sources."""
    if not PINECONE_API_KEY:
        return _list_regulations_local()
    try:
        from sentinel.config import PINECONE_INDEX_NAME
        from sentinel.retrieval.ingest import embed_texts
        from pinecone import Pinecone

        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)

        known_regs = [
            "HIPAA", "SOC 2", "GDPR", "EU AI Act", "NIST AI RMF",
            "SR 11-7", "California SB 53", "California SB 942", "California AB 853",
        ]
        query_text = "regulatory compliance requirements"
        embedding = embed_texts([query_text])[0]

        regs: dict[str, set[str]] = {}
        for reg_name in known_regs:
            results = index.query(
                vector=embedding,
                top_k=5,
                namespace="regulations",
                include_metadata=True,
                filter={"regulation": {"$eq": reg_name}},
            )
            for match in results.matches:
                source = match.metadata.get("source", "")
                edition = match.metadata.get("edition", "current")
                regs.setdefault(reg_name, set()).add(f"{source} ({edition})")

        # Also do an unfiltered query to catch anything not in known_regs
        results = index.query(
            vector=embedding, top_k=20, namespace="regulations", include_metadata=True,
        )
        for match in results.matches:
            reg = match.metadata.get("regulation", "Unknown")
            source = match.metadata.get("source", "")
            edition = match.metadata.get("edition", "current")
            regs.setdefault(reg, set()).add(f"{source} ({edition})")

        lines = []
        for reg in sorted(regs.keys()):
            sources = ", ".join(sorted(regs[reg]))
            lines.append(f"- {reg}: {sources}")
        return f"{len(regs)} regulations in knowledge base:\n" + "\n".join(lines)
    except Exception as e:
        return _list_regulations_local()


def _list_regulations_local() -> str:
    from sentinel.config import DATA_DIR
    reg_dir = DATA_DIR / "regulations"
    files = sorted(reg_dir.glob("*.txt")) + sorted(reg_dir.glob("*.md"))
    files = [f for f in files if f.name != "README.md"]
    lines = [f"- {f.stem}" for f in files]
    return f"{len(files)} regulation files available:\n" + "\n".join(lines)


@tool
def retrieve_regulation_text_tool(query: str, regulation: str = "") -> str:
    """Retrieve regulation text from the knowledge base for a given query. Optionally filter by regulation name (e.g. 'HIPAA', 'SOC 2', 'GDPR')."""
    if not PINECONE_API_KEY:
        return "Pinecone not configured. Use local retrieval mode."
    try:
        from sentinel.retrieval.regulations import retrieve_regulation_text, format_regulation_context
        regs = [regulation] if regulation else None
        chunks = retrieve_regulation_text(query, regulations=regs, top_k=15)
        if not chunks:
            return f"No regulation text found for: {query}"
        context = format_regulation_context(chunks)
        return f"Retrieved {len(chunks)} regulation sections:\n{context}"
    except Exception as e:
        return f"Regulation retrieval failed: {e}"


@tool
def audit_single_sop(sop_id: str) -> str:
    """Audit one SOP against all relevant regulations by retrieving actual regulation text from the knowledge base. Returns compliance findings with specific regulatory citations."""
    from sentinel.retrieval.local import load_sop_by_id, load_sop_chunks

    sop = load_sop_by_id(sop_id)
    if sop is None:
        return f"SOP not found: {sop_id}"

    fm = sop["frontmatter"]
    chunks = load_sop_chunks(sop)
    if not chunks:
        return f"SOP {sop_id} has no content"

    regulations = fm.get("regulations", [])
    if not regulations:
        return f"SOP {sop_id} ({fm.get('title', '')}) has no tagged regulations — skipping"

    reg_context = _get_regulation_context(fm.get("title", sop_id), regulations)
    if not reg_context:
        return f"SOP {sop_id}: no regulation text retrieved — check Pinecone connection"

    try:
        findings, metrics = audit_sop(chunks, reg_context, regulations)
    except Exception as e:
        return f"SOP {sop_id}: audit failed — {e}"

    for f in findings:
        _audit_results["findings"].append(f)
    _audit_results["cell_metrics"].append({
        "sop_id": sop_id,
        "regulations": regulations,
        "findings": len(findings),
        **metrics,
    })

    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    lines = [f"{sop_id} ({fm.get('title', '')}): {len(findings)} findings — {compliant}C/{partial}P/{gap}G"]
    for f in findings:
        lines.append(f"  {f.clause_id}: {f.compliance_level.value} ({f.severity.value}) — {f.gap_description or 'Compliant'}")
    return "\n".join(lines)


@tool
def audit_all_sops() -> str:
    """Run the full audit across ALL SOPs, retrieving regulation text from the knowledge base for each. Fans out by SOP with 10-wide parallelism."""
    import concurrent.futures
    from sentinel.retrieval.local import list_all_sops, load_sop_by_id, load_sop_chunks

    all_sops = list_all_sops()

    def _audit_one_sop(sop_meta: dict) -> str:
        sid = sop_meta["sop_id"]
        regulations = sop_meta.get("regulations", [])
        if not regulations:
            return f"{sid}: skipped (no tagged regulations)"

        sop = load_sop_by_id(sid)
        if sop is None:
            return f"{sid}: skipped (not found)"

        chunks = load_sop_chunks(sop)
        if not chunks:
            return f"{sid}: skipped (no content)"

        reg_context = _get_regulation_context(sop_meta.get("title", sid), regulations)
        if not reg_context:
            return f"{sid}: skipped (no regulation text retrieved)"

        try:
            findings, metrics = audit_sop(chunks, reg_context, regulations)
        except Exception as e:
            return f"{sid}: FAILED — {e}"

        for f in findings:
            _audit_results["findings"].append(f)
        _audit_results["cell_metrics"].append({
            "sop_id": sid,
            "regulations": regulations,
            "findings": len(findings),
            **metrics,
        })

        compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
        partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
        gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)
        return f"{sid}: {len(findings)} findings — {compliant}C/{partial}P/{gap}G"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_audit_one_sop, s): s for s in all_sops}
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    findings = _audit_results["findings"]
    total = len(findings)
    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    summary = (
        f"Audit complete: {total} findings across {len(all_sops)} SOPs\n"
        f"  Compliant: {compliant} ({100*compliant//max(total,1)}%)\n"
        f"  Partial:   {partial} ({100*partial//max(total,1)}%)\n"
        f"  Gap:       {gap} ({100*gap//max(total,1)}%)\n\n"
        "Per-SOP breakdown:\n" + "\n".join(sorted(results))
    )
    return summary
