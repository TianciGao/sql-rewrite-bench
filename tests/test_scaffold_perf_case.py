from __future__ import annotations

import json
import subprocess
import sys


def test_scaffold_perf_case_dry_run_shape() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.cli",
            "scaffold-perf-case",
            "--case-id",
            "PERF_9999",
            "--out",
            "cases/PERF/PERF_9999",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)

    assert payload["command"] == "scaffold-perf-case"
    assert payload["ok"] is True
    assert payload["mode"] == "dry-run"
    assert payload["template_basis"]["case_id"] == "PERF_0002"
    assert payload["created_files"] == []
    assert payload["updated_registries"] == []
    assert payload["admission_or_review_claims"] == []
    assert "manifest.yaml" in payload["planned_files"]
    assert "source SQL text" in payload["human_required_fields"]
    assert "admission status" in payload["forbidden_automatic_decisions"]
