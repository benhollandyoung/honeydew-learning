from importlib.metadata import version

from pytest import MonkeyPatch
from typer.testing import CliRunner

from honeydew_learning import cli
from honeydew_learning.diagnostics import (
    Diagnostic,
    DiagnosticStatus,
)

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert version("honeydew_learning") in result.output


# def test_status_command() -> None:
#    result = runner.invoke(app, ["status"])
#
#   assert result.exit_code == 0
#    assert "Agent: not running" in result.output


def test_doctor_failure(monkeypatch: MonkeyPatch) -> None:
    def fake_diagnostics() -> list[Diagnostic]:
        return [
            Diagnostic(
                name="Operating system",
                status=DiagnosticStatus.FAIL,
                detail="macOS required",
            )
        ]

    monkeypatch.setattr(cli, "run_diagnostics", fake_diagnostics)

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 1
    assert "FAIL" in result.output
    assert "macOS required" in result.output


def test_doctor_warning(monkeypatch: MonkeyPatch) -> None:
    def fake_diagnostics() -> list[Diagnostic]:
        return [
            Diagnostic(
                name="Ollama",
                status=DiagnosticStatus.WARN,
                detail="Ollama not installed",
            )
        ]

    monkeypatch.setattr(cli, "run_diagnostics", fake_diagnostics)

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "WARN" in result.output
    assert "Ollama not installed" in result.output


def test_doctor_mixed(monkeypatch: MonkeyPatch) -> None:
    def fake_diagnostics() -> list[Diagnostic]:
        return [
            Diagnostic(
                name="Python",
                status=DiagnosticStatus.FAIL,
                detail="Python 3.12+ not installed",
            ),
            Diagnostic(
                name="Swift",
                status=DiagnosticStatus.WARN,
                detail="Swift compiler not installed",
            ),
            Diagnostic(
                name="Ollama",
                status=DiagnosticStatus.PASS,
                detail="Ollama installed",
            ),
        ]

    monkeypatch.setattr(cli, "run_diagnostics", fake_diagnostics)

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 1
    assert "FAIL" in result.output
    assert "WARN" in result.output
    assert "PASS" in result.output

    assert "Python 3.12+ not installed" in result.output
    assert "Swift compiler not installed" in result.output
    assert "Ollama installed" in result.output
