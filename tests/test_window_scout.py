import subprocess
from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from honeydew_learning import window_scout


def test_discover_windows_success(monkeypatch: MonkeyPatch) -> None:

    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
                args=["fake-helper"],
                returncode=0,
                stdout='''[{"id": 123,
                "application": "ChatGPT", 
                "bundleID": "com.openai.codex"}]''',
                stderr="",
            )



    monkeypatch.setattr(window_scout.subprocess, "run", fake_run,)

    windows = window_scout.discover_windows(
        Path("/fake/window-scout")
    )

    assert len(windows) == 1
    assert windows[0].application == "ChatGPT"
    assert windows[0].bundleID == "com.openai.codex"
    assert windows[0].id == 123

def test_discover_windows_invalid(monkeypatch: MonkeyPatch) -> None:

    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
                args=["fake-helper"],
                returncode=0,
                stdout='[{"id":123',
                stderr="",
            )



    monkeypatch.setattr(window_scout.subprocess, "run", fake_run,)


    with pytest.raises(ValidationError):
        window_scout.discover_windows(
            Path("/fake/window-scout")
        )

def test_discover_windows_process_failure(monkeypatch: MonkeyPatch) -> None:
    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(returncode=1, 
                                            cmd=["fake-helper"], 
                                            stderr="Window scout failed",)

    monkeypatch.setattr(window_scout.subprocess, "run", fake_run,)

    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        window_scout.discover_windows(Path("/fake/window-scout"))

    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Window scout failed"


