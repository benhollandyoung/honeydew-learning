import subprocess
from pathlib import Path

import pytest
from pydantic import ValidationError

from honeydew_learning import window_scout


def test_discover_windows_success() -> None:
    def fake_run(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        assert command == ["/fake/window-scout"]
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["check"] is True
        assert kwargs["timeout"] == 10

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=(
                '[{"id": 123, "application": "ChatGPT", '
                '"bundleID": "com.openai.codex"}]'
            ),
            stderr="",
        )

    windows = window_scout.discover_windows(
        Path("/fake/window-scout"),
        runner=fake_run,
    )

    assert len(windows) == 1
    assert windows[0].application == "ChatGPT"
    assert windows[0].bundleID == "com.openai.codex"
    assert windows[0].id == 123


def test_discover_windows_malformed_json() -> None:

    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["fake-helper"],
            returncode=0,
            stdout='[{"id":123',
            stderr="",
        )

    with pytest.raises(ValidationError):
        window_scout.discover_windows(
            Path("/fake/window-scout"),
            runner=fake_run,
        )


def test_discover_windows_process_failure() -> None:
    def fake_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=["fake-helper"],
            stderr="Window scout failed",
        )

    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        window_scout.discover_windows(Path("/fake/window-scout"), runner=fake_run)

    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Window scout failed"
