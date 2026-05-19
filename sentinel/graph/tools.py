"""LangChain tools wrapping Sentinel's retrieval and auditing functions."""
from __future__ import annotations

import json
import logging
import time

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
RETRY_BACKOFF = 5

from sentinel.config import PINECONE_API_KEY, TAVILY_API_KEY
from sentinel.models import AuditFinding, ComplianceLevel, Severity

_audit_results: dict = {"findings": [], "cell_metrics": [], "total_input_tokens": 0, "total_output_tokens": 0}


def get_audit_results() -> dict:
    return _audit_results


def reset_audit_results() -> None:
    _audit_results["findings"] = []
    _audit_results["cell_metrics"] = []
    _audit_results["total_input_tokens"] = 0
    _audit_results["total_output_tokens"] = 0


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
def list_sops(query: str = "") -> str:
    """List all available SOPs.

    The optional `query` argument is a **literal lowercase substring filter** — it is NOT semantic search. A SOP is kept only when `query.lower()` appears verbatim inside the SOP title, SOP ID, or business unit. Paraphrases, synonyms, and natural-language descriptions will not match.

    Recommended discovery pattern: call `list_sops()` with no query to list all SOPs, then pick the one you want by reading the titles. Only pass a `query` when you already know a literal token that appears in the title/SOP ID/business unit (e.g. `"ISEC"`, `"incident"`, `"Clinical"`).
    """
    from sentinel.retrieval.local import list_all_sops

    all_sops = list_all_sops()
    if query:
        q = query.lower()
        all_sops = [s for s in all_sops if q in s["title"].lower() or q in s["sop_id"].lower() or q in s.get("business_unit", "").lower()]

    if not all_sops:
        return (
            f"No SOPs contain the literal substring '{query}' in their title, SOP ID, or business unit. "
            f"This tool is a literal substring filter, not semantic search — paraphrases and natural-language "
            f"descriptions will not match. Call list_sops() with no query to list all SOPs and pick by title, "
            f"or retry with a shorter literal token (e.g. a single word that likely appears verbatim in the title)."
        )

    lines = [f"- {s['sop_id']}: {s['title']} ({s.get('business_unit', '')})" for s in all_sops]
    return f"{len(all_sops)} SOPs:\n" + "\n".join(lines)


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


def _build_subagent_tools(sop_text: str, sop_id: str, sop_title: str, use_tavily: bool = True):
    """Build the tool set for the audit sub-agent."""

    @tool
    def retrieve_regulation(query: str = "", regulation: str = "") -> str:
        """Search the regulation knowledge base (Pinecone) for specific regulatory requirements. Use targeted queries like 'HIPAA access control requirements' or 'SOC 2 CC6 logical access'. Optionally filter by regulation name. The `query` argument is required and must be a non-empty search phrase."""
        if not isinstance(query, str) or not query.strip():
            return "Missing or empty 'query' argument — please re-issue with a specific search phrase"
        if not PINECONE_API_KEY:
            return "Pinecone not configured."
        try:
            from sentinel.retrieval.regulations import retrieve_regulation_text, format_regulation_context
            regs = [regulation] if regulation else None
            chunks = retrieve_regulation_text(query, regulations=regs, top_k=15)
            if not chunks:
                return f"No regulation text found for: {query}"
            context = format_regulation_context(chunks)
            return f"Retrieved {len(chunks)} sections:\n{context}"
        except Exception as e:
            return f"Retrieval failed: {e}"

    @tool
    def search_web(query: str = "") -> str:
        """Search the web via Tavily for latest regulatory guidance, enforcement actions, or interpretation. Use for questions the knowledge base can't answer — e.g. recent HHS enforcement, updated NIST guidance, or regulatory FAQs. The `query` argument is required and must be a non-empty search phrase."""
        if not isinstance(query, str) or not query.strip():
            return "Missing or empty 'query' argument — please re-issue with a specific search phrase"
        if not TAVILY_API_KEY:
            return "Tavily not configured — web search unavailable."
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=TAVILY_API_KEY)
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=3,
                include_answer=True,
            )
            parts = []
            if response.get("answer"):
                parts.append(f"Summary: {response['answer']}")
            for result in response.get("results", [])[:3]:
                parts.append(f"Source: {result.get('title', '')}\nURL: {result.get('url', '')}\n{result.get('content', '')[:500]}")
            return "\n\n".join(parts) if parts else "No results found."
        except Exception as e:
            return f"Web search failed: {e}"

    @tool
    def read_sop() -> str:
        """Read the full SOP text being audited. Call this to review the SOP content before or during your assessment."""
        return f"SOP: {sop_id} — {sop_title}\n\n{sop_text}"

    tools = [retrieve_regulation, read_sop]
    if use_tavily:
        tools.insert(1, search_web)
    return tools


