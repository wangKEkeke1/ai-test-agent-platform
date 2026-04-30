import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from agents.case_generator import CaseGeneratorAgent
from agents.api_tester import ApiTesterAgent
from agents.ui_tester import UiTesterAgent
from agents.defect_analyzer import DefectAnalyzerAgent
from agents.risk_assessor import RiskAssessorAgent

console = Console()


class TestWorkflow:
    def __init__(self, config):
        self.config = config
        self.case_gen = CaseGeneratorAgent(config)
        self.api_tester = ApiTesterAgent(config)
        self.ui_tester = UiTesterAgent(config)
        self.defect_analyzer = DefectAnalyzerAgent(config)
        self.risk_assessor = RiskAssessorAgent(config)

    def run(self, requirement):
        console.print()
        console.print(Panel(
            "[bold white]AI Test Agent Platform[/bold white]\n"
            "[dim]5-Agent Long-chain Reasoning Architecture[/dim]",
            title="[bold]AI-Test-Agent-Platform[/bold]",
            border_style="bright_cyan",
        ))
        console.print()
        start_time = time.time()
        context = {"requirement": requirement}
        all_results = {}

        console.rule("[bold cyan]Phase 1 - Case Generation[/bold cyan]")
        case_result = self.case_gen.run(context)
        all_results["case_generation"] = case_result
        context["cases"] = case_result["cases"]
        console.print()

        console.rule("[bold green]Phase 2 - API & UI Automation[/bold green]")
        api_result = self.api_tester.run(context)
        all_results["api_results"] = api_result
        console.print()
        ui_result = self.ui_tester.run(context)
        all_results["ui_results"] = ui_result
        console.print()

        console.rule("[bold red]Phase 3 - Defect Root Cause Analysis[/bold red]")
        defect_result = self.defect_analyzer.run({"api_results": api_result, "ui_results": ui_result})
        all_results["defect_analysis"] = defect_result
        console.print()

        console.rule("[bold blue]Phase 4 - Risk Assessment[/bold blue]")
        risk_result = self.risk_assessor.run({"api_results": api_result, "ui_results": ui_result, "defect_analysis": defect_result})
        all_results["risk_assessment"] = risk_result
        console.print()

        elapsed = time.time() - start_time
        self._print_summary(all_results, elapsed)
        return all_results

    def _print_summary(self, results, elapsed):
        console.rule("[bold white]Summary[/bold white]")
        table = Table(title="Agent Summary", show_header=True, header_style="bold")
        table.add_column("Agent", style="cyan", width=25)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Output", width=35)
        table.add_column("Tokens", justify="right", width=12)
        total_in, total_out = 0, 0
        agents_data = [
            ("① Case Generation", "✓", f"{len(results['case_generation']['cases'])} cases", results["case_generation"]["token_usage"]),
            ("② API Automation", "✓", f"{results['api_results']['summary']['passed']}/{results['api_results']['summary']['total']} passed", results["api_results"]["token_usage"]),
            ("③ UI Automation", "✓", f"{results['ui_results']['summary']['passed']}/{results['ui_results']['summary']['total']} passed", results["ui_results"]["token_usage"]),
            ("④ Defect Analyzer", "✓", f"{len(results['defect_analysis'].get('defects', []))} defects", results["defect_analysis"]["token_usage"]),
            ("⑤ Risk Assessor", "✓", f"Risk: {results['risk_assessment']['risk_report']['risk_level']}", results["risk_assessment"]["token_usage"]),
        ]
        for name, status, output, usage in agents_data:
            table.add_row(name, status, output, f"{usage['input'] + usage['output']:,}")
            total_in += usage["input"]
            total_out += usage["output"]
        console.print(table)
        console.print()
        console.print(f"  [bold]Elapsed:[/bold] {elapsed:.1f}s")
        console.print(f"  [bold]Total Tokens:[/bold] {total_in + total_out:,} (In: {total_in:,} + Out: {total_out:,})")
        console.print()
