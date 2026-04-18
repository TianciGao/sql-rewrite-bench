from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


def run_cli_json(command: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.cli", command],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout)


def test_registry_check_json_shape() -> None:
    payload = run_cli_json("registry-check")

    assert {
        "command",
        "ok",
        "ran_at_utc",
        "report_path",
        "error_count",
        "checks",
        "registries",
        "errors",
    }.issubset(payload)
    assert payload["command"] == "registry-check"
    assert {"source_registry", "case_registry"}.issubset(payload["registries"])
    assert {"schema", "controlled_field_counts"}.issubset(payload["registries"]["source_registry"])
    assert {"schema", "controlled_field_counts", "validated_engine_counts"}.issubset(
        payload["registries"]["case_registry"]
    )
    assert isinstance(payload["checks"], list)
    assert isinstance(payload["errors"], list)


def test_current_snapshot_json_shape() -> None:
    payload = run_cli_json("current-snapshot")

    assert {
        "command",
        "ok",
        "ran_at_utc",
        "report_path",
        "basis",
        "sources",
        "cases",
    }.issubset(payload)
    assert payload["command"] == "current-snapshot"
    assert {"sources", "cases"}.issubset(payload["basis"])
    assert {"total", "counts"}.issubset(payload["sources"])
    assert {"by_acquisition_status", "by_current_real_status"}.issubset(
        payload["sources"]["counts"]
    )
    assert {"total", "counts", "engine_coverage"}.issubset(payload["cases"])
    assert {
        "by_pool",
        "by_admission_status",
        "by_promotion_status",
        "by_dataset_line",
        "by_validated_engine_set",
    }.issubset(payload["cases"]["counts"])
    assert {
        "case_count_by_engine",
        "tri_engine_validated_case_count",
    }.issubset(payload["cases"]["engine_coverage"])
