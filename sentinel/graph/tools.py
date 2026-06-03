"""LangChain tools wrapping Sentinel's retrieval and auditing functions."""
from __future__ import annotations

import json
import logging
import re
import threading
import time

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

MAX_RETRIES = 4
RETRY_BACKOFF = 5
RATE_LIMIT_BACKOFF = 30

from sentinel.config import NEXUS_API_KEY, PINECONE_API_KEY, TAVILY_API_KEY
from sentinel.models import AuditFinding, ComplianceLevel, Severity

_audit_results: dict = {"findings": [], "cell_metrics": [], "total_input_tokens": 0, "total_output_tokens": 0}

_shared_http_client = None
_http_client_lock = threading.Lock()


def _get_shared_http_client():
    """Return a process-wide httpx.Client with connection pooling.

    httpx.Client is thread-safe, so all ThreadPoolExecutor workers share one
    pool.  DNS is resolved once per hostname and TCP connections are reused
    across SOP audits, eliminating the DNS-exhaustion failures seen under high
    concurrency.
    """
    global _shared_http_client
    if _shared_http_client is not None:
        return _shared_http_client
    with _http_client_lock:
        if _shared_http_client is None:
            import httpx

            _shared_http_client = httpx.Client(
                limits=httpx.Limits(
                    max_connections=200,
                    max_keepalive_connections=100,
                    keepalive_expiry=120,
                ),
                timeout=httpx.Timeout(600.0, connect=30.0),
            )
    return _shared_http_client


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
        from sentinel.retrieval.ingest_regulations import REGULATION_MAP
        from pinecone import Pinecone

        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)

        known_regs = sorted(set(REGULATION_MAP.values()))
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


_LIST_SOPS_SYNONYMS = {
    "fda": "clinical ai products",
    "samd": "clinical ai products",
    "medical device": "clinical ai products",
    "ai/ml": "ai/ml engineering",
    "ai ml": "ai/ml engineering",
    "machine learning": "ai/ml engineering",
    "algorithm": "ai/ml engineering",
}


@tool
def list_sops(query: str = "") -> str:
    """List all available SOPs. Pass an empty query (the default) to return ALL SOPs in a single call — use this for broad discovery questions instead of guessing keywords. Optionally filter by a search query (matches title, SOP ID, or business unit substring). Available business units: 'AI/ML Engineering' (SOP-AIML-*), 'Clinical AI Products' (SOP-CLIN-*), 'Customer Operations' (SOP-COPS-*), 'Data Governance & Privacy' (SOP-DGP-*), 'Financial Services' (SOP-FIN-*), 'Human Resources' (SOP-HR-*), 'Information Security' (SOP-ISEC-*), 'IT Operations & Infrastructure' (SOP-ITOP-*), 'Legal & Compliance' (SOP-LEGC-*), 'Product & Engineering' (SOP-PENG-*)."""
    from sentinel.retrieval.local import list_all_sops

    all_sops = list_all_sops()
    if query:
        q = query.lower()
        expanded = _LIST_SOPS_SYNONYMS.get(q, q)
        all_sops = [
            s for s in all_sops
            if q in s["title"].lower()
            or q in s["sop_id"].lower()
            or q in s.get("business_unit", "").lower()
            or expanded in s.get("business_unit", "").lower()
        ]

    if not all_sops:
        return f"No SOPs found matching '{query}'"

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


@tool
def search_web(query: str = "") -> str:
    """Search the web via Tavily for latest regulatory guidance, enforcement actions, or interpretation. Use for questions the static knowledge base can't answer — e.g. recent HHS OCR enforcement, FDA AI/ML device guidance, EU AI Office codes of practice, EDPB decisions, OCC bulletins. The `query` argument is required and must be a non-empty search phrase."""
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


