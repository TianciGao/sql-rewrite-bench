from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.common_core_v0_validation import validate_evaluation_package


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_denominator(path: Path, total_cases: int = 40) -> list[str]:
    case_ids = [f"PERF_{i:04d}" for i in range(1, total_cases + 1)]
    _write_csv(
        path,
        [
            "case_id",
            "pool",
            "source_family",
            "denominator_role",
            "notes_link",
            "caveat",
            "included_in_common_core_v0",
        ],
        [
            {
                "case_id": case_id,
                "pool": "performance",
                "source_family": "TPC-H",
                "denominator_role": "perf_denominator_case",
                "notes_link": "benchmark_spec/reviews/COMMON_CORE_V0_HUMAN_GATE_DECISIONS_DRAFT.md",
                "caveat": "",
                "included_in_common_core_v0": "yes",
            }
            for case_id in case_ids
        ],
    )
    return case_ids


def _write_manifest(path: Path, **overrides: object) -> None:
    payload = {
        "run_id": "run-001",
        "method_id": "demo-method",
        "git_commit": "abc1234",
        "denominator_id": "common_core_v0_40",
        "attempted_cases": 40,
        "is_leaderboard_method": True,
        "method_role": "same_engine",
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _run_event_row(case_id: str, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": "run-001",
        "event_id": f"evt-{case_id}",
        "method_id": "demo-method",
        "method_version": "v1",
        "case_id": case_id,
        "pool": "performance",
        "source_family": "TPC-H",
        "task_track": "same_engine",
        "engine_source": "",
        "engine_target": "postgresql",
        "rewrite_id": "rewrite_pos_01",
        "rewrite_role": "positive",
        "attempt_index": 1,
        "execution_phase": "execute",
        "status": "success",
        "failure_bucket": "",
        "is_denominator_case": "true",
        "is_valid_result": "true",
        "is_speedup_eligible": "true",
        "result_match_status": "match",
        "normalization_policy": "none",
        "baseline_runtime_ms": "10.0",
        "rewrite_runtime_ms": "8.0",
        "speedup_ratio": "1.25",
        "speedup_exclusion_reason": "",
        "plan_artifact_status": "present",
        "verifier_mode": "engine_local_witness",
        "artifact_path": "",
        "notes": "",
    }
    row.update(overrides)
    return row


def _write_run_event_long(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "run_id",
        "event_id",
        "method_id",
        "method_version",
        "case_id",
        "pool",
        "source_family",
        "task_track",
        "engine_source",
        "engine_target",
        "rewrite_id",
        "rewrite_role",
        "attempt_index",
        "execution_phase",
        "status",
        "failure_bucket",
        "is_denominator_case",
        "is_valid_result",
        "is_speedup_eligible",
        "result_match_status",
        "normalization_policy",
        "baseline_runtime_ms",
        "rewrite_runtime_ms",
        "speedup_ratio",
        "speedup_exclusion_reason",
        "plan_artifact_status",
        "verifier_mode",
        "artifact_path",
        "notes",
    ]
    _write_csv(path, fieldnames, rows)


def _write_method_case_summary(path: Path, case_ids: list[str]) -> None:
    _write_csv(
        path,
        [
            "run_id",
            "method_id",
            "case_id",
            "pool",
            "source_family",
            "included_in_denominator",
            "case_eval_status",
            "best_positive_rewrite_id",
            "best_negative_rewrite_id",
            "valid_positive_count",
            "failed_positive_count",
            "has_valid_baseline",
            "has_valid_plan_artifacts",
            "has_valid_result_check",
            "is_speedup_eligible_case",
            "best_speedup_ratio",
            "translation_success",
            "verifier_supported",
            "failure_bucket_primary",
            "caveat",
            "notes_link",
        ],
        [
            {
                "run_id": "run-001",
                "method_id": "demo-method",
                "case_id": case_id,
                "pool": "performance",
                "source_family": "TPC-H",
                "included_in_denominator": "true",
                "case_eval_status": "valid_success",
                "best_positive_rewrite_id": "rewrite_pos_01",
                "best_negative_rewrite_id": "rewrite_neg_01",
                "valid_positive_count": 1,
                "failed_positive_count": 0,
                "has_valid_baseline": "true",
                "has_valid_plan_artifacts": "true",
                "has_valid_result_check": "true",
                "is_speedup_eligible_case": "true",
                "best_speedup_ratio": "1.10",
                "translation_success": "",
                "verifier_supported": "true",
                "failure_bucket_primary": "",
                "caveat": "",
                "notes_link": "benchmark_spec/reviews/COMMON_CORE_V0_HUMAN_GATE_DECISIONS_DRAFT.md",
            }
            for case_id in case_ids
        ],
    )


def test_common_core_v0_validation_accepts_valid_synthetic_package(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"
    run_event_long = tmp_path / "run_event_long.csv"
    method_case_summary = tmp_path / "method_case_summary.csv"

    case_ids = _write_denominator(denominator)
    _write_manifest(manifest)
    _write_run_event_long(run_event_long, [_run_event_row(case_id) for case_id in case_ids])
    _write_method_case_summary(method_case_summary, case_ids)

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
        run_event_long_path=run_event_long,
        method_case_summary_path=method_case_summary,
    )

    assert payload["ok"] is True, payload
    assert payload["issue_count"] == 0


def test_common_core_v0_validation_rejects_unknown_case_id(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"
    run_event_long = tmp_path / "run_event_long.csv"

    case_ids = _write_denominator(denominator)
    _write_manifest(manifest)
    rows = [_run_event_row(case_ids[0]), _run_event_row("PERF_9999")]
    _write_run_event_long(run_event_long, rows)

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
        run_event_long_path=run_event_long,
    )

    codes = {issue["code"] for issue in payload["issues"]}
    assert "unknown_case_id" in codes


def test_common_core_v0_validation_rejects_speedup_without_eligibility(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"
    run_event_long = tmp_path / "run_event_long.csv"

    case_ids = _write_denominator(denominator)
    _write_manifest(manifest, attempted_cases=1)
    _write_run_event_long(
        run_event_long,
        [
            _run_event_row(
                case_ids[0],
                is_speedup_eligible="false",
                speedup_ratio="1.20",
                speedup_exclusion_reason="",
            )
        ],
    )

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
        run_event_long_path=run_event_long,
    )

    codes = Counter(issue["code"] for issue in payload["issues"])
    assert "speedup_present_for_ineligible_row" in codes
    assert "missing_speedup_exclusion_reason" in codes


def test_common_core_v0_validation_rejects_silent_denominator_drop(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"
    method_case_summary = tmp_path / "method_case_summary.csv"

    case_ids = _write_denominator(denominator)
    _write_manifest(manifest, attempted_cases=40)
    _write_method_case_summary(method_case_summary, case_ids[:39])

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
        method_case_summary_path=method_case_summary,
    )

    codes = {issue["code"] for issue in payload["issues"]}
    assert "silent_denominator_drop" in codes


def test_common_core_v0_validation_rejects_support_method_marked_as_leaderboard(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"

    _write_denominator(denominator)
    _write_manifest(
        manifest,
        method_role="verifier_support",
        is_leaderboard_method=True,
        attempted_cases=0,
    )

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
    )

    codes = {issue["code"] for issue in payload["issues"]}
    assert "support_method_marked_as_leaderboard" in codes


def test_common_core_v0_validation_rejects_port_translation_in_same_engine_leaderboard(tmp_path: Path) -> None:
    denominator = tmp_path / "denominator.csv"
    manifest = tmp_path / "manifest.json"
    leaderboard = tmp_path / "same_engine_leaderboard.csv"

    _write_denominator(denominator)
    _write_manifest(manifest, attempted_cases=0)
    _write_csv(
        leaderboard,
        [
            "run_id",
            "method_id",
            "engine_target",
            "pool_scope",
            "denominator_cases",
            "valid_success_cases",
            "speedup_eligible_cases",
            "gm_speedup",
            "pass_rate",
            "coverage_rate",
            "result_validity_rate",
            "plan_observability_rate",
            "notes",
            "route_id",
        ],
        [
            {
                "run_id": "run-001",
                "method_id": "demo-method",
                "engine_target": "postgresql",
                "pool_scope": "all",
                "denominator_cases": 40,
                "valid_success_cases": 0,
                "speedup_eligible_cases": 0,
                "gm_speedup": "",
                "pass_rate": 0.0,
                "coverage_rate": 0.0,
                "result_validity_rate": 0.0,
                "plan_observability_rate": 0.0,
                "notes": "",
                "route_id": "port_translation",
            }
        ],
    )

    payload = validate_evaluation_package(
        denominator_path=denominator,
        manifest_path=manifest,
        same_engine_leaderboard_path=leaderboard,
    )

    codes = {issue["code"] for issue in payload["issues"]}
    assert "port_translation_mixed_into_same_engine" in codes
