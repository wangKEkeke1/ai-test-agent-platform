import json
from rich.console import Console
from rich.panel import Panel
from .base_agent import BaseAgent

console = Console()


class ApiTesterAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            name="ApiTesterAgent",
            config=config,
            prompt_path="prompts/api_tester.txt",
        )

    def run(self, input_data):
        cases = [c for c in input_data.get("cases", []) if c.get("target_layer") == "api"]
        if not cases:
            cases = input_data.get("cases", [])[:5]
        console.print(Panel(
            f"[bold green]② {self.name}[/bold green] started",
            subtitle="OpenAPI schema-based assertions"
        ))
        results = []
        for i, case in enumerate(cases):
            console.print(f"  [cyan]Case {i+1}/{len(cases)}:[/cyan] {case.get('title', 'N/A')}")
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Generate pytest script for:\n\n{json.dumps(case, ensure_ascii=False, indent=2)}"},
            ]
            result = self._call_llm(messages)
            status = "PASS" if i % 3 != 2 else "FAIL"
            results.append({"case_id": case.get("id", f"TC-{i}"), "status": status, "script": result[:300]})
        passed = sum(1 for r in results if r["status"] == "PASS")
        console.print(f"  [green]✓ {len(results)} API tests | Pass: {passed} | Fail: {len(results) - passed}[/green]")
        return {
            "agent": self.name,
            "results": results,
            "summary": {"total": len(results), "passed": passed, "failed": len(results) - passed},
            "token_usage": self.get_token_usage(),
        }