_AUDIT_SUBAGENT_PROMPT = """You are an expert regulatory compliance auditor assessing a single SOP for Meridian Health Technologies, an AI-powered healthcare fintech company.

## Your Task
Audit the SOP against ALL applicable regulations. You must determine which regulations are relevant based on the SOP's content and business unit.

## Process
1. First, call `read_sop` to review the SOP content
2. Based on the SOP's subject matter, search the regulation knowledge base with targeted queries for each potentially applicable regulation (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California AI laws)
3. For each regulation that applies, retrieve the specific sections/requirements relevant to this SOP
4. If you need clarification on a regulation's current interpretation or recent enforcement, use `search_web`
5. Assess the SOP against each applicable requirement
6. Output your complete findings as a JSON array in your FINAL message

## Rules
- Every `retrieve_regulation` and `search_web` call MUST include a non-empty `query` argument. Never emit a tool call with empty `{}` args — if you have nothing specific to search for, don't call the tool. When issuing parallel tool calls, double-check that each call's argument dict contains a concrete `query` string.
- Be thorough: check EVERY regulation that could apply
- Be specific: cite exact regulatory sections
- Do NOT downgrade severity for aspirational language
- Skip regulations clearly irrelevant to this SOP's scope

## CRITICAL: Output Format
Your FINAL message MUST contain a JSON array (and nothing else) where each element has these exact fields:
- requirement_id: short identifier (e.g. "HIPAA-164.312(a)", "CC6.1", "GDPR-Art.32")
- requirement_title: brief title
- regulation: which regulation (e.g. "HIPAA", "SOC 2", "GDPR")
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP (empty string if none)
- gap_description: what is missing (empty string if compliant)
- remediation: specific recommendation (empty string if compliant)
- reasoning: 2-3 sentences citing the specific regulation section

Do NOT include any text before or after the JSON array in your final message. Just the raw JSON array."""


def _build_subagent_model(provider: str = "nebius"):
    """Build the ChatOpenAI model for audit sub-agents."""
    from langchain_openai import ChatOpenAI
    from sentinel.config import MODEL_MAX_TOKENS
    if provider == "openai":
        from sentinel.config import OPENAI_API_KEY, OPENAI_MODEL
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
            max_tokens=MODEL_MAX_TOKENS,
            stream_usage=True,
            metadata={"ls_provider": "openai", "ls_model_name": OPENAI_MODEL},
        )
    from sentinel.config import MODEL, NEBIUS_API_KEY, NEBIUS_BASE_URL
    return ChatOpenAI(
        model=MODEL,
        api_key=NEBIUS_API_KEY,
        base_url=NEBIUS_BASE_URL,
        temperature=0.1,
        max_tokens=MODEL_MAX_TOKENS,
        stream_usage=True,
        metadata={"ls_provider": "nebius", "ls_model_name": MODEL},
    )


