import time
from openai import OpenAI
from rich.console import Console

console = Console()


class BaseAgent:
    def __init__(self, name, config, prompt_path):
        self.name = name
        self.config = config
        self.client = OpenAI(
            base_url=config["llm"]["base_url"],
            api_key=config["llm"]["api_key"],
        )
        self.model = config["llm"]["model"]
        self.system_prompt = self._load_prompt(prompt_path)
        self.token_usage = {"input": 0, "output": 0}

    def _load_prompt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _call_llm(self, messages, temperature=None):
        start = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.config["llm"]["temperature"],
            max_tokens=self.config["llm"]["max_tokens"],
        )
        elapsed = time.time() - start
        content = response.choices[0].message.content
        usage = response.usage
        self.token_usage["input"] += usage.prompt_tokens
        self.token_usage["output"] += usage.completion_tokens
        console.print(
            f"  [dim]└─ LLM call completed in {elapsed:.1f}s | "
            f"tokens: {usage.prompt_tokens}in + {usage.completion_tokens}out[/dim]"
        )
        return content

    def run(self, input_data):
        raise NotImplementedError

    def get_token_usage(self):
        return self.token_usage.copy()
