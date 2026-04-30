import json
from rich.console import Console
from rich.panel import Panel
from .base_agent import BaseAgent

console = Console()


class CaseGeneratorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            name="CaseGeneratorAgent",
            config=config,
            prompt_path="prompts/case_generator.txt",
        )
        self.rounds = config["agents"]["case_generator"]["rounds"]

    def run(self, input_data):
        requirement = input_data["requirement"]
        console.print(Panel(
            f"[bold cyan]① {self.name}[/bold cyan] started",
            subtitle="Long-chain reasoning core"
        ))
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Generate test cases for:\n\n{requirement}"},
        ]
        reasoning_trace = []
        for round_num in range(1, self.rounds + 1):
            console.print(f"  [yellow]Reasoning round {round_num}/{self.rounds}[/yellow]")
            result = self._call_llm(messages)
            reasoning_trace.append({"round": round_num, "output": result[:200]})
            messages.append({"role": "assistant", "content": result})
            if round_num < self.rounds:
                messages.append({
                    "role": "user",
                    "content": "Continue deeper analysis, add missing edge cases, output final structured JSON.",
                })
        try:
            parsed = json.loads(result)
            cases = parsed.get("cases", [])
        except json.JSONDecodeError:
            cases = [{"id": "TC-RAW", "title": "Raw output", "raw": result}]
        console.print(f"  [green]✓ Generated {len(cases)} test cases[/green]")
        return {
            "agent": self.name,
            "cases": cases,
            "reasoning_trace": reasoning_trace,
            "token_usage": self.get_token_usage(),
        }
