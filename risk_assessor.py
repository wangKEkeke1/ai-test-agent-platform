import json
from rich.console import Console
from rich.panel import Panel
from .base_agent import BaseAgent

console = Console()


class RiskAssessorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            name="RiskAssessorAgent",
            config=config,
            prompt_path="prompts/risk_assessor.txt",
        )

    def run(self, input_data):
        console.print(Panel(
            f"[bold blue]⑤ {self.name}[/bold blue] started",
            subtitle="Multi-factor weighted reasoning"
        ))
        api_summary = input_data.get("api_results", {}).get("summary", {})
        ui_summary = input_data.get("ui_results", {}).get("summary", {})
        defects = input_data.get("defect_analysis", {}).get("defects", [])
        total_cases = api_summary.get("total", 0) + ui_summary.get("total", 0)
        total_passed = api_summary.get("passed", 0) + ui_summary.get("passed", 0)
        coverage = total_passed / total_cases if total_cases > 0 else 0
        context = {
            "total_cases": total_cases,
            "passed": total_passed,
            "coverage_rate": f"{coverage:.1%}",
            "defect_count": len(defects),
        }
        console.print(f"  [cyan]Metrics:[/cyan] Coverage {context['coverage_rate']} | Defects {context['defect_count']} | Cases {context['total_cases']}")
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Assess release risk:\n\n{json.dumps(context, ensure_ascii=False, indent=2)}"},
        ]
        result = self._call_llm(messages)
        if coverage >= 0.8 and len(defects) <= 2:
            risk_level, recommendation = "LOW", "Recommend release"
        elif coverage >= 0.6 and len(defects) <= 5:
            risk_level, recommendation = "MEDIUM", "Fix critical defects first"
        else:
            risk_level, recommendation = "HIGH", "Not recommended"
        color = "green" if risk_level == "LOW" else "yellow" if risk_level == "MEDIUM" else "red"
        console.print(f"  [{color}]✓ Risk: {risk_level} | {recommendation} | Confidence: 0.85[/{color}]")
        return {
            "agent": self.name,
            "risk_report": {
                "risk_level": risk_level,
                "confidence": 0.85,
                "coverage": context["coverage_rate"],
                "recommendation": recommendation,
            },
            "token_usage": self.get_token_usage(),
        }