def _build_subagent_tools(sop_text: str, sop_id: str, sop_title: str, use_tavily: bool = True, retrieval: str = "rag"):
    """Build the tool set for the audit sub-agent.

    Returns (tools, recorded_findings) where recorded_findings is a mutable
    list populated by the record_finding tool during execution.
    """
    recorded_findings: list[dict] = []
    _retrieval_calls = {"count": 0, "limit": 30}

    @tool
    def record_finding(
        requirement_id: str,
        requirement_title: str,
        regulation: str,
        compliance_level: str = "",
        severity: str = "",
        reasoning: str = "",
        evidence_quote: str = "",
        gap_description: str = "",
        remediation: str = "",
        compliance_status: str = "",
        finding: str = "",
        sop_reference: str = "",
    ) -> str:
        """Record a single audit finding. Call this IMMEDIATELY after assessing each requirement — do NOT wait until the end. Each call saves one finding."""
        if not compliance_level and compliance_status:
            logger.warning("record_finding: aliasing 'compliance_status' -> 'compliance_level' (prompt schema drift)")
            compliance_level = compliance_status
        if not reasoning and finding:
            logger.warning("record_finding: aliasing 'finding' -> 'reasoning' (prompt schema drift)")
            reasoning = finding
        if sop_reference:
            logger.warning("record_finding: dropping unsupported 'sop_reference' arg (prompt schema drift)")
        if not compliance_level:
            return "Missing required 'compliance_level'. Must be one of: compliant, partial, gap"
        if not severity:
            return "Missing required 'severity'. Must be one of: critical, high, medium, low, info"
        if not reasoning:
            return "Missing required 'reasoning'. Provide 2-3 sentences citing the specific regulation section."
        valid_levels = {"compliant", "partial", "gap"}
        valid_sevs = {"critical", "high", "medium", "low", "info"}
        cl = compliance_level.lower().strip()
        sev = severity.lower().strip()
        if cl not in valid_levels:
            return f"Invalid compliance_level '{compliance_level}'. Must be one of: {', '.join(sorted(valid_levels))}"
        if sev not in valid_sevs:
            return f"Invalid severity '{severity}'. Must be one of: {', '.join(sorted(valid_sevs))}"
        recorded_findings.append({
            "requirement_id": requirement_id,
            "requirement_title": requirement_title,
            "regulation": regulation,
            "compliance_level": cl,
            "severity": sev,
            "evidence_quote": evidence_quote or "",
            "gap_description": gap_description or "",
            "remediation": remediation or "",
            "reasoning": reasoning,
        })
        return f"Recorded finding #{len(recorded_findings)}: {requirement_id} ({regulation}) — {cl}/{sev}"

    @tool
    def retrieve_regulation_rag(query: str = "", regulation: str = "") -> str:
        """Search the Pinecone vector store for regulation text chunks via semantic similarity. Use targeted queries like 'HIPAA access control requirements' or 'SOC 2 CC6 logical access'. Optionally filter by regulation name. The `query` argument is required and must be a non-empty search phrase."""
        if _retrieval_calls["count"] >= _retrieval_calls["limit"]:
            return f"Retrieval limit reached ({_retrieval_calls['limit']} calls). Record your findings now with record_finding and finish the audit."
        _retrieval_calls["count"] += 1
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
            return f"RAG retrieval failed: {e}"

    @tool
    def retrieve_regulation_nexus(query: str = "", regulation: str = "") -> str:
        """Query Pinecone Nexus for regulation requirements using natural-language questions. Ask things like 'What does HIPAA require for access controls?' or 'What are the SOC 2 CC6.1 requirements for logical access?'. Optionally specify a regulation name to focus the query. The `query` argument is required and must be a non-empty search phrase."""
        if _retrieval_calls["count"] >= _retrieval_calls["limit"]:
            return f"Retrieval limit reached ({_retrieval_calls['limit']} calls). Record your findings now with record_finding and finish the audit."
        _retrieval_calls["count"] += 1
        if not isinstance(query, str) or not query.strip():
            return "Missing or empty 'query' argument — please re-issue with a specific search phrase"
        if not NEXUS_API_KEY:
            return "Nexus not configured — set NEXUS_API_KEY."
        try:
            from sentinel.retrieval.nexus import query_nexus, format_nexus_response
            ask = f"{regulation}: {query}" if regulation else query
            data = query_nexus(ask)
            if data.get("state") != "completed":
                return f"Nexus query failed: {data.get('state', 'unknown')}"
            return format_nexus_response(data)
        except Exception as e:
            return f"Nexus retrieval failed: {e}"

    @tool
    def read_sop() -> str:
        """Read the full SOP text being audited. Call this to review the SOP content before or during your assessment."""
        return f"SOP: {sop_id} — {sop_title}\n\n{sop_text}"

    @tool
    def _search_web_capped(query: str = "") -> str:
        """Search the web for current regulatory guidance, enforcement actions, or recent developments. Use when you need information beyond the static knowledge base."""
        if _retrieval_calls["count"] >= _retrieval_calls["limit"]:
            return f"Retrieval limit reached ({_retrieval_calls['limit']} calls). Record your findings now with record_finding and finish the audit."
        _retrieval_calls["count"] += 1
        return search_web.invoke({"query": query})
    _search_web_capped.name = "search_web"

    tools = [read_sop, record_finding]
    if retrieval in ("nexus", "both") and NEXUS_API_KEY:
        tools.insert(0, retrieve_regulation_nexus)
    if retrieval in ("rag", "both") and PINECONE_API_KEY:
        tools.insert(0, retrieve_regulation_rag)
    if use_tavily:
        tools.append(_search_web_capped)
    return tools, recorded_findings


_AUDIT_SUBAGENT_PROMPT_RAG = """You are an expert regulatory compliance auditor assessing a single SOP for Meridian Health Technologies, an AI-powered healthcare fintech company.

## Your Task
Audit the SOP against ALL applicable regulations. You must determine which regulations are relevant based on the SOP's content and business unit.

## Process
1. First, call `read_sop` to review the SOP content
2. Based on the SOP's subject matter, search the regulation knowledge base with targeted queries for each potentially applicable regulation (HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, California AI laws)
3. For each regulation that applies, retrieve the specific sections/requirements relevant to this SOP
4. If you need clarification on a regulation's current interpretation or recent enforcement, use `search_web`
5. Assess the SOP against each applicable requirement. After completing each assessment, IMMEDIATELY call `record_finding` with the result — do not wait until the end.
6. After all requirements are assessed, output a single short sentence summarizing counts (e.g. "Done — 12 findings recorded."). Do NOT repeat findings in your final message.

## Rules
- Every `retrieve_regulation_rag` and `search_web` call MUST include a non-empty `query` argument. Never emit a tool call with empty `{}` args — if you have nothing specific to search for, don't call the tool. When issuing parallel tool calls, double-check that each call's argument dict contains a concrete `query` string.
- Be thorough: check EVERY regulation that could apply
- Be specific: cite exact regulatory sections
- Be efficient: you have a budget of ~30 retrieval calls total. Use 2–4 targeted queries per regulation, not dozens. Once you have enough context for a regulation, record your findings and move on.
- Do NOT downgrade severity for aspirational language
- Skip regulations clearly irrelevant to this SOP's scope
- If a retrieval tool call fails (returns an error), do NOT cite that regulation's requirements from memory. Only record findings based on text you successfully retrieved. State that retrieval failed in your summary.

## CRITICAL: Output Method
For EACH requirement you assess, IMMEDIATELY call `record_finding` with these fields:
- requirement_id: short identifier (e.g. "HIPAA-164.312(a)", "CC6.1", "GDPR-Art.32")
- requirement_title: brief title
- regulation: which regulation (e.g. "HIPAA", "SOC 2", "GDPR")
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP (empty string if none)
- gap_description: what is missing (empty string if compliant)
- remediation: specific recommendation (empty string if compliant)
- reasoning: 2-3 sentences citing the specific regulation section

The argument keys MUST be exactly these names — not `compliance_status`, not `finding`, not `sop_reference`. Example tool-call payload:
{
  "requirement_id": "HIPAA-164.312(a)",
  "requirement_title": "Access Control",
  "regulation": "HIPAA",
  "compliance_level": "partial",
  "severity": "high",
  "evidence_quote": "...",
  "gap_description": "...",
  "remediation": "...",
  "reasoning": "..."
}

Call `record_finding` ONCE PER REQUIREMENT as you go. Do NOT accumulate findings for a batch output.
After calling `record_finding` for every requirement, your FINAL message should be a single short sentence (e.g. "Done — 12 findings recorded."). Do NOT list findings in your final message — the harness reads them from record_finding calls."""