def _audit_single_sop_impl(sop_id: str, provider: str = "nebius", use_tavily: bool = True) -> str:
    """Core implementation for auditing a single SOP."""
    from langgraph.prebuilt import create_react_agent
    from sentinel.retrieval.local import load_sop_by_id, load_sop_chunks

    sop = load_sop_by_id(sop_id)
    if sop is None:
        return f"SOP not found: {sop_id}"

    fm = sop["frontmatter"]
    chunks = load_sop_chunks(sop)
    if not chunks:
        return f"SOP {sop_id} has no content"

    actual_id = fm.get("sop_id", sop_id)
    title = fm.get("title", "")
    business_unit = fm.get("business_unit", "")
    sop_text = "\n\n---\n\n".join(f"[{c.section}]\n{c.chunk_text}" for c in chunks)

    subagent_tools = _build_subagent_tools(sop_text, actual_id, title, use_tavily=use_tavily)
    model = _build_subagent_model(provider)

    subagent = create_react_agent(
        model=model,
        tools=subagent_tools,
        prompt=_AUDIT_SUBAGENT_PROMPT,
        name="sop_auditor",
    )

    start = time.time()
    result = subagent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Audit SOP {actual_id}: {title} (Business Unit: {business_unit})",
        }],
    })
    elapsed = time.time() - start

    messages = result.get("messages", [])
    for msg in messages:
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            _audit_results["total_input_tokens"] += usage.get("input_tokens", 0)
            _audit_results["total_output_tokens"] += usage.get("output_tokens", 0)

    findings_json = ""

    for msg in reversed(messages):
        content = msg.content if hasattr(msg, "content") else str(msg)
        if not isinstance(content, str) or "[" not in content:
            continue

        if "```" in content:
            fence_start = content.find("```")
            lang_end = content.find("\n", fence_start)
            inner_start = lang_end + 1 if lang_end > fence_start else fence_start + 3
            fence_end = content.find("```", inner_start)
            if fence_end > inner_start:
                content = content[inner_start:fence_end].strip()

        start_idx = content.find("[")
        if start_idx < 0:
            continue

        candidate = content[start_idx:]
        end_idx = candidate.rfind("]")
        if end_idx > 0:
            candidate = candidate[: end_idx + 1]

        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                findings_json = candidate
                break
        except json.JSONDecodeError:
            repaired = candidate.rstrip().rstrip(",")
            if not repaired.endswith("}"):
                last_brace = repaired.rfind("}")
                if last_brace > 0:
                    repaired = repaired[: last_brace + 1]
            repaired += "]"
            try:
                parsed = json.loads(repaired)
                if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                    findings_json = repaired
                    break
            except json.JSONDecodeError:
                continue

    if not findings_json:
        return f"SOP {actual_id}: sub-agent did not produce structured findings"

    try:
        items = json.loads(findings_json)
    except json.JSONDecodeError:
        start_idx = findings_json.find("[")
        end_idx = findings_json.rfind("]") + 1
        if start_idx >= 0 and end_idx > start_idx:
            try:
                items = json.loads(findings_json[start_idx:end_idx])
            except json.JSONDecodeError:
                return f"SOP {actual_id}: failed to parse sub-agent findings"
        else:
            return f"SOP {actual_id}: failed to parse sub-agent findings"

    if not isinstance(items, list):
        items = [items]

    _COMPLIANCE_LEVEL_MAP = {
        "compliant": "compliant", "partial": "partial", "gap": "gap",
        "info": "compliant", "non-compliant": "gap", "non_compliant": "gap",
    }
    _SEVERITY_MAP = {
        "critical": "critical", "high": "high", "medium": "medium",
        "low": "low", "info": "info",
        "compliant": "info", "partial": "medium", "gap": "high",
    }

    findings = []
    for data in items:
        rid = data.get("requirement_id", data.get("clause_id", ""))
        raw_cl = data.get("compliance_level", "gap").lower().strip()
        raw_sev = data.get("severity", "high").lower().strip()
        try:
            findings.append(AuditFinding(
                clause_id=rid,
                clause_title=data.get("requirement_title", data.get("clause_title", "")),
                regulation=data.get("regulation", ""),
                sop_id=actual_id,
                sop_title=title,
                business_unit=business_unit,
                compliance_level=ComplianceLevel(_COMPLIANCE_LEVEL_MAP.get(raw_cl, "gap")),
                severity=Severity(_SEVERITY_MAP.get(raw_sev, "high")),
                evidence_quote=data.get("evidence_quote", ""),
                gap_description=data.get("gap_description", ""),
                remediation=data.get("remediation", ""),
                reasoning=data.get("reasoning", ""),
            ))
        except (ValueError, KeyError):
            continue

    for f in findings:
        _audit_results["findings"].append(f)
    _audit_results["cell_metrics"].append({
        "sop_id": actual_id,
        "findings": len(findings),
        "latency": elapsed,
    })

    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    sub_in = sum(
        getattr(m, "usage_metadata", {}).get("input_tokens", 0)
        for m in messages if getattr(m, "usage_metadata", None)
    )
    sub_out = sum(
        getattr(m, "usage_metadata", {}).get("output_tokens", 0)
        for m in messages if getattr(m, "usage_metadata", None)
    )

    lines = [f"{actual_id} ({title}): {len(findings)} findings — {compliant}C/{partial}P/{gap}G"]
    for f in findings:
        lines.append(f"  {f.clause_id}: {f.compliance_level.value} ({f.severity.value}) — {f.gap_description or 'Compliant'}")
    lines.append(f"Sub-agent tokens: {sub_in + sub_out:,} ({sub_in:,} in / {sub_out:,} out)")
    return "\n".join(lines)


@tool
def audit_single_sop(sop_id: str) -> str:
    """Audit one SOP against all relevant regulations using a sub-agent with access to the regulation knowledge base (Pinecone) and web search (Tavily). Accepts an SOP ID (e.g. 'SOP-AIML-009') or title (e.g. 'Algorithmic Bias Detection'). The sub-agent determines which regulations apply and iteratively retrieves regulatory text."""
    result = _audit_single_sop_impl(sop_id, provider="nebius", use_tavily=True)
    for attempt in range(1, MAX_RETRIES + 1):
        if not _is_retryable(result):
            break
        logger.info("Retry attempt %d/%d for %s", attempt, MAX_RETRIES, sop_id)
        time.sleep(RETRY_BACKOFF * attempt)
        result = _audit_single_sop_impl(sop_id, provider="nebius", use_tavily=True)
    return result


