from __future__ import annotations

import subprocess
import sys


def test_cli_help_smoke() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "--help"],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "registry-check" in completed.stdout
    assert "current-snapshot" in completed.stdout