_AUDIT_SUBAGENT_PROMPT_NEXUS = """You are an expert regulatory compliance auditor assessing a single SOP for Meridian Health Technologies, an AI-powered healthcare fintech company.

## Your Task
Audit the SOP against ALL applicable regulations. You must determine which regulations are relevant based on the SOP's content and business unit.

## Knowledge base
You have access to a Nexus knowledge base containing 50 regulatory source documents covering:
- **Core frameworks**: HIPAA (45 CFR Parts 160/162/164, multiple editions), SOC 2 (Trust Services Criteria + Description Criteria), GDPR (full article-by-article), EU AI Act (current + 2021 proposal), NIST AI RMF (AI 100-1 + AI 600-1 GenAI Profile), SR 11-7/SR 26-2 (Model Risk Management), California SB 53/SB 942/AB 853
- **NIST publications**: CSF 2.0, SP 800-53 Rev 5, 800-88, 800-61, 800-63B, 800-207, 800-34, 800-161, 800-218, SP 1270, Privacy Framework 1.0
- **Healthcare/FDA**: 21 CFR Part 11 (electronic records), Part 807, Part 820 (QSR), AI/ML SaMD framework, Clinical Decision Support guidance, EU MDR 2017/745
- **Financial/security**: BSA, ECOA (Reg B), FCRA, PCI DSS, AMLD4, OWASP Top 10, OWASP API Security Top 10

Nexus returns grounded, cited answers with inline citation markers ([c1], [c2], etc.) referencing the source documents. Each answer is synthesized from the actual regulation text — not a summary.

## How to query Nexus effectively
Use `retrieve_regulation_nexus` to query the knowledge base. Nexus works best with:

1. **Natural-language questions, not keyword searches.**
   - Good: "What does 45 CFR 164.312(a) require for access control to electronic PHI?"
   - Good: "Under SOC 2 CC6.1, what controls must an entity implement for logical access?"
   - Bad: "HIPAA access control requirements" (too vague for Nexus)

2. **Include structural locators** (article numbers, CFR sections, criterion codes) when you know them — this produces the most precise answers.
   - "What exactly does GDPR Article 32 require for security of processing?"
   - "What does SOC 2 Common Criterion CC6.1 address?"

3. **Ask narrow, focused questions.** One specific requirement per query outperforms broad requests. If you need to check multiple sections of a regulation, make separate calls.
   - Instead of: "List all HIPAA Security Rule safeguards"
   - Prefer: "What administrative safeguards does 45 CFR 164.308 require?" + "What technical safeguards does 45 CFR 164.312 require?"

4. **Cross-framework synthesis works in a single query.** When an SOP touches multiple regulations, you can ask Nexus to compare requirements across frameworks.
   - "Compare breach notification requirements under HIPAA 45 CFR 164.404 and GDPR Article 33. Cite each."
   - "What access control requirements apply under both HIPAA 164.312(a) and SOC 2 CC6.1?"

5. **Temporal/edition queries are supported.** The corpus includes multiple editions (HIPAA 2017/2020/2024, SR 11-7 2011 vs SR 26-2 2026). Ask about differences when relevant.

## Process
1. Call `read_sop` to review the SOP content
2. Determine which regulations apply based on the SOP's subject matter and business unit
3. Query Nexus with specific, natural-language questions for each applicable regulation's requirements — cite structural locators when you know them. You may combine related regulations into a single cross-framework query.
4. If you need the latest enforcement actions or guidance beyond the static corpus, use `search_web`
5. Assess the SOP against each applicable requirement, preserving inline citations ([c1], [c2]) from Nexus in your reasoning. After completing each assessment, IMMEDIATELY call `record_finding` with the result — do not wait until the end.
6. After all requirements are assessed, output a single short sentence summarizing counts (e.g. "Done — 12 findings recorded."). Do NOT repeat findings in your final message.

## Rules
- Every `retrieve_regulation_nexus` and `search_web` call MUST include a non-empty `query` argument. Never emit a tool call with empty `{}` args. When issuing parallel tool calls, double-check that each call's argument dict contains a concrete `query` string.
- Be thorough: check EVERY regulation that could apply — including supplementary frameworks (NIST SP 800-series, OWASP, PCI DSS, FDA/21 CFR) when the SOP's subject matter warrants it
- Be specific: cite the exact regulatory section returned by Nexus (preserve [c1]/[c2] markers)
- Be efficient: you have a budget of ~30 retrieval calls total. Use 1–3 targeted Nexus queries per regulation. Once you have enough context, record your findings and move on.
- Do NOT downgrade severity for aspirational language
- Skip regulations clearly irrelevant to this SOP's scope
- If a retrieval tool call fails (returns an error), do NOT cite that regulation's requirements from memory. Only record findings based on text you successfully retrieved. State that retrieval failed in your summary.

## CRITICAL: Output Method
For EACH requirement you assess, IMMEDIATELY call `record_finding` with these fields:
- requirement_id: short identifier (e.g. "HIPAA-164.312(a)", "CC6.1", "GDPR-Art.32")
- requirement_title: brief title
- regulation: which regulation (e.g. "HIPAA", "SOC 2", "GDPR")
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP (empty string if none)
- gap_description: what is missing (empty string if compliant)
- remediation: specific recommendation (empty string if compliant)
- reasoning: 2-3 sentences citing the specific regulation section

The argument keys MUST be exactly these names — not `compliance_status`, not `finding`, not `sop_reference`. Example tool-call payload:
{
  "requirement_id": "HIPAA-164.312(a)",
  "requirement_title": "Access Control",
  "regulation": "HIPAA",
  "compliance_level": "partial",
  "severity": "high",
  "evidence_quote": "...",
  "gap_description": "...",
  "remediation": "...",
  "reasoning": "..."
}

Call `record_finding` ONCE PER REQUIREMENT as you go. Do NOT accumulate findings for a batch output.
After calling `record_finding` for every requirement, your FINAL message should be a single short sentence (e.g. "Done — 12 findings recorded."). Do NOT list findings in your final message — the harness reads them from record_finding calls."""


