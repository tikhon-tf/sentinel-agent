#!/usr/bin/env python3
"""
Act 4 — Closing the loop: from compliance review to Jira ticket.

A compliance reviewer asks Sentinel a real question — "does our SOP meet this
regulation?". Sentinel consults the regulation, reads the SOP, and produces a
structured finding. When the finding is a gap, a Jira ticket is filed on the
team's Kanban board so a human assignee can act on it.

The demo narrates every step so the audience can follow the end-to-end flow:
the audit context, the prompts sent to the model, the structured finding
produced, and the resulting ticket.

Usage:
    python -m demo.act4_actuation
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentinel.config import JIRA_BASE_URL, JIRA_PROJECT_KEY, MODEL
from sentinel.graph.tools import create_jira_ticket
from sentinel.llm import get_client

EXCERPT_CHARS = 800
TICKETABLE_LEVELS = {"gap", "partial"}
TICKETABLE_SEVERITIES = {"critical", "high", "medium"}


SYSTEM_PROMPT = """You are Sentinel, a regulatory compliance auditor for Meridian Health Technologies.

Given a regulation requirement and an SOP excerpt, assess whether the SOP satisfies the requirement and produce a JSON object with these exact fields:

  - compliance_level: "compliant" | "partial" | "gap"
  - severity:         "critical" | "high" | "medium" | "low" | "info"
  - evidence_quote:   the most relevant exact quote from the SOP (or empty string)
  - gap_description:  what is missing or insufficient, if anything (or empty string)
  - remediation:      specific recommended action to close the gap (or empty string)
  - reasoning:        2-3 sentences citing the specific regulatory clause

