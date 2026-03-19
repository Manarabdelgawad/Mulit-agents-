from rich.console import Console
from rich.text import Text

_c = Console()

_STYLES = {
    "orch":  ("bold cyan",    "cyan"),
    "story": ("bold green",   "green"),
    "image": ("bold magenta", "magenta"),
}

_LABELS = {
    "orch":  "Orchestrator",
    "story": "Story Agent",
    "image": "Image Agent",
}


class _Logger:
    def _print(self, key: str, message: str):
        label_s, msg_s = _STYLES[key]
        _c.print(Text(f"[{_LABELS[key]}] ", style=label_s) + Text(message, style=msg_s))

    def orch(self, msg: str):  self._print("orch",  msg)
    def agent(self, key: str, msg: str): self._print(key, msg)
    def error(self, msg: str): _c.print(Text("[ERROR] ", style="bold red") + Text(msg, style="red"))

    def result(self, story: str, image_url: str):
        _c.rule("[bold white]Result[/bold white]")
        _c.print("\n[bold green]Story[/bold green]\n" + story)
        _c.print("\n[bold magenta]Image URL[/bold magenta]\n" + (image_url or "N/A"))
        _c.rule(style="dim")


log = _Logger()