_AUDIT_SUBAGENT_PROMPT_NEXUS_RAG = """You are an expert regulatory compliance auditor assessing a single SOP for Meridian Health Technologies, an AI-powered healthcare fintech company.

## Your Task
Audit the SOP against ALL applicable regulations. You must determine which regulations are relevant based on the SOP's content and business unit.

## Knowledge base — two retrieval tools
You have two regulation retrieval tools. Use whichever is most effective for each query, or both for cross-validation:

### `retrieve_regulation_nexus` (Nexus KnowQL — grounded answers)
Nexus contains 50 regulatory source documents and returns grounded, cited answers with inline citation markers ([c1], [c2], etc.). Best for:
- Natural-language questions: "What does 45 CFR 164.312(a) require for access control to electronic PHI?"
- Cross-framework synthesis: "Compare breach notification requirements under HIPAA 45 CFR 164.404 and GDPR Article 33."
- Questions that include structural locators (article numbers, CFR sections, criterion codes)

Corpus covers: HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7/SR 26-2, California SB 53/SB 942/AB 853, NIST SP 800-series, FDA/21 CFR, OWASP, PCI DSS, BSA, ECOA, FCRA, EU MDR, EU SCCs, EU ePrivacy, AMLD4.

### `retrieve_regulation_rag` (Pinecone RAG — semantic search)
Searches chunked regulation text via vector similarity. Best for:
- Keyword-oriented searches: "HIPAA encryption key management HSM technical safeguards"
- Broad discovery: finding which sections mention a concept when you don't know the exact provision
- Retrieving raw regulation text chunks with section metadata

Optionally filter by regulation name for precision.

### When to use which
- **Start with Nexus** for most queries — it returns synthesized, cited answers
- **Use RAG** when Nexus returns sparse results, or when you want the raw text of a specific regulation section
- **Cross-validate** critical findings by querying both tools to confirm coverage

## Process
1. Call `read_sop` to review the SOP content
2. Determine which regulations apply based on the SOP's subject matter and business unit
3. Query for each applicable regulation's requirements using `retrieve_regulation_nexus` and/or `retrieve_regulation_rag`
4. If you need the latest enforcement actions or guidance beyond the static corpus, use `search_web`
5. Assess the SOP against each applicable requirement, preserving inline citations ([c1], [c2]) from Nexus in your reasoning. After completing each assessment, IMMEDIATELY call `record_finding` with the result — do not wait until the end.
6. After all requirements are assessed, output a single short sentence summarizing counts (e.g. "Done — 12 findings recorded."). Do NOT repeat findings in your final message.

## Rules
- Every `retrieve_regulation_nexus`, `retrieve_regulation_rag`, and `search_web` call MUST include a non-empty `query` argument. Never emit a tool call with empty `{}` args. When issuing parallel tool calls, double-check that each call's argument dict contains a concrete `query` string.
- Be thorough: check EVERY regulation that could apply — including supplementary frameworks (NIST SP 800-series, OWASP, PCI DSS, FDA/21 CFR) when the SOP's subject matter warrants it
- Be specific: cite the exact regulatory section returned by Nexus (preserve [c1]/[c2] markers) or RAG (section metadata)
- Be efficient: you have a budget of ~30 retrieval calls total. Use 1–3 targeted queries per regulation. Once you have enough context, record your findings and move on.
- Do NOT downgrade severity for aspirational language
- Skip regulations clearly irrelevant to this SOP's scope
- If a retrieval tool call fails (returns an error), do NOT cite that regulation's requirements from memory. Only record findings based on text you successfully retrieved. State that retrieval failed in your summary.

## CRITICAL: Output Method
For EACH requirement you assess, IMMEDIATELY call `record_finding` with these fields:
- requirement_id: short identifier (e.g. "HIPAA-164.312(a)", "CC6.1", "GDPR-Art.32")
- requirement_title: brief title
- regulation: which regulation (e.g. "HIPAA", "SOC 2", "GDPR")
- compliance_level: "compliant" | "partial" | "gap"
- severity: "critical" | "high" | "medium" | "low" | "info"
- evidence_quote: exact quote from the SOP (empty string if none)
- gap_description: what is missing (empty string if compliant)
- remediation: specific recommendation (empty string if compliant)
- reasoning: 2-3 sentences citing the specific regulation section

The argument keys MUST be exactly these names — not `compliance_status`, not `finding`, not `sop_reference`. Example tool-call payload:
{
  "requirement_id": "HIPAA-164.312(a)",
  "requirement_title": "Access Control",
  "regulation": "HIPAA",
  "compliance_level": "partial",
  "severity": "high",
  "evidence_quote": "...",
  "gap_description": "...",
  "remediation": "...",
  "reasoning": "..."
}

Call `record_finding` ONCE PER REQUIREMENT as you go. Do NOT accumulate findings for a batch output.
After calling `record_finding` for every requirement, your FINAL message should be a single short sentence (e.g. "Done — 12 findings recorded."). Do NOT list findings in your final message — the harness reads them from record_finding calls."""


