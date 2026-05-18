#!/usr/bin/env python3
"""
Act 1 — ChatGPT sub-agent audit.

Same sub-agent architecture as Act 2, but uses GPT-5.5 (OpenAI)
instead of DeepSeek-V4-Pro (Nebius). No Tavily web search.

Usage:
    python -m demo.act1_prototype
    python -m demo.act1_prototype --provider nebius  # Use Nebius instead
"""
import argparse
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

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
    parser = argparse.ArgumentParser(description="Act 1: Agentic RAG Prototype")
    parser.add_argument("--provider", choices=["nebius", "openai"], default="openai")
    args = parser.parse_args()

    console = Console()

    model_label = "GPT-5.5 (OpenAI)" if args.provider == "openai" else "DeepSeek-V4-Pro (Nebius)"

    console.print()
    console.rule("[bold red]Act 1 — Agentic RAG Prototype[/bold red]")
    console.print()
    console.print(Panel(
        AUDIT_QUERY,
        title="Audit Query",
        border_style="blue",
    ))
    console.print()
    console.print(f"[bold]Model:[/bold] {model_label}")
    console.print()

    start = time.time()
    console.print("[dim]Decomposing query into regulation clauses...[/dim]")

    state = run_audit(
        AUDIT_QUERY,
        provider=args.provider,
        run_name=f"act1-{args.provider}",
        tags=["act1", "prototype", args.provider],
    )

    elapsed = time.time() - start
    findings = state["findings"]
    cell_metrics = state.get("cell_metrics", [])

    console.print(f"\n[bold]Audit complete in {elapsed:.1f}s[/bold]")

    render_summary(findings, console)
    render_heatmap(findings, console)

    output_dir = Path("output/act1")
    csv_path, json_path, metrics_path, metrics = save_register(
        findings, cell_metrics, output_dir, prefix="act1_rag"
    )

    console.print()
    console.rule("[bold]Act 1 Metrics[/bold]")
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
        "[bold red]Presenter line:[/bold red] \"This is the auditor every compliance team "
        "built last year. Same model we're about to run in Act 2. The model is fine. "
        "The retrieval is wrong — and on a compliance audit, wrong retrieval is wrong "
        "findings in front of HHS OCR.\""
    )


if __name__ == "__main__":
    main()
