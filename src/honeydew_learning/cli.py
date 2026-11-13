from importlib.metadata import version

import typer
from rich.console import Console

app = typer.Typer(
    name="honeydew",
    help="A local-first learning agent for macOS.",
)

console = Console()


@app.command()
def status() -> None:
    """Display the current agent status."""
    console.print("[bold]Honeydew[/bold]")
    console.print("Agent: not running")


@app.command("version")
def show_version() -> None:
    """Display the installed version."""
    console.print(version("honeydew-learning"))


if __name__ == "__main__":
    app()
