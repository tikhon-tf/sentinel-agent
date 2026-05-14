#!/usr/bin/env python3
"""
Act 3 — Snowglobe finds what you missed.

Two adversarial scenarios, first without guardrails (FAIL), then with guardrails (PASS).

Usage:
    python -m demo.act3_simulation
"""
import json
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentinel.simulation.snowglobe import (
    SCENARIO_A,
    SCENARIO_B,
    run_scenario_a,
    run_scenario_b,
    run_simulation,
)


def main():
    console = Console()

    console.print()
    console.rule("[bold magenta]Act 3 — Snowglobe Adversarial Simulation[/bold magenta]")
    console.print()

    # --- Scenario A: Without guardrails ---
    console.print(Panel(
        f"[bold]{SCENARIO_A['name']}[/bold]\n\n"
        f"Persona: {SCENARIO_A['persona']}\n\n"
        f"{SCENARIO_A['description']}",
        title="Scenario A",
        border_style="red",
    ))
    console.print()

    console.print("[dim]Running Scenario A without guardrails...[/dim]")
    result_a_no = run_scenario_a(finding=None, guardrails_enabled=False)
    _print_result(console, result_a_no)

    # --- Scenario B: Without guardrails ---
    console.print()
    console.print(Panel(
        f"[bold]{SCENARIO_B['name']}[/bold]\n\n"
        f"Persona: {SCENARIO_B['persona']}\n\n"
        f"{SCENARIO_B['description']}",
        title="Scenario B",
        border_style="red",
    ))
    console.print()

    console.print("[dim]Running Scenario B without guardrails...[/dim]")
    result_b_no = run_scenario_b(guardrails_enabled=False)
    _print_result(console, result_b_no)

    # --- Apply guardrails ---
    console.print()
    console.rule("[bold yellow]Applying Guardrails[/bold yellow]")
    console.print()
    console.print(
        "  1. Severity-downgrade now requires an explicit, logged exemption from a human reviewer\n"
        "  2. Citation-validation sub-graph re-reads the cited paragraph end-to-end before "
        "accepting a control as sufficient"
    )
    console.print()

    # --- Scenario A: With guardrails ---
    console.print("[dim]Re-running Scenario A with guardrails...[/dim]")
    result_a_yes = run_scenario_a(finding=None, guardrails_enabled=True)
    _print_result(console, result_a_yes)

    # --- Scenario B: With guardrails ---
    console.print("[dim]Re-running Scenario B with guardrails...[/dim]")
    result_b_yes = run_scenario_b(guardrails_enabled=True)
    _print_result(console, result_b_yes)

    # --- Summary table ---
    console.print()
    table = Table(title="Snowglobe Simulation Results", show_lines=True)
    table.add_column("Scenario", style="bold")
    table.add_column("Guardrails", justify="center")
    table.add_column("Result", justify="center")
    table.add_column("Tokens", justify="right")
    table.add_column("Latency", justify="right")

    for label, r in [
        ("A: Severity Downgrade", result_a_no),
        ("A: Severity Downgrade", result_a_yes),
        ("B: Deceptive Language", result_b_no),
        ("B: Deceptive Language", result_b_yes),
    ]:
        guardrails = "ON" if r["guardrails_enabled"] else "OFF"
        passed = r["passed"]
        result_text = "[bold green]PASS[/bold green]" if passed else "[bold red]FAIL[/bold red]"
        table.add_row(label, guardrails, result_text, str(r["tokens"]), f"{r['latency']:.1f}s")

    console.print(table)

    # Save results
    output_dir = Path("output/act3")
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "scenario_a_no_guardrails": result_a_no,
        "scenario_a_with_guardrails": result_a_yes,
        "scenario_b_no_guardrails": result_b_no,
        "scenario_b_with_guardrails": result_b_yes,
    }
    (output_dir / "simulation_results.json").write_text(
        json.dumps(results, indent=2, default=str), encoding="utf-8"
    )

    console.print()
    console.print(
        "[bold magenta]Presenter line:[/bold magenta] \"You do not find this in production. "
        "You find it here, before it costs you an OCR Resolution Agreement and a failed "
        "SOC 2 report.\""
    )
    console.print()


def _print_result(console: Console, result: dict):
    passed = result["passed"]
    status = "[bold green]PASS[/bold green]" if passed else "[bold red]FAIL[/bold red]"
    console.print(f"  Result: {status}  |  Tokens: {result['tokens']}  |  Latency: {result['latency']:.1f}s")

    response = result["agent_response"]
    if len(response) > 400:
        response = response[:400] + "..."
    console.print(f"  [dim]Agent: {response}[/dim]")
    console.print()


if __name__ == "__main__":
    main()