def _build_subagent_model(provider: str = "nebius", model_name: str | None = None):
    """Build the ChatOpenAI model for audit sub-agents.

    All instances share a single httpx.Client via ``_get_shared_http_client()``
    so that ThreadPoolExecutor workers reuse one connection pool instead of each
    creating their own (which caused DNS-exhaustion failures at 50 workers).
    """
    from langchain_openai import ChatOpenAI
    from sentinel.config import MODEL_MAX_TOKENS, REASONING_EFFORT
    extra_kwargs: dict = {}
    if REASONING_EFFORT != "off" and provider != "openai":
        extra_kwargs["extra_body"] = {
            "chat_template_kwargs": {"thinking": True, "reasoning_effort": REASONING_EFFORT},
        }
    http_client = _get_shared_http_client()
    if provider == "openai":
        from sentinel.config import OPENAI_API_KEY, OPENAI_MODEL
        name = model_name or OPENAI_MODEL
        return ChatOpenAI(
            model=name,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
            max_tokens=MODEL_MAX_TOKENS,
            stream_usage=True,
            http_client=http_client,
            metadata={"ls_provider": "openai", "ls_model_name": name},
            **extra_kwargs,
        )
    from sentinel.config import MODEL, NEBIUS_API_KEY, NEBIUS_BASE_URL, NEBIUS_TESTING_API_KEY, NEBIUS_TESTING_BASE_URL
    name = model_name or MODEL
    is_testing = "Nemotron" in name
    kwargs = dict(
        model=name,
        api_key=NEBIUS_TESTING_API_KEY if is_testing else NEBIUS_API_KEY,
        base_url=NEBIUS_TESTING_BASE_URL if is_testing else NEBIUS_BASE_URL,
        temperature=0.1,
        stream_usage=True,
        http_client=http_client,
        metadata={"ls_provider": "nebius", "ls_model_name": name},
        **extra_kwargs,
    )
    if "DeepSeek" in name:
        kwargs["max_tokens"] = MODEL_MAX_TOKENS
    return ChatOpenAI(**kwargs)


def _parse_findings_json(messages) -> str | None:
    """Extract a JSON findings array from sub-agent messages (backwards compat fallback)."""
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
                return candidate
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
                    return repaired
            except json.JSONDecodeError:
                continue
    return None


def _audit_single_sop_impl(sop_id: str, provider: str = "nebius", use_tavily: bool = True, retrieval: str = "rag", model_name: str | None = None) -> str:
    """Core implementation for auditing a single SOP."""
    from langchain.agents import create_agent
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

    subagent_tools, recorded_findings = _build_subagent_tools(sop_text, actual_id, title, use_tavily=use_tavily, retrieval=retrieval)
    model = _build_subagent_model(provider, model_name=model_name)

    if retrieval == "both":
        prompt = _AUDIT_SUBAGENT_PROMPT_NEXUS_RAG
    elif retrieval == "nexus":
        prompt = _AUDIT_SUBAGENT_PROMPT_NEXUS
    else:
        prompt = _AUDIT_SUBAGENT_PROMPT_RAG
    subagent = create_agent(
        model=model,
        tools=subagent_tools,
        system_prompt=prompt,
        name="sop_auditor",
    )

    start = time.time()
    result = None
    try:
        result = subagent.invoke(
            {
                "messages": [{
                    "role": "user",
                    "content": f"Audit SOP {actual_id}: {title} (Business Unit: {business_unit})",
                }],
            },
            config={"recursion_limit": 80},
        )
    except Exception as e:
        elapsed = time.time() - start
        logger.error("Sub-agent for %s failed after %.1fs: %s", actual_id, elapsed, e)
        if not recorded_findings:
            return f"FAILED: {actual_id} — sub-agent error: {e}"
        logger.info("%s: sub-agent errored but %d findings were recorded via tool", actual_id, len(recorded_findings))
    elapsed = time.time() - start

    messages = result.get("messages", []) if result else []
    for msg in messages:
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            _audit_results["total_input_tokens"] += usage.get("input_tokens", 0)
            _audit_results["total_output_tokens"] += usage.get("output_tokens", 0)

    # Detect truncation from the last AI message
    truncated = False
    for msg in reversed(messages):
        if getattr(msg, "type", "") == "ai":
            rm = getattr(msg, "response_metadata", None) or {}
            if isinstance(rm, dict) and rm.get("finish_reason") == "length":
                truncated = True
                logger.warning("Sub-agent for %s was truncated (finish_reason=length)", actual_id)
            content = getattr(msg, "content", None)
            if not truncated and (content is None or content == ""):
                truncated = True
                logger.warning("Sub-agent for %s produced empty final message (likely truncated)", actual_id)
            break

    # Phase 1: Use tool-recorded findings if available
    items = []
    findings_source = "none"

    if recorded_findings:
        items = list(recorded_findings)
        findings_source = "tool"
        logger.info("%s: %d findings recorded via record_finding tool", actual_id, len(items))

    # Phase 2: Fall back to JSON parsing from messages (backwards compat)
    if not items:
        findings_json = _parse_findings_json(messages)
        if findings_json:
            try:
                parsed = json.loads(findings_json)
                if isinstance(parsed, list):
                    items = parsed
                else:
                    items = [parsed]
                findings_source = "json"
            except json.JSONDecodeError:
                pass

    if not items:
        suffix = " (response was truncated)" if truncated else ""
        return f"SOP {actual_id}: sub-agent did not produce structured findings{suffix}"

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
        "findings_source": findings_source,
        "truncated": truncated,
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
        delay = _retry_delay(attempt, result)
        logger.info("Retry attempt %d/%d for %s (waiting %.0fs)", attempt, MAX_RETRIES, sop_id, delay)
        time.sleep(delay)
        result = _audit_single_sop_impl(sop_id, provider="nebius", use_tavily=True)
    return result


def _is_retryable(result: str) -> bool:
    """Check if a single-SOP audit result indicates a retryable failure.

    Truncation is NOT retryable — it will just truncate again.
    """
    if "response was truncated" in result:
        return False
    return (
        "FAILED" in result
        or "sub-agent did not produce structured findings" in result
        or "failed to parse sub-agent findings" in result
    )


