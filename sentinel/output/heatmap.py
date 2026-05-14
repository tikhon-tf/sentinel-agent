"""Severity heat-map rendering for the audit register."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.text import Text

from sentinel.models import AuditFinding, ComplianceLevel, Severity


SEVERITY_COLORS = {
    Severity.CRITICAL: "bold white on red",
    Severity.HIGH: "bold white on dark_red",
    Severity.MEDIUM: "bold black on yellow",
    Severity.LOW: "bold black on cyan",
    Severity.INFO: "bold black on green",
}

COMPLIANCE_SYMBOLS = {
    ComplianceLevel.COMPLIANT: ("PASS", "green"),
    ComplianceLevel.PARTIAL: ("PARTIAL", "yellow"),
    ComplianceLevel.GAP: ("GAP", "red"),
}


def render_heatmap(findings: list[AuditFinding], console: Console | None = None):
    """Render a severity heat-map table to the console."""
    console = console or Console()

    clause_ids = sorted(set(f.clause_id for f in findings))
    sop_ids = sorted(set(f.sop_id for f in findings if f.sop_id != "NONE"))

    lookup: dict[tuple[str, str], AuditFinding] = {}
    for f in findings:
        lookup[(f.clause_id, f.sop_id)] = f

    table = Table(
        title="Sentinel Audit Heat-Map",
        show_header=True,
        header_style="bold",
        show_lines=True,
        expand=False,
    )

    table.add_column("Clause", style="bold", width=16)
    for sop_id in sop_ids[:15]:
        table.add_column(sop_id, width=12, justify="center")

    for clause_id in clause_ids:
        row = [clause_id]
        for sop_id in sop_ids[:15]:
            finding = lookup.get((clause_id, sop_id))
            if finding:
                symbol, color = COMPLIANCE_SYMBOLS[finding.compliance_level]
                severity_style = SEVERITY_COLORS.get(finding.severity, "")
                cell = Text(symbol, style=severity_style if finding.compliance_level != ComplianceLevel.COMPLIANT else f"bold {color}")
                row.append(cell)
            else:
                row.append(Text("—", style="dim"))
        table.add_row(*row)

    console.print(table)


def render_summary(findings: list[AuditFinding], console: Console | None = None):
    """Render an executive summary of the audit."""
    console = console or Console()

    total = len(findings)
    compliant = sum(1 for f in findings if f.compliance_level == ComplianceLevel.COMPLIANT)
    partial = sum(1 for f in findings if f.compliance_level == ComplianceLevel.PARTIAL)
    gaps = sum(1 for f in findings if f.compliance_level == ComplianceLevel.GAP)

    critical = sum(1 for f in findings if f.severity == Severity.CRITICAL)
    high = sum(1 for f in findings if f.severity == Severity.HIGH)
    medium = sum(1 for f in findings if f.severity == Severity.MEDIUM)
    low = sum(1 for f in findings if f.severity == Severity.LOW)

    console.print()
    console.rule("[bold]Sentinel Audit Summary[/bold]")
    console.print()

    summary_table = Table(show_header=False, box=None, padding=(0, 2))
    summary_table.add_column("Label", style="bold")
    summary_table.add_column("Value")
    summary_table.add_row("Total Findings", str(total))
    summary_table.add_row("Compliant", f"[green]{compliant}[/green] ({100*compliant/total:.0f}%)" if total else "0")
    summary_table.add_row("Partial", f"[yellow]{partial}[/yellow] ({100*partial/total:.0f}%)" if total else "0")
    summary_table.add_row("Gap", f"[red]{gaps}[/red] ({100*gaps/total:.0f}%)" if total else "0")
    console.print(summary_table)

    console.print()
    sev_table = Table(show_header=False, box=None, padding=(0, 2))
    sev_table.add_column("Severity", style="bold")
    sev_table.add_column("Count")
    sev_table.add_row("Critical", f"[bold red]{critical}[/bold red]")
    sev_table.add_row("High", f"[red]{high}[/red]")
    sev_table.add_row("Medium", f"[yellow]{medium}[/yellow]")
    sev_table.add_row("Low", f"[cyan]{low}[/cyan]")
    console.print(sev_table)

    if gaps > 0 or critical > 0:
        console.print()
        console.print("[bold red]TOP GAPS REQUIRING IMMEDIATE REMEDIATION:[/bold red]")
        console.print()
        critical_findings = [f for f in findings if f.severity in (Severity.CRITICAL, Severity.HIGH) and f.compliance_level == ComplianceLevel.GAP]
        for i, f in enumerate(critical_findings[:10], 1):
            console.print(f"  {i}. [bold]{f.clause_id}[/bold] × {f.sop_id}: {f.gap_description[:120]}")
            if f.remediation:
                console.print(f"     → {f.remediation[:120]}")

    console.print()