Rules:
- Be specific. Cite exact regulatory section numbers.
- Aspirational language ("aims to", "will implement", "under development") does NOT constitute an implemented control — mark as gap.
- Return JSON only, with no prose before or after, and no code fences."""


@dataclass(frozen=True)
class AuditCase:
    """A neutral, realistic compliance review that someone might ask Sentinel to run."""

    name: str
    requester: str
    summary: str
    sop_id: str
    clause_id: str
    clause_title: str
    regulation: str
    regulation_excerpt: str
    sop_excerpt: str


CASE_HIPAA_ACCESS = AuditCase(
    name="HIPAA Access Control Review",
    requester="Security Compliance team",
    summary=(
        "We're preparing for the HIPAA technical-safeguards section of our SOC 2 + HIPAA "
        "audit next month. Please review SOP-ISEC-002 (Access Control for ePHI Systems) "
        "against 45 CFR § 164.312(a) and let us know if there are any gaps we need to "
        "remediate before the audit."
    ),
    sop_id="SOP-ISEC-002",
    clause_id="45 CFR § 164.312(a)(2)(i)",
    clause_title="Unique user identification",
    regulation="HIPAA Security Rule",
    regulation_excerpt=(
        "45 CFR § 164.312(a)(1) Standard: Access control. Implement technical policies "
        "and procedures for electronic information systems that maintain electronic "
        "protected health information to allow access only to those persons or software "
        "programs that have been granted access rights as specified in § 164.308(a)(4).\n\n"
        "§ 164.312(a)(2)(i) Unique user identification (Required). Assign a unique name "
        "and/or number for identifying and tracking user identity.\n\n"
        "§ 164.312(a)(2)(ii) Emergency access procedure (Required). Establish (and "
        "implement as needed) procedures for obtaining necessary electronic protected "
        "health information during an emergency."
    ),
    sop_excerpt=(
        "SOP-ISEC-002 § 5 — Access Control for ePHI Systems\n\n"
        "5.1 Role-Based Access. Access to ePHI systems is granted based on role "
        "assignments managed in our identity provider. Access reviews occur quarterly "
        "and are documented in the access-review log.\n\n"
        "5.2 Account Provisioning. New employee accounts are provisioned via a shared "
        "service-desk ticket. Initial credentials are emailed to the requesting manager, "
        "who shares them with the new hire on their first day.\n\n"
        "5.3 Termination. Access revocation is handled by the IT team upon notification "
        "from HR. We aim to complete revocation within five business days of an "
        "employee's last day of work."
    ),
)


CASE_GDPR_BREACH = AuditCase(
    name="GDPR Breach Notification Readiness",
    requester="CISO office",
    summary=(
        "We just added an EU subprocessor and want to confirm our incident-response "
        "playbook satisfies GDPR Article 33's 72-hour supervisory-authority notification "
        "before we go live. Please review SOP-IRSP-001 and flag anything missing."
    ),
    sop_id="SOP-IRSP-001",
    clause_id="GDPR Art. 33(1)",
    clause_title="Notification of a personal data breach to the supervisory authority",
    regulation="GDPR (Regulation (EU) 2016/679)",
    regulation_excerpt=(
        "GDPR Article 33(1) — Notification of a personal data breach to the supervisory "
        "authority.\n\n"
        "In the case of a personal data breach, the controller shall without undue delay "
        "and, where feasible, not later than 72 hours after having become aware of it, "
        "notify the personal data breach to the supervisory authority competent in "
        "accordance with Article 55, unless the personal data breach is unlikely to "
        "result in a risk to the rights and freedoms of natural persons. Where the "
        "notification to the supervisory authority is not made within 72 hours, it shall "
        "be accompanied by reasons for the delay."
    ),
    sop_excerpt=(
        "SOP-IRSP-001 § 4 — Incident Notification\n\n"
        "4.1 Internal Escalation. Detected security incidents are reported to the on-call "
        "security engineer within one hour of detection and to the CISO within four "
        "hours.\n\n"
        "4.2 Regulatory Notification (Health Data). For incidents involving Protected "
        "Health Information (PHI), HIPAA breach-notification procedures apply. The "
        "Compliance Officer notifies HHS within 60 days, and affected individuals within "
        "60 days, in line with 45 CFR § 164.404 and § 164.408.\n\n"
        "4.3 External Communications. Communications to media, customers, and law "
        "enforcement are coordinated by the Communications team in consultation with "
        "Legal Counsel."
    ),
)


CASES: list[AuditCase] = [CASE_HIPAA_ACCESS, CASE_GDPR_BREACH]


# ============================================================================ main


def main() -> None:
    console = Console()

    console.print()
    console.rule("[bold blue]Act 4 — Closing the Loop: Audit → Jira Ticket[/bold blue]")
    console.print()
    console.print(Panel(
        "A compliance reviewer asks Sentinel a real question. Sentinel consults the "
        "regulation, reads the SOP, and produces a structured finding. When the "
        "finding is a gap, a Jira ticket is filed automatically so a human assignee "
        "can act on it.",
        title="Act 4",
        border_style="blue",
    ))

    results: list[dict] = []
    for case in CASES:
        record = _run_case(console, case)
        results.append(record)

    _render_summary(console, results)
    _save_results(results)


# ============================================================================ per-case flow


def _run_case(console: Console, case: AuditCase) -> dict:
    console.print()
    console.print(Rule(f"[bold cyan]{case.name}[/bold cyan]", style="cyan"))
    console.print()
    console.print(Panel(
        f"[bold]Requested by:[/bold] {case.requester}\n\n{case.summary}",
        title="Compliance question",
        border_style="cyan",
    ))

    # --- Step 1: gather audit context ---
    console.print()
    console.print("[bold]Step 1 — Gather audit context[/bold]")
    console.print(f"  SOP under review: [bold]{case.sop_id}[/bold]")
    console.print(f"  Regulation:       [bold]{case.regulation}[/bold]")
    console.print(f"  Clause focus:     [bold]{case.clause_id} — {case.clause_title}[/bold]")
    console.print(Panel(case.regulation_excerpt, title=f"Regulation excerpt — {case.clause_id}", border_style="dim"))
    console.print(Panel(case.sop_excerpt, title=f"SOP excerpt — {case.sop_id}", border_style="dim"))

    # --- Step 2: send to Sentinel auditor ---
    console.print()
    console.print("[bold]Step 2 — Sentinel auditor produces a structured finding[/bold]")
    user_prompt = _build_user_prompt(case)
    console.print(Panel(SYSTEM_PROMPT, title="System prompt", border_style="dim"))
    console.print(Panel(_truncate(user_prompt, EXCERPT_CHARS), title="User prompt", border_style="dim"))

    console.print("[dim]Calling the model…[/dim]")
    response = _call_model(user_prompt)
    console.print(
        f"  Model: [bold]{response['model']}[/bold]  |  "
        f"Tokens: {response['input_tokens']:,} in / {response['output_tokens']:,} out  |  "
        f"Latency: {response['latency']:.1f}s"
    )
    console.print(Panel(
        _truncate(response["content"], EXCERPT_CHARS),
        title="Model response (raw)",
        border_style="white",
    ))

    finding = _parse_finding(response["content"])
    if finding is None:
        console.print("[bold red]Could not parse a structured finding from the response — skipping ticket creation[/bold red]")
        return {
            "case": case.name,
            "model": response["model"],
            "tokens": response["tokens"],
            "latency": response["latency"],
            "finding": None,
            "ticket_result": None,
        }

    console.print(Panel(_render_finding(case, finding), title="Structured finding", border_style="yellow"))

    # --- Step 3: decide on action ---
    console.print()
    console.print("[bold]Step 3 — Decide on action[/bold]")
    level = finding["compliance_level"]
    severity = finding["severity"]
    if level not in TICKETABLE_LEVELS or severity not in TICKETABLE_SEVERITIES:
        console.print(
            f"  Compliance level [bold]{level}[/bold] at severity [bold]{severity}[/bold] — "
            "no ticket needed. Sentinel recommends no further action."
        )
        return {
            "case": case.name,
            "model": response["model"],
            "tokens": response["tokens"],
            "latency": response["latency"],
            "finding": finding,
            "ticket_result": None,
        }

    console.print(
        f"  Compliance level [bold]{level}[/bold] at severity [bold]{severity}[/bold] — "
        "filing a Jira ticket so a human assignee can remediate."
    )

    # --- Step 4: file ticket ---
    console.print()
    console.print("[bold]Step 4 — File Jira ticket[/bold]")
    console.print("[dim]Calling create_jira_ticket tool…[/dim]")
    ticket_payload = {
        "sop_id": case.sop_id,
        "clause_id": case.clause_id,
        "clause_title": case.clause_title,
        "regulation": case.regulation,
        "severity": severity,
        "gap_description": finding.get("gap_description", "") or "(no description provided)",
        "remediation": finding.get("remediation", ""),
        "evidence_quote": finding.get("evidence_quote", ""),
        "reasoning": finding.get("reasoning", ""),
    }
    ticket_result = create_jira_ticket.invoke(ticket_payload)
    border = "green" if ticket_result.startswith("Filed Jira ticket") else "red"
    console.print(Panel(
        _render_ticket_block(ticket_payload, ticket_result),
        title="Jira Ticket",
        border_style=border,
    ))

    return {
        "case": case.name,
        "model": response["model"],
        "tokens": response["tokens"],
        "latency": response["latency"],
        "finding": finding,
        "ticket_payload": ticket_payload,
        "ticket_result": ticket_result,
    }


# ============================================================================ helpers


def _build_user_prompt(case: AuditCase) -> str:
    return (
        f"Audit case: {case.name}\n"
        f"SOP under review: {case.sop_id}\n"
        f"Regulatory clause focus: {case.clause_id} — {case.clause_title}\n\n"
        f"Regulation requirement:\n{case.regulation_excerpt.strip()}\n\n"
        f"SOP excerpt:\n{case.sop_excerpt.strip()}\n\n"
        "Produce your structured assessment as a JSON object."
    )


def _call_model(user_prompt: str) -> dict:
    client = get_client()
    start = time.time()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1200,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    elapsed = time.time() - start
    usage = response.usage
    return {
        "model": MODEL,
        "content": response.choices[0].message.content or "",
        "latency": elapsed,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "tokens": usage.prompt_tokens + usage.completion_tokens,
    }


def _parse_finding(raw: str) -> dict | None:
    """Extract the JSON finding object from the model response. Tolerant to code fences."""
    text = raw.strip()
    if "```" in text:
        fence_start = text.find("```")
        lang_end = text.find("\n", fence_start)
        inner_start = lang_end + 1 if lang_end > fence_start else fence_start + 3
        fence_end = text.find("```", inner_start)
        if fence_end > inner_start:
            text = text[inner_start:fence_end].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    candidate = text[start:end + 1]
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    return {
        "compliance_level": str(parsed.get("compliance_level", "")).strip().lower(),
        "severity": str(parsed.get("severity", "")).strip().lower(),
        "evidence_quote": parsed.get("evidence_quote", "") or "",
        "gap_description": parsed.get("gap_description", "") or "",
        "remediation": parsed.get("remediation", "") or "",
        "reasoning": parsed.get("reasoning", "") or "",
    }


def _render_finding(case: AuditCase, finding: dict) -> str:
    lines = [
        f"[bold]Compliance level:[/bold] {finding['compliance_level']}",
        f"[bold]Severity:[/bold] {finding['severity']}",
    ]
    if finding.get("evidence_quote"):
        lines.append(f"[bold]Evidence quote:[/bold] \"{_truncate(finding['evidence_quote'], 250)}\"")
    if finding.get("gap_description"):
        lines.append(f"[bold]Gap:[/bold] {_truncate(finding['gap_description'], 350)}")
    if finding.get("remediation"):
        lines.append(f"[bold]Remediation:[/bold] {_truncate(finding['remediation'], 350)}")
    if finding.get("reasoning"):
        lines.append(f"[bold]Reasoning:[/bold] {_truncate(finding['reasoning'], 350)}")
    return "\n".join(lines)


def _render_ticket_block(payload: dict, ticket_result: str) -> str:
    return (
        f"[bold]Result:[/bold] {ticket_result}\n\n"
        f"[bold]Summary:[/bold] [{payload['severity'].upper()}] {payload['clause_id']}: "
        f"{payload['clause_title']} ({payload['sop_id']})\n"
        f"[bold]Labels:[/bold] sentinel, compliance-finding, sev-{payload['severity']}, "
        f"{_slug(payload['regulation'])}, {_slug(payload['sop_id'])}"
    )


def _render_summary(console: Console, results: list[dict]) -> None:
    console.print()
    console.rule("[bold blue]Summary[/bold blue]")
    table = Table(title="Act 4 — Reviews and Tickets", show_lines=True)
    table.add_column("Case", style="bold")
    table.add_column("Level", justify="center")
    table.add_column("Severity", justify="center")
    table.add_column("Tokens", justify="right")
    table.add_column("Latency", justify="right")
    table.add_column("Jira Ticket")

    for r in results:
        case = r["case"]
        finding = r["finding"]
        ticket = r["ticket_result"]
        level = finding["compliance_level"] if finding else "—"
        sev = finding["severity"] if finding else "—"
        if ticket is None and finding is not None:
            ticket_cell = "[dim](no ticket — finding does not meet threshold)[/dim]"
        elif ticket is None:
            ticket_cell = "[dim](no ticket — parse failed)[/dim]"
        else:
            ticket_cell = ticket
        table.add_row(
            case,
            level,
            sev,
            f"{r['tokens']:,}",
            f"{r['latency']:.1f}s",
            ticket_cell,
        )

    console.print(table)
    if JIRA_BASE_URL and JIRA_PROJECT_KEY:
        project_url = f"{JIRA_BASE_URL}/browse/{JIRA_PROJECT_KEY}"
        console.print()
        console.print(f"[bold]Jira project:[/bold] {project_url}")
    console.print()


def _save_results(results: list[dict]) -> None:
    output_dir = Path("output/act4")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "actuation_results.json").write_text(
        json.dumps(results, indent=2, default=str), encoding="utf-8"
    )


def _truncate(text: str, limit: int) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "…"


def _slug(text: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


if __name__ == "__main__":
    main()
