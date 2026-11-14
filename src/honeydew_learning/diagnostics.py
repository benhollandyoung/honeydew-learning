import platform
import shutil
import sys
from dataclasses import dataclass
from enum import Enum


class DiagnosticStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class Diagnostic:
    name: str
    status: DiagnosticStatus
    detail: str


def run_diagnostics() -> list[Diagnostic]:
    os_check = platform.system() == "Darwin"
    py_check = sys.version_info >= (3, 12)
    swift_path = shutil.which("swift")
    ol_path = shutil.which("ollama")
    sw_check = swift_path is not None
    ol_check = ol_path is not None

    os = Diagnostic(
        name="Operating system",
        status=(DiagnosticStatus.PASS if os_check else DiagnosticStatus.FAIL),
        detail=("macOS detected" if os_check else "macOS required"),
    )

    py = Diagnostic(
        name="Python version",
        status=(DiagnosticStatus.PASS if py_check else DiagnosticStatus.FAIL),
        detail=(
            f"Python {sys.version_info.major}. "
            f"{sys.version_info.minor}.{sys.version_info.micro} installed"
            if py_check
            else "Python 3.12+ required"
        ),
    )

    sw = Diagnostic(
        name="Swift compiler",
        status=(DiagnosticStatus.PASS if sw_check else DiagnosticStatus.WARN),
        detail=(
            f"Swift compiler found: {swift_path}"
            if sw_check
            else "Swift compiler not found"
        ),
    )
    ol = Diagnostic(
        name="Ollama",
        status=(DiagnosticStatus.PASS if ol_check else DiagnosticStatus.WARN),
        detail=(f"Ollama found: {ol_path}" if ol_check else "Ollama not found"),
    )

    return [os, py, sw, ol]
