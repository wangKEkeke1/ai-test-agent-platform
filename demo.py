"""
Demo mode: Simulates full 5-Agent workflow without API keys.
Run: python demo.py
"""

import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def sim(delay=0.3):
    time.sleep(delay)
    return {"input": random.randint(8000, 25000), "output": random.randint(500, 3000)}


def run_demo():
    console.print()
    console.print(Panel(
        "[bold white]AI Test Agent Platform[/bold white]\n"
        "[dim]5-Agent Long-chain Reasoning | Full Pipeline Demo[/dim]",
        title="[bold]AI-Test-Agent-Platform[/bold]",
        border_style="bright_cyan",
    ))
    console.print()
    total_start = time.time()
    all_usage = []

    console.rule("[bold cyan]Phase 1 - Case Generation Agent[/bold cyan]")
    console.print(Panel("[bold cyan]① Case Generation Agent[/bold cyan] started", subtitle="4-round CoT reasoning"))
    cases = [
        {"id": "TC-001", "title": "Modify quantity to 5 and checkout", "priority": "P0", "target_layer": "api"},
        {"id": "TC-002", "title": "Set quantity to 0 auto-remove", "priority": "P0", "target_layer": "api"},
        {"id": "TC-003", "title": "Exceed stock - button disabled", "priority": "P0", "target_layer": "ui"},
        {"id": "TC-004", "title": "Invalid input (-1, abc)", "priority": "P1", "target_layer": "api"},
        {"id": "TC-005", "title": "Amount precision 2 decimals", "priority": "P1", "target_layer": "api"},
        {"id": "TC-006", "title": "Batch select partial items", "priority": "P0", "target_layer": "api"},
        {"id": "TC-007", "title": "No selection - checkout disabled", "priority": "P1", "target_layer": "ui"},
        {"id": "TC-008", "title": "Redirect to payment page", "priority": "P0", "target_layer": "ui"},
        {"id": "TC-009", "title": "Concurrent quantity modification", "priority": "P2", "target_layer": "api"},
        {"id": "TC-010", "title": "API response < 500ms", "priority": "P1", "target_layer": "api"},
    ]
    for i in range(1, 5):
        console.print(f"  [yellow]Reasoning round {i}/4[/yellow]")
        u = sim()
        console.print(f"  [dim]└─ LLM call: {random.uniform(1.5, 3.0):.1f}s | {u['input']}in + {u['output']}out[/dim]")
        all_usage.append(u)
    console.print(f"  [green]✓ Generated {len(cases)} test cases[/green]")
    console.print()

    console.rule("[bold green]Phase 2 - API & UI Automation[/bold green]")
    console.print(Panel("[bold green]② API Automation Agent[/bold green] started", subtitle="OpenAPI assertions"))
    api_cases = [c for c in cases if c["target_layer"] == "api"]
    api_results = []
    for i, c in enumerate(api_cases):
        console.print(f"  [cyan]Case {i+1}/{len(api_cases)}:[/cyan] {c['title']}")
        u = sim(0.2)
        console.print(f"  [dim]└─ LLM call: {random.uniform(0.8, 2.0):.1f}s | {u['input']}in + {u['output']}out[/dim]")
        all_usage.append(u)
        status = "PASS" if random.random() > 0.2 else "FAIL"
        api_results.append({"case_id": c["id"], "status": status})
    api_p = sum(1 for r in api_results if r["status"] == "PASS")
    console.print(f"  [green]✓ {len(api_results)} API tests | Pass: {api_p} | Fail: {len(api_results) - api_p}[/green]")
    console.print()

    console.print(Panel("[bold magenta]③ UI Automation Agent[/bold magenta] started", subtitle="Playwright E2E"))
    ui_cases = [c for c in cases if c["target_layer"] == "ui"]
    ui_results = []
    for i, c in enumerate(ui_cases):
        console.print(f"  [cyan]Case {i+1}/{len(ui_cases)}:[/cyan] {c['title']}")
        u = sim(0.3)
        console.print(f"  [dim]└─ LLM call: {random.uniform(1.0, 2.5):.1f}s | {u['input']}in + {u['output']}out[/dim]")
        all_usage.append(u)
        status = "PASS" if random.random() > 0.25 else "FAIL"
        ui_results.append({"case_id": c["id"], "status": status})
    ui_p = sum(1 for r in ui_results if r["status"] == "PASS")
    console.print(f"  [green]✓ {len(ui_results)} UI tests | Pass: {ui_p} | Fail: {len(ui_results) - ui_p}[/green]")
    console.print()

    console.rule("[bold red]Phase 3 - Defect Root Cause Analysis[/bold red]")
    failed = [r for r in api_results + ui_results if r["status"] == "FAIL"]
    defects = []
    if failed:
        console.print(Panel("[bold red]④ Defect Analyzer Agent[/bold red] started", subtitle="ReAct reasoning"))
        for i, f in enumerate(failed):
            console.print(f"  [red]Analyzing {i+1}/{len(failed)}:[/red] {f['case_id']}")
            for step, label in enumerate(["Exclude env issues", "Exclude case defects", "Locate root cause"], 1):
                console.print(f"    [dim]Thought: Step {step} - {label}...[/dim]")
                u = sim(0.2)
                console.print(f"    [dim]└─ LLM call: {random.uniform(0.5, 1.5):.1f}s | {u['input']}in + {u['output']}out[/dim]")
                all_usage.append(u)
            rc = random.choice(["code defect", "env issue", "case defect"])
            console.print(f"    [bold]Final Answer: {rc}[/bold]")
            defects.append({"case_id": f["case_id"], "root_cause": rc})
        console.print(f"  [green]✓ Found {len(defects)} defects[/green]")
    else:
        console.print("  [yellow]④ No failures detected, skipped[/yellow]")
    console.print()

    console.rule("[bold blue]Phase 4 - Risk Assessment[/bold blue]")
    console.print(Panel("[bold blue]⑤ Risk Assessor Agent[/bold blue] started", subtitle="Multi-factor reasoning"))
    total = len(api_results) + len(ui_results)
    passed = api_p + ui_p
    cov = passed / total if total > 0 else 0
    console.print(f"  [cyan]Metrics:[/cyan] Coverage {cov:.0%} | Defects {len(defects)} | Cases {total}")
    u = sim(0.5)
    console.print(f"  [dim]└─ LLM call: {random.uniform(1.5, 3.0):.1f}s | {u['input']}in + {u['output']}out[/dim]")
    all_usage.append(u)
    if cov >= 0.7 and len(defects) <= 3:
        rl, rec, color = "LOW", "Recommend release", "green"
    elif cov >= 0.5:
        rl, rec, color = "MEDIUM", "Fix critical defects first", "yellow"
    else:
        rl, rec, color = "HIGH", "Not recommended", "red"
    console.print(f"  [{color}]✓ Risk: {rl} | {rec} | Confidence: 0.87[/{color}]")
    console.print()

    elapsed = time.time() - total_start
    tt = sum(u["input"] + u["output"] for u in all_usage)
    ti = sum(u["input"] for u in all_usage)
    to = sum(u["output"] for u in all_usage)

    console.rule("[bold white]Execution Summary[/bold white]")
    table = Table(title="Agent Summary", show_header=True, header_style="bold")
    table.add_column("Agent", style="cyan", width=30)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Key Output", width=35)
    table.add_column("Tokens", justify="right", width=12)
    table.add_row("① Case Generation", "✓", f"{len(cases)} cases (4-round CoT)", f"{random.randint(60000, 90000):,}")
    table.add_row("② API Automation", "✓", f"Pass {api_p}/{len(api_results)}", f"{random.randint(40000, 70000):,}")
    table.add_row("③ UI Automation", "✓", f"Pass {ui_p}/{len(ui_results)}", f"{random.randint(15000, 30000):,}")
    table.add_row("④ Defect Analyzer", "✓", f"{len(defects)} defects (ReAct)", f"{random.randint(30000, 50000):,}")
    table.add_row("⑤ Risk Assessor", "✓", f"Risk: {rl}", f"{random.randint(10000, 20000):,}")
    console.print(table)
    console.print()
    console.print(f"  [bold]Elapsed:[/bold]       {elapsed:.1f}s")
    console.print(f"  [bold]Total Tokens:[/bold] {tt:,} (In: {ti:,} + Out: {to:,})")
    console.print(f"  [bold]LLM Calls:[/bold]    {len(all_usage)}")
    console.print(f"  [bold]Coverage:[/bold]      {cov:.0%}")
    console.print(f"  [bold]Risk:[/bold]          {rl} - {rec}")
    console.print()
    console.print("[bold green]✓ Full pipeline completed[/bold green]")
    console.print()


if __name__ == "__main__":
    run_demo()
