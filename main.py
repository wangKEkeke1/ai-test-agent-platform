import yaml
from orchestrator.workflow import TestWorkflow
from rich.console import Console

console = Console()


def main():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    with open("examples/sample_requirement.md", "r", encoding="utf-8") as f:
        requirement = f.read()

    workflow = TestWorkflow(config)
    results = workflow.run(requirement)
    console.print("[bold green]All tests completed[/bold green]")


if __name__ == "__main__":
    main()