def _is_rate_limited(result: str) -> bool:
    return "429" in result or "exceeded" in result.lower() or "quota" in result.lower() or "rate" in result.lower()


def _retry_delay(attempt: int, result: str) -> float:
    """Compute retry delay with jitter. Longer for rate limits."""
    import random
    base = RATE_LIMIT_BACKOFF if _is_rate_limited(result) else RETRY_BACKOFF
    delay = base * attempt
    return delay + random.uniform(0, delay * 0.5)


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
        any_rate_limited = any(_is_rate_limited(results_by_id[sid]) for sid in to_retry)
        delay = _retry_delay(attempt, "429" if any_rate_limited else "FAILED")
        logger.info("Retry attempt %d/%d for %d SOPs (waiting %.0fs): %s", attempt, MAX_RETRIES, len(to_retry), delay, ", ".join(to_retry))
        time.sleep(delay)
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
        f"  Total tokens: {tok_in + tok_out:,} ({tok_in:,} in / {tok_out:,} out)\n"
        f"  Failed after retries: {still_failed}\n\n"
        "Per-SOP breakdown:\n" + "\n".join(sorted(results))
    )
    return summary


@tool
def audit_all_sops() -> str:
    """Run the full audit across ALL SOPs using sub-agents. Each SOP gets its own auditor sub-agent with access to the regulation knowledge base and web search. Fans out with configurable parallelism (MAX_AUDIT_WORKERS)."""
    return _audit_all_sops_impl(audit_single_sop)


