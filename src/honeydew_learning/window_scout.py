import subprocess
from collections.abc import Callable
from pathlib import Path

from pydantic import TypeAdapter

from honeydew_learning.models import WindowInfo

# This is a type-alias
Runner = Callable[..., subprocess.CompletedProcess[str]]


def discover_windows(
    executable: Path,
    *,
    runner: Runner = subprocess.run,
) -> list[WindowInfo]:
    result = runner(
        [str(executable)],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    adapter = TypeAdapter(list[WindowInfo])

    return adapter.validate_json(result.stdout)
