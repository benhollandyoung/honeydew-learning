import shutil

from pytest import MonkeyPatch

from honeydew_learning import diagnostics
from honeydew_learning.diagnostics import DiagnosticStatus


def test_missing_swift(monkeypatch: MonkeyPatch) -> None:
    def fake_which(command: str) -> str | None:
        if command == "swift":
            return None
        return f"/usr/bin/{command}"
    
    monkeypatch.setattr(
            shutil,
            "which",
            fake_which,
    )

    results = diagnostics.run_diagnostics()

    swift =  next( result for result in results if result.name == "Swift compiler")

    assert swift.status == DiagnosticStatus.WARN


def test_mising_ollama(monkeypatch: MonkeyPatch) -> None:
    def fake_which(command: str) -> str | None:
        if command == "ollama":
            return None
        return f"/usr/bin/{command}" 

    monkeypatch.setattr(shutil, "which", fake_which)

    results = diagnostics.run_diagnostics()

    ollama = next(result for result in results if result.name == "Ollama")

    assert ollama.status == DiagnosticStatus.WARN
    assert ollama.detail == "Ollama not found"

