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


def test_scaffold_perf_case_write_creates_placeholder_skeleton(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    import scripts.cli as cli

    root = tmp_path / "repo"
    case_root = root / "cases" / "PERF"
    registry_dir = root / "inventory"
    report_dir = root / "reports" / "cli"
    case_root.mkdir(parents=True)
    registry_dir.mkdir(parents=True)
    registry_path = registry_dir / "case_registry.csv"
    registry_path.write_text(",".join(cli.CASE_REQUIRED_FIELDS) + "\n", encoding="utf-8")

    monkeypatch.setattr(cli, "ROOT", root)
    monkeypatch.setattr(cli, "REPORT_DIR", report_dir)
    monkeypatch.setattr(cli, "CASE_REGISTRY", registry_path)
    monkeypatch.setattr(cli, "PERF_CASE_ROOT", case_root)
    monkeypatch.setattr(cli, "PERF_TEMPLATE_DIR", case_root / "PERF_0002")

    exit_code = cli.main(
        [
            "scaffold-perf-case",
            "--case-id",
            "PERF_9099",
            "--out",
            "cases/PERF/PERF_9099",
            "--write",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["command"] == "scaffold-perf-case"
    assert payload["mode"] == "write"
    assert payload["ok"] is True
    assert payload["updated_registries"] == []
    assert payload["admission_or_review_claims"] == []
    assert "cases/PERF/PERF_9099/manifest.yaml" in payload["created_files"]
    assert "cases/PERF/PERF_9099/provenance/raw_record.json" in payload["created_files"]
    assert set(payload["source_lineage_and_provenance"]) == {
        "always_human_required",
        "placeholder_fields",
        "never_auto_infer",
    }

    scaffold_root = case_root / "PERF_9099"
    assert (scaffold_root / "manifest.yaml").is_file()
    assert (scaffold_root / "source.sql").read_text(encoding="utf-8").startswith("-- TODO")
    assert "source_id: TODO" in (scaffold_root / "manifest.yaml").read_text(encoding="utf-8")
    assert "PERF_9099" not in registry_path.read_text(encoding="utf-8")
