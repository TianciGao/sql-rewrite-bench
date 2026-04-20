from __future__ import annotations

import json
import subprocess
import sys


def test_scaffold_port_case_dry_run_shape() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.cli",
            "scaffold-port-case",
            "--case-id",
            "PORT_9999",
            "--out",
            "cases/PORT/PORT_9999",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)

    assert payload["command"] == "scaffold-port-case"
    assert payload["ok"] is True
    assert payload["mode"] == "dry-run"
    assert payload["template_basis"]["case_id"] == "PORT_0002"
    assert payload["created_files"] == []
    assert payload["updated_registries"] == []
    assert payload["admission_or_review_claims"] == []
    assert "rewrite_pos_02_spark.sql" in payload["planned_files"]
    assert "source dialect classification" in payload["human_required_fields"]
    assert "admission status" in payload["forbidden_automatic_decisions"]
    assert (
        "source dialect vs target dialect rewrites must be explicit"
        in payload["portability_specific_requirements"]
    )