def _slug(text: str) -> str:
    """Lowercase, alphanumeric-and-dashes slug for Jira labels."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _render_ticket_description(
    *,
    sop_id: str,
    clause_id: str,
    clause_title: str,
    regulation: str,
    severity: str,
    gap_description: str,
    remediation: str,
    evidence_quote: str,
    reasoning: str,
) -> str:
    """Render a plain-text Jira description with section headers. ADF wrapping happens in the client."""
    parts: list[str] = []
    parts.append(f"SOP: {sop_id}")
    parts.append(f"Regulation: {regulation}")
    parts.append(f"Clause: {clause_id} — {clause_title}")
    parts.append(f"Severity: {severity}")
    if evidence_quote:
        parts.append(f"Evidence:\n  \"{evidence_quote.strip()}\"")
    parts.append(f"Gap:\n  {gap_description}")
    if remediation:
        parts.append(f"Recommended remediation:\n  {remediation}")
    if reasoning:
        parts.append(f"Reasoning:\n  {reasoning}")
    parts.append("Filed automatically by the Sentinel compliance agent.")
    return "\n\n".join(parts)


@tool
def create_jira_ticket(
    sop_id: str,
    clause_id: str,
    clause_title: str,
    regulation: str,
    severity: str,
    gap_description: str,
    remediation: str = "",
    evidence_quote: str = "",
    reasoning: str = "",
) -> str:
    """Create a Jira ticket for a confirmed compliance gap in the project configured via JIRA_PROJECT_KEY.

    Call this when an audit finding has compliance_level 'gap' or 'partial' AND severity is medium or higher,
    so a human assignee can act on it. One call creates one ticket. Returns the issue key and URL on success.

    Args:
        sop_id: SOP identifier (e.g. 'SOP-ISEC-002')
        clause_id: regulatory clause identifier (e.g. 'HIPAA-164.312(a)', 'CC6.1')
        clause_title: short title of the clause (e.g. 'Access Control')
        regulation: regulation name (e.g. 'HIPAA', 'SOC 2', 'GDPR')
        severity: one of 'critical', 'high', 'medium', 'low', 'info'
        gap_description: what is missing or insufficient in the SOP
        remediation: recommended remediation (optional)
        evidence_quote: exact quote from the SOP (optional)
        reasoning: 2-3 sentence rationale citing the regulation (optional)
    """
    from sentinel.actuation.jira_client import JiraClient, SEVERITY_TO_PRIORITY
    from sentinel.config import (
        JIRA_API_TOKEN,
        JIRA_BASE_URL,
        JIRA_DEFAULT_ISSUE_TYPE,
        JIRA_EMAIL,
        JIRA_PROJECT_KEY,
    )

    missing = [
        name for name, val in [
            ("JIRA_BASE_URL", JIRA_BASE_URL),
            ("JIRA_EMAIL", JIRA_EMAIL),
            ("JIRA_API_TOKEN", JIRA_API_TOKEN),
            ("JIRA_PROJECT_KEY", JIRA_PROJECT_KEY),
        ] if not val
    ]
    if missing:
        return f"Jira not configured — set {', '.join(missing)} in the environment"

    sev = (severity or "").strip().lower()
    if sev not in SEVERITY_TO_PRIORITY:
        sev = "medium"

    summary = f"[{sev.upper()}] {clause_id}: {clause_title} ({sop_id})"
    labels = sorted({
        "sentinel",
        "compliance-finding",
        f"sev-{sev}",
        _slug(regulation) or "regulation",
        _slug(sop_id) or "sop",
    })
    description = _render_ticket_description(
        sop_id=sop_id,
        clause_id=clause_id,
        clause_title=clause_title,
        regulation=regulation,
        severity=sev,
        gap_description=gap_description,
        remediation=remediation,
        evidence_quote=evidence_quote,
        reasoning=reasoning,
    )

    try:
        client = JiraClient(
            base_url=JIRA_BASE_URL,
            email=JIRA_EMAIL,
            api_token=JIRA_API_TOKEN,
            project_key=JIRA_PROJECT_KEY,
            issue_type=JIRA_DEFAULT_ISSUE_TYPE,
        )
        try:
            issue = client.create_issue(
                summary=summary,
                description=description,
                labels=labels,
                priority=SEVERITY_TO_PRIORITY[sev],
            )
        finally:
            client.close()
        return f"Filed Jira ticket {issue['key']} at {issue['url']}"
    except Exception as e:
        logger.exception("create_jira_ticket failed")
        return f"Jira ticket creation failed: {e}"


@tool
def create_jira_tickets(findings_json: str) -> str:
    """Create multiple Jira tickets at once for confirmed compliance gaps.

    Use this instead of calling create_jira_ticket repeatedly.
    Pass a JSON array string where each object has: sop_id, clause_id, clause_title, regulation, severity, gap_description.
    Optional fields: remediation, evidence_quote, reasoning.

    Example: '[{"sop_id":"SOP-ISEC-008","clause_id":"HIPAA-164.312(a)","clause_title":"Access Control","regulation":"HIPAA","severity":"high","gap_description":"Missing MFA requirement"}]'

    Returns a summary of created tickets and any failures.
    """
    try:
        findings = json.loads(findings_json)
    except (json.JSONDecodeError, TypeError):
        return "Invalid JSON. Pass a JSON array string of finding objects."
    if not isinstance(findings, list):
        return "Expected a JSON array of findings."

    from sentinel.actuation.jira_client import JiraClient, SEVERITY_TO_PRIORITY
    from sentinel.config import (
        JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_DEFAULT_ISSUE_TYPE,
        JIRA_EMAIL, JIRA_PROJECT_KEY,
    )

    missing = [
        name for name, val in [
            ("JIRA_BASE_URL", JIRA_BASE_URL), ("JIRA_EMAIL", JIRA_EMAIL),
            ("JIRA_API_TOKEN", JIRA_API_TOKEN), ("JIRA_PROJECT_KEY", JIRA_PROJECT_KEY),
        ] if not val
    ]
    if missing:
        return f"Jira not configured — set {', '.join(missing)} in the environment"
    if not findings:
        return "No findings provided."

    client = JiraClient(
        base_url=JIRA_BASE_URL, email=JIRA_EMAIL, api_token=JIRA_API_TOKEN,
        project_key=JIRA_PROJECT_KEY, issue_type=JIRA_DEFAULT_ISSUE_TYPE,
    )
    created = []
    failed = []
    try:
        for f in findings:
            sop_id = f.get("sop_id", "")
            clause_id = f.get("clause_id", f.get("requirement_id", ""))
            clause_title = f.get("clause_title", f.get("requirement_title", ""))
            regulation = f.get("regulation", "")
            sev = (f.get("severity", "medium") or "medium").strip().lower()
            if sev not in SEVERITY_TO_PRIORITY:
                sev = "medium"

            summary = f"[{sev.upper()}] {clause_id}: {clause_title} ({sop_id})"
            labels = sorted({
                "sentinel", "compliance-finding",
                f"sev-{sev}", _slug(regulation) or "regulation", _slug(sop_id) or "sop",
            })
            description = _render_ticket_description(
                sop_id=sop_id, clause_id=clause_id, clause_title=clause_title,
                regulation=regulation, severity=sev,
                gap_description=f.get("gap_description", ""),
                remediation=f.get("remediation", ""),
                evidence_quote=f.get("evidence_quote", ""),
                reasoning=f.get("reasoning", ""),
            )
            try:
                issue = client.create_issue(
                    summary=summary, description=description,
                    labels=labels, priority=SEVERITY_TO_PRIORITY[sev],
                )
                created.append(f"{issue['key']} — {clause_id} ({sop_id})")
            except Exception as e:
                failed.append(f"{clause_id} ({sop_id}): {e}")
    finally:
        client.close()

    lines = [f"Created {len(created)} Jira ticket(s), {len(failed)} failed."]
    for t in created:
        lines.append(f"  ✓ {t}")
    for f in failed:
        lines.append(f"  ✗ {f}")
    return "\n".join(lines)


def build_tools(provider: str = "nebius", use_tavily: bool = True, retrieval: str = "rag", model_name: str | None = None) -> list:
    """Build the complete tool list for the agent, parameterized by provider, Tavily, retrieval backend ("rag", "nexus", or "both"), and optional model_name override."""

    @tool
    def _audit_single_sop(sop_id: str) -> str:
        """Audit one SOP against all relevant regulations using a sub-agent with access to the regulation knowledge base. Accepts an SOP ID (e.g. 'SOP-AIML-009') or title (e.g. 'Algorithmic Bias Detection'). The sub-agent determines which regulations apply and iteratively retrieves regulatory text."""
        result = _audit_single_sop_impl(sop_id, provider=provider, use_tavily=use_tavily, retrieval=retrieval, model_name=model_name)
        for attempt in range(1, MAX_RETRIES + 1):
            if not _is_retryable(result):
                break
            delay = _retry_delay(attempt, result)
            logger.info("Retry attempt %d/%d for %s (waiting %.0fs)", attempt, MAX_RETRIES, sop_id, delay)
            time.sleep(delay)
            result = _audit_single_sop_impl(sop_id, provider=provider, use_tavily=use_tavily, retrieval=retrieval, model_name=model_name)
        return result

    @tool
    def _audit_sops(sop_ids: list[str]) -> str:
        """Audit a specific list of SOPs in parallel using sub-agents. Accepts a list of SOP IDs (e.g. ['SOP-AIML-009', 'SOP-ISEC-008']) or titles. Use this when the user asks to audit a subset of SOPs — by business unit, regulation, or explicit list. For ALL SOPs, use audit_all_sops instead."""
        import concurrent.futures
        from sentinel.config import MAX_AUDIT_WORKERS

        if not sop_ids:
            return "No SOP IDs provided."

        workers = min(len(sop_ids), MAX_AUDIT_WORKERS)
        results_by_id: dict[str, str] = {}

        def _audit_one(sid: str) -> str:
            try:
                return _audit_single_sop.invoke(sid)
            except Exception as e:
                return f"{sid}: FAILED — {e}"

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_audit_one, sid): sid for sid in sop_ids}
            for future in concurrent.futures.as_completed(futures):
                sid = futures[future]
                results_by_id[sid] = future.result()

        results = list(results_by_id.values())
        still_failed = sum(1 for r in results if _is_retryable(r))

        tok_in = _audit_results["total_input_tokens"]
        tok_out = _audit_results["total_output_tokens"]

        summary = (
            f"Audit complete: {len(sop_ids)} SOPs\n"
            f"  Failed: {still_failed}\n"
            f"  Total tokens: {tok_in + tok_out:,} ({tok_in:,} in / {tok_out:,} out)\n\n"
            "Per-SOP breakdown:\n" + "\n".join(sorted(results))
        )
        return summary

    @tool
    def _audit_all_sops() -> str:
        """Run the full audit across ALL 200 SOPs using sub-agents. Each SOP gets its own auditor sub-agent with access to the regulation knowledge base. Fans out with configurable parallelism (MAX_AUDIT_WORKERS)."""
        return _audit_all_sops_impl(_audit_single_sop)

    _audit_single_sop.name = "audit_single_sop"
    _audit_sops.name = "audit_sops"
    _audit_all_sops.name = "audit_all_sops"

    if retrieval in ("nexus", "both"):
        @tool
        def _list_regulations() -> str:
            """List all regulations available in the Nexus knowledge base. Returns regulation names and document coverage."""
            return (
                "Nexus knowledge base (50 source documents):\n"
                "\n"
                "Core 9 frameworks:\n"
                "- HIPAA: 45 CFR Parts 160, 162, 164 (current + 2017/2020/2024 editions)\n"
                "- SOC 2: 2017 Trust Services Criteria, 2018 Description Criteria\n"
                "- GDPR: Regulation (EU) 2016/679, full article-by-article text\n"
                "- EU AI Act: Regulation (EU) 2024/1689 + 2021 Commission proposal\n"
                "- NIST AI RMF: AI 100-1 (final + drafts), AI 600-1 GenAI Profile\n"
                "- SR 11-7 / SR 26-2: Model Risk Management (2011 original + 2026 revised)\n"
                "- California SB 53: Frontier AI Transparency\n"
                "- California SB 942: AI Transparency Act\n"
                "- California AB 853: AI Transparency Amendments\n"
                "\n"
                "NIST publications:\n"
                "- NIST CSF 2.0: Cybersecurity Framework\n"
                "- NIST Privacy Framework 1.0\n"
                "- NIST SP 1270: AI Bias\n"
                "- NIST SP 800-53 Rev 5: Security and Privacy Controls\n"
                "- NIST SP 800-88 Rev 1: Media Sanitization\n"
                "- NIST SP 800-61 Rev 2: Incident Handling\n"
                "- NIST SP 800-63B: Digital Identity / Authentication\n"
                "- NIST SP 800-207: Zero Trust Architecture\n"
                "- NIST SP 800-34 Rev 1: Contingency Planning\n"
                "- NIST SP 800-161 Rev 1: Supply Chain Risk Management\n"
                "- NIST SP 800-218: Secure Software Development (SSDF)\n"
                "\n"
                "FDA / 21 CFR:\n"
                "- FDA 21 CFR Part 11: Electronic Records & Signatures\n"
                "- FDA 21 CFR Part 807: Premarket Notification (510k)\n"
                "- FDA 21 CFR Part 820: Quality System Regulation\n"
                "- FDA AI/ML SaMD: Software as Medical Device Framework\n"
                "- FDA CDS Guidance: Clinical Decision Support\n"
                "\n"
                "EU directives & regulations:\n"
                "- EU MDR: Medical Device Regulation 2017/745\n"
                "- EU SCCs: Standard Contractual Clauses 2021/914\n"
                "- EU ePrivacy Directive 2002/58\n"
                "- EU AMLD4: Anti-Money Laundering Directive 2015/849\n"
                "- EU Funds Transfer Regulation 2015/847\n"
                "\n"
                "OWASP:\n"
                "- OWASP Top 10 (2021)\n"
                "- OWASP API Security Top 10 (2023)\n"
                "\n"
                "Financial:\n"
                "- BSA: Bank Secrecy Act (31 CFR Chapter X)\n"
                "- ECOA Regulation B: Equal Credit Opportunity\n"
                "- FCRA: Fair Credit Reporting Act\n"
                "- PCI DSS: Payment Card Industry Data Security Standard"
            )
        _list_regulations.name = "list_regulations"

        @tool
        def _retrieve_regulation_text(query: str, regulation: str = "") -> str:
            """Retrieve regulation text from the Nexus knowledge base for a given query. Optionally filter by regulation name (e.g. 'HIPAA', 'SOC 2', 'GDPR'). Returns a grounded answer with citations."""
            if not NEXUS_API_KEY:
                return "Nexus not configured — set NEXUS_API_KEY."
            try:
                from sentinel.retrieval.nexus import query_nexus, format_nexus_response
                ask = f"{regulation}: {query}" if regulation else query
                data = query_nexus(ask)
                if data.get("state") != "completed":
                    return f"Nexus query failed: {data.get('state', 'unknown')}"
                return f"Nexus result:\n{format_nexus_response(data)}"
            except Exception as e:
                return f"Nexus retrieval failed: {e}"
        _retrieve_regulation_text.name = "retrieve_regulation_text_tool"

        tools = [
            list_sops,
            _list_regulations,
            _retrieve_regulation_text,
            _audit_single_sop,
            _audit_sops,
            _audit_all_sops,
            create_jira_ticket,
            create_jira_tickets,
        ]
    else:
        tools = [
            list_sops,
            list_regulations,
            retrieve_regulation_text_tool,
            _audit_single_sop,
            _audit_sops,
            _audit_all_sops,
            create_jira_ticket,
            create_jira_tickets,
        ]
    if use_tavily:
        tools.insert(3, search_web)
    return tools
