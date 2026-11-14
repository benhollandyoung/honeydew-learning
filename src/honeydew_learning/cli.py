from importlib.metadata import version

import typer
from rich.console import Console

from honeydew_learning.diagnostics import (
        DiagnosticStatus,
        run_diagnostics,
)

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

@app.command()
def doctor() -> None:
    """Check Honeydew's development environment."""
    results = run_diagnostics()

    status_colors = {

            DiagnosticStatus.PASS: "green",
            DiagnosticStatus.WARN: "yellow",
            DiagnosticStatus.FAIL: "red",
        } 

    fine = True
    for diag in results:
        colour = status_colors[diag.status]
        console.print(f"[{colour}] {diag.status.value} [/{colour}] "
        f"{diag.name} {diag.detail}")
        if diag.status == DiagnosticStatus.FAIL:
            fine = False

    if not fine:
        raise typer.Exit(code=1)





if __name__ == "__main__":
    app()
