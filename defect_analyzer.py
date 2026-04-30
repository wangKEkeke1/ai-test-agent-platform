import json
from rich.console import Console
from rich.panel import Panel
from .base_agent import BaseAgent

console = Console()


class DefectAnalyzerAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            name="DefectAnalyzerAgent",
            config=config,
            prompt_path="prompts/defect_analyzer.txt",
        )
        self.max_rounds = config["agents"]["defect_analyzer"]["max_rounds"]

    def run(self, input_data):
        failed_cases = []
        for source in ["api_results", "ui_results"]:
            data = input_data.get(source, {})
            for r in data.get("results", []):
                if r.get("status") == "FAIL":
                    failed_cases.append(r)
        if not failed_cases:
            console.print(Panel(
                f"[bold yellow]④ {self.name}[/bold yellow] No failures, skipped",
                subtitle="ReAct reasoning"
            ))
            return {"agent": self.name, "defects": [], "token_usage": self.get_token_usage()}
        console.print(Panel(
            f"[bold red]④ {self.name}[/bold red] started",
            subtitle="ReAct reasoning loop"
        ))
        defects = []
        for i, case in enumerate(failed_cases):
            console.print(f"  [red]Analyzing {i+1}/{len(failed_cases)}:[/red] {case.get('case_id', 'N/A')}")
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyze root cause for:\n\n{json.dumps(case, ensure_ascii=False, indent=2)}"},
            ]
            for step in range(self.max_rounds):
                result = self._call_llm(messages)
                messages.append({"role": "assistant", "content": result})
                if "Final Answer" in result or step == self.max_rounds - 1:
                    break
                messages.append({"role": "user", "content": "Continue analysis, provide final root cause."})
            if "code" in result.lower():
                root_cause = "code defect"
            elif "env" in result.lower():
                root_cause = "env issue"
            else:
                root_cause = "case defect"
            defects.append({"case_id": case.get("case_id"), "root_cause": root_cause, "fix": result[:300]})
        console.print(f"  [green]✓ Found {len(defects)} defects[/green]")
        return {"agent": self.name, "defects": defects, "token_usage": self.get_token_usage()}
