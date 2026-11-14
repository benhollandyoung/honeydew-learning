import subprocess
from pathlib import Path

from pydantic import TypeAdapter

from honeydew_learning.models import WindowInfo


def discover_windows(executable: Path) -> list[WindowInfo]:
    result = subprocess.run(
            [str(executable)],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    adapter = TypeAdapter(list[WindowInfo])

    return adapter.validate_json(result.stdout)
