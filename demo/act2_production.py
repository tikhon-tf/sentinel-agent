#!/usr/bin/env python3
"""
Act 2 — Pinecone Nexus completes in one shot.

Same model. Same corpus. Structured one-shot retrieval via Pinecone Nexus.
One KnowQL query returns typed, cited findings.

Usage:
    python -m demo.act2_production
    python -m demo.act2_production --mode nexus  # Pinecone Nexus
    python -m demo.act2_production --mode local   # Local structured retrieval (default)
"""
import argparse
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentinel.graph.agent import run_audit
from sentinel.output.register import compute_metrics, save_register
from sentinel.output.heatmap import render_heatmap, render_summary

AUDIT_QUERY = (
    "Audit Meridian Health Technologies' internal Information Security and PHI Handling "
    "SOPs against SOC 2 Trust Services Criteria (CC1 through CC9) and the HIPAA Security "
    "Rule (45 CFR § 164.308 administrative safeguards, § 164.310 physical safeguards, "
    "§ 164.312 technical safeguards). For each finding, report: the compliance level "
    "(compliant, partial, or gap), the exact criterion or safeguard violated, a quoted "
    "piece of evidence from the SOP, a recommended remediation, and a severity rating."
)


def main():
    parser = argparse.ArgumentParser(description="Act 2: Production Stack with Nexus")
    parser.add_argument("--mode", choices=["nexus", "local"], default="local")
    args = parser.parse_args()

    console = Console()

    console.print()
    console.rule("[bold green]Act 2 — Production Stack with Pinecone Nexus[/bold green]")
    console.print()
    console.print(Panel(
        AUDIT_QUERY,
        title="Audit Query",
        border_style="green",
    ))
    console.print()
    console.print(f"[bold]Retrieval mode:[/bold] {args.mode} (structured one-shot)")
    console.print(f"[bold]Model:[/bold] DeepSeek-V4-Pro on Nebius")
    console.print(f"[bold]Grounding:[/bold] Tavily live regulation search")
    console.print()

    start = time.time()
    console.print("[dim]Decomposing query → Grounding regulations via Tavily → One-shot Nexus retrieval...[/dim]")

    state = run_audit(AUDIT_QUERY, mode=args.mode)

    elapsed = time.time() - start
    findings = state["findings"]
    cell_metrics = state.get("cell_metrics", [])

    console.print(f"\n[bold]Audit complete in {elapsed:.1f}s[/bold]")

    render_summary(findings, console)
    render_heatmap(findings, console)

    output_dir = Path("output/act2")
    csv_path, json_path, metrics_path, metrics = save_register(
        findings, cell_metrics, output_dir, prefix="act2_nexus"
    )

    console.print()
    console.rule("[bold]Act 2 Metrics[/bold]")
    console.print(f"  Total findings:       {metrics.total_findings}")
    console.print(f"  Total tokens:         {metrics.total_tokens:,}")
    console.print(f"  Total latency:        {metrics.total_latency:.1f}s")
    console.print(f"  Avg latency/cell:     {metrics.avg_latency_per_cell:.1f}s")
    console.print(f"  Retrieval steps:      {metrics.total_retrieval_steps}")
    console.print(f"  Estimated cost:       ${metrics.total_cost:.4f}")
    console.print()
    console.print(f"  Register: {csv_path}")
    console.print(f"  Findings: {json_path}")
    console.print(f"  Metrics:  {metrics_path}")

    console.print()
    console.print(
        "[bold green]Presenter line:[/bold green] \"Same model. Same corpus. The agent "
        "declares what it needs and Nexus returns it — typed, governed, cited — in one "
        "shot. Seven steps becomes one. Fifty-thousand tokens becomes seven. And the "
        "accuracy gap is the difference between a clean SOC 2 report and a re-audit.\""
    )


if __name__ == "__main__":
    main()