def _is_retryable(result: str) -> bool:
    """Check if a single-SOP audit result indicates a retryable failure."""
    return (
        "FAILED" in result
        or "sub-agent did not produce structured findings" in result
        or "failed to parse sub-agent findings" in result
    )


def _audit_all_sops_impl(single_sop_tool, max_workers: int | None = None) -> str:
    """Core implementation for auditing all SOPs."""
    import concurrent.futures
    from sentinel.config import MAX_AUDIT_WORKERS
    from sentinel.retrieval.local import list_all_sops

    workers = max_workers or MAX_AUDIT_WORKERS
    all_sops = list_all_sops()
    sop_by_id = {s["sop_id"]: s for s in all_sops}

    def _audit_one(sop_meta: dict) -> str:
        sid = sop_meta["sop_id"]
        try:
            return single_sop_tool.invoke(sid)
        except Exception as e:
            return f"{sid}: FAILED — {e}"

    results_by_id: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_audit_one, s): s["sop_id"] for s in all_sops}
        for future in concurrent.futures.as_completed(futures):
            sid = futures[future]
            results_by_id[sid] = future.result()

    for attempt in range(1, MAX_RETRIES + 1):
        to_retry = [sid for sid, r in results_by_id.items() if _is_retryable(r)]
        if not to_retry:
            break
        logger.info("Retry attempt %d/%d for %d SOPs: %s", attempt, MAX_RETRIES, len(to_retry), ", ".join(to_retry))
        time.sleep(RETRY_BACKOFF * attempt)
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(to_retry))) as executor:
            futures = {executor.submit(_audit_one, sop_by_id[sid]): sid for sid in to_retry}
            for future in concurrent.futures.as_completed(futures):
                sid = futures[future]
                new_result = future.result()
                if not _is_retryable(new_result):
                    logger.info("Retry succeeded for %s", sid)
                results_by_id[sid] = new_result

    results = list(results_by_id.values())
    still_failed = sum(1 for r in results if _is_retryable(r))

    findings = _audit_results["findings"]
    total = len(findings)
    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gap = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    tok_in = _audit_results["total_input_tokens"]
    tok_out = _audit_results["total_output_tokens"]

    summary = (
        f"Audit complete: {total} findings across {len(all_sops)} SOPs\n"
        f"  Compliant: {compliant} ({100*compliant//max(total,1)}%)\n"
        f"  Partial:   {partial} ({100*partial//max(total,1)}%)\n"
        f"  Gap:       {gap} ({100*gap//max(total,1)}%)\n"
        f"  Sub-agent tokens: {tok_in + tok_out:,} ({tok_in:,} in / {tok_out:,} out)\n"
        f"  Failed after retries: {still_failed}\n\n"
        "Per-SOP breakdown:\n" + "\n".join(sorted(results))
    )
    return summary


@tool
def audit_all_sops() -> str:
    """Run the full audit across ALL SOPs using sub-agents. Each SOP gets its own auditor sub-agent with access to the regulation knowledge base and web search. Fans out with configurable parallelism (MAX_AUDIT_WORKERS)."""
    return _audit_all_sops_impl(audit_single_sop)


def build_tools(provider: str = "nebius", use_tavily: bool = True) -> list:
    """Build the complete tool list for the agent, parameterized by provider and Tavily usage."""

    @tool
    def _audit_single_sop(sop_id: str) -> str:
        """Audit one SOP against all relevant regulations using a sub-agent with access to the regulation knowledge base (Pinecone). Accepts an SOP ID (e.g. 'SOP-AIML-009') or title (e.g. 'Algorithmic Bias Detection'). The sub-agent determines which regulations apply and iteratively retrieves regulatory text."""
        result = _audit_single_sop_impl(sop_id, provider=provider, use_tavily=use_tavily)
        for attempt in range(1, MAX_RETRIES + 1):
            if not _is_retryable(result):
                break
            logger.info("Retry attempt %d/%d for %s", attempt, MAX_RETRIES, sop_id)
            time.sleep(RETRY_BACKOFF * attempt)
            result = _audit_single_sop_impl(sop_id, provider=provider, use_tavily=use_tavily)
        return result

    @tool
    def _audit_all_sops() -> str:
        """Run the full audit across ALL SOPs using sub-agents. Each SOP gets its own auditor sub-agent with access to the regulation knowledge base. Fans out with configurable parallelism (MAX_AUDIT_WORKERS)."""
        return _audit_all_sops_impl(_audit_single_sop)

    _audit_single_sop.name = "audit_single_sop"
    _audit_all_sops.name = "audit_all_sops"

    return [list_sops, list_regulations, retrieve_regulation_text_tool, _audit_single_sop, _audit_all_sops]
