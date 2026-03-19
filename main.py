import sys, os
sys.path.insert(0, os.path.dirname(__file__))


from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.prompt import Prompt

from config.shared_state import Shared_State as State
import agents.Orch
from graph import build
from utils.logger import log

from dotenv import load_dotenv
load_dotenv()
console = Console()


def main():
    app = build()
    console.rule("Story + Image Pipeline")
    console.print("Orchestrator → Story Agent → Image Agent\n")

    while True:
        try:
            user_input = Prompt.ask("enter your prompt").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        result = app.invoke(State(
            messages=[HumanMessage(content=user_input)],
            user_input=user_input,
            story=None,
            image_url=None,
            error=None,
        ))

        if result.get("error"):
            log.error(result["error"])
        else:
            log.result(result["story"], result["image_url"])


if __name__ == "__main__":
    main()