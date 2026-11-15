from importlib.metadata import version
from pathlib import Path
from subprocess import CalledProcessError, TimeoutExpired

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from honeydew_learning.diagnostics import (
    DiagnosticStatus,
    run_diagnostics,
)
from honeydew_learning.window_scout import discover_windows

app = typer.Typer(
    name="honeydew",
    help="A local-first learning agent for macOS.",
)

console = Console()
error_console = Console(stderr=True)


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
        console.print(
            f"[{colour}] {diag.status.value} [/{colour}] {diag.name} {diag.detail}"
        )
        if diag.status == DiagnosticStatus.FAIL:
            fine = False

    if not fine:
        error_console.print("[red] Failed development environment tests. [/]")
        raise typer.Exit(code=1)


@app.command()
def windows(
    executable: Path = typer.Option(
        Path("/tmp/honeydew-window-scout"),
        "--executable",
        help="Path to native Window Scout executable.",
    ),
) -> None:
    """List the approved macOS windows."""

    try:
        windows = discover_windows(executable)
    except FileNotFoundError:
        error_console.print("[red] Swift executable not found! [/red]")
        raise typer.Exit(code=1)
    except CalledProcessError:
        error_console.print("[red] Swift executable failed [/red]")
        raise typer.Exit(code=1)
    except TimeoutExpired:
        error_console.print("[red] Swift executable timed out [/red]")
        raise typer.Exit(code=1)
    except ValidationError:
        error_console.print("[red] Swift executable returned invalid JSON [/red]")
        raise typer.Exit(code=1)

    console.print("Honeydew 🍈")
    table = Table(title="Allowed windows")
    table.add_column("Window ID", style="cyan")
    table.add_column("Application name", style="magenta")
    table.add_column("Bundle ID", style="bold yellow")

    if not windows:
        console.print("[yellow] No windows found! [/yellow]")
        return

    for window in windows:
        table.add_row(str(window.id), window.application, window.bundleID)

    console.print(table)


if __name__ == "__main__":
    app()
