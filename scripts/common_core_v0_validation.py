from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DENOMINATOR = ROOT / "reports" / "curation" / "common_core_v0_final_denominator.csv"
EVAL_DIR = ROOT / "reports" / "evaluation" / "common_core_v0"
DEFAULT_SCHEMA_DIR = EVAL_DIR
DEFAULT_MANIFEST_SCHEMA = EVAL_DIR / "run_manifest.schema.json"
EXPECTED_DENOMINATOR_ID = "common_core_v0_40"

CSV_SCHEMA_FILES = {
    "run_event_long": EVAL_DIR / "run_event_long.schema.csv",
    "method_case_summary": EVAL_DIR / "method_case_summary.schema.csv",
    "same_engine_leaderboard": EVAL_DIR / "same_engine_leaderboard.schema.csv",
    "controls_summary": EVAL_DIR / "controls_summary.schema.csv",
    "port_translation_summary": EVAL_DIR / "port_translation_summary.schema.csv",
    "verifier_support_summary": EVAL_DIR / "verifier_support_summary.schema.csv",
    "plan_observability_summary": EVAL_DIR / "plan_observability_summary.schema.csv",
    "failure_bucket_summary": EVAL_DIR / "failure_bucket_summary.schema.csv",
}

REQUIRED_COMMON_CORE_VALUES = {
    "common_core_v0_40",
}

SUPPORT_ONLY_METHOD_ROLES = {
    "verifier_support",
    "support_only",
    "verifier_only",
}

TRUE_VALUES = {"true", "yes", "1", "y"}
FALSE_VALUES = {"false", "no", "0", "n", ""}


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
        }


def _read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return reader.fieldnames or [], rows


def _read_schema_columns(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "column_name" not in (reader.fieldnames or []):
            raise ValueError(f"{path} does not contain a column_name header")
        return [row["column_name"] for row in reader if row.get("column_name")]


def _load_denominator_case_ids(path: Path) -> set[str]:
    _, rows = _read_csv_rows(path)
    return {row["case_id"] for row in rows if row.get("case_id")}


def _load_manifest(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _boolish(value: Any) -> bool | None:
    lowered = _stringify(value).strip().lower()
    if lowered in TRUE_VALUES:
        return True
    if lowered in FALSE_VALUES:
        return False
    return None


def _row_value(row: dict[str, str], *candidates: str) -> str:
    for key in candidates:
        value = row.get(key, "")
        if value not in ("", None):
            return value
    return ""


def _has_disallowed_claim(value: Any) -> bool:
    return "admitted_common_core" in _stringify(value)


def _is_invalid_or_inconsistent(row: dict[str, str]) -> bool:
    status = _stringify(row.get("status")).strip().lower()
    valid_result = _boolish(row.get("is_valid_result"))
    result_match = _stringify(row.get("result_match_status")).strip().lower()
    return (
        status not in {"success", ""}
        or valid_result is False
        or result_match == "mismatch"
    )


def _validate_manifest_shape(manifest: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not manifest:
        return issues

    required = {
        "run_id",
        "method_id",
        "git_commit",
        "denominator_id",
        "attempted_cases",
        "is_leaderboard_method",
        "method_role",
    }
    missing = sorted(key for key in required if key not in manifest)
    if missing:
        issues.append(
            ValidationIssue(
                "manifest_missing_required_fields",
                f"Manifest is missing required fields: {', '.join(missing)}",
            )
        )

    denominator_id = manifest.get("denominator_id")
    if denominator_id != EXPECTED_DENOMINATOR_ID:
        issues.append(
            ValidationIssue(
                "manifest_invalid_denominator_id",
                f"Manifest denominator_id must equal {EXPECTED_DENOMINATOR_ID}, got {denominator_id!r}",
            )
        )

    method_role = _stringify(manifest.get("method_role")).strip()
    is_leaderboard_method = _boolish(manifest.get("is_leaderboard_method"))
    if method_role in SUPPORT_ONLY_METHOD_ROLES and is_leaderboard_method is True:
        issues.append(
            ValidationIssue(
                "support_method_marked_as_leaderboard",
                "Verifier/support methods must not be marked is_leaderboard_method=yes",
            )
        )

    for key, value in manifest.items():
        if _has_disallowed_claim(value):
            issues.append(
                ValidationIssue(
                    "manifest_claims_admitted_common_core",
                    f"Manifest field {key!r} contains disallowed value 'admitted_common_core'",
                )
            )

    return issues


def _validate_schema_columns(csv_name: str, csv_path: Path, schema_path: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    actual_columns, _ = _read_csv_rows(csv_path)
    expected_columns = _read_schema_columns(schema_path)
    missing = [column for column in expected_columns if column not in actual_columns]
    if missing:
        issues.append(
            ValidationIssue(
                "missing_schema_columns",
                f"{csv_name} is missing expected schema columns: {', '.join(missing)}",
            )
        )
    return issues


def _validate_run_event_long(
    csv_path: Path,
    denominator_case_ids: set[str],
    manifest: dict[str, Any],
) -> tuple[list[ValidationIssue], set[str], int]:
    issues: list[ValidationIssue] = []
    columns, rows = _read_csv_rows(csv_path)
    distinct_case_ids: set[str] = set()

    required_alias_groups = {
        "run_id": ("run_id",),
        "method_id": ("method_id",),
        "route_id": ("route_id", "task_track"),
        "engine": ("engine", "engine_target"),
        "git_commit": ("git_commit",),
        "denominator_id": ("denominator_id",),
    }
    for idx, row in enumerate(rows, start=2):
        case_id = _stringify(row.get("case_id")).strip()
        if case_id:
            distinct_case_ids.add(case_id)
        if case_id and case_id not in denominator_case_ids:
            issues.append(
                ValidationIssue(
                    "unknown_case_id",
                    f"{csv_path.name}:{idx} contains case_id {case_id!r} outside the frozen denominator",
                )
            )

        for label, candidates in required_alias_groups.items():
            value = _row_value(row, *candidates)
            if label in {"git_commit", "denominator_id"} and not value:
                value = _stringify(manifest.get(label))
            if not _stringify(value).strip():
                issues.append(
                    ValidationIssue(
                        "missing_governance_field",
                        f"{csv_path.name}:{idx} does not resolve required field {label!r}",
                    )
                )

        resolved_denominator_id = _row_value(row, "denominator_id") or _stringify(manifest.get("denominator_id"))
        if resolved_denominator_id not in REQUIRED_COMMON_CORE_VALUES:
            issues.append(
                ValidationIssue(
                    "invalid_row_denominator_id",
                    f"{csv_path.name}:{idx} must resolve denominator_id={EXPECTED_DENOMINATOR_ID}, got {resolved_denominator_id!r}",
                )
            )

        is_speedup_eligible = _boolish(row.get("is_speedup_eligible"))
        speedup_ratio = _stringify(row.get("speedup_ratio")).strip()
        speedup_exclusion_reason = _stringify(row.get("speedup_exclusion_reason")).strip()
        if speedup_ratio and is_speedup_eligible is not True:
            issues.append(
                ValidationIssue(
                    "speedup_present_for_ineligible_row",
                    f"{csv_path.name}:{idx} has speedup_ratio but is_speedup_eligible is not true",
                )
            )

        if (is_speedup_eligible is False or _is_invalid_or_inconsistent(row)) and not speedup_exclusion_reason:
            issues.append(
                ValidationIssue(
                    "missing_speedup_exclusion_reason",
                    f"{csv_path.name}:{idx} is invalid/inconsistent or not speedup-eligible but lacks speedup_exclusion_reason",
                )
            )

        for key, value in row.items():
            if _has_disallowed_claim(value):
                issues.append(
                    ValidationIssue(
                        "row_claims_admitted_common_core",
                        f"{csv_path.name}:{idx} field {key!r} contains disallowed value 'admitted_common_core'",
                    )
                )

    return issues, distinct_case_ids, len(rows)


def _validate_method_case_summary(
    csv_path: Path,
    denominator_case_ids: set[str],
    manifest: dict[str, Any],
) -> tuple[list[ValidationIssue], set[str]]:
    issues: list[ValidationIssue] = []
    _, rows = _read_csv_rows(csv_path)
    seen_case_ids: set[str] = set()
    for idx, row in enumerate(rows, start=2):
        case_id = _stringify(row.get("case_id")).strip()
        if case_id:
            seen_case_ids.add(case_id)
        if case_id and case_id not in denominator_case_ids:
            issues.append(
                ValidationIssue(
                    "unknown_case_id",
                    f"{csv_path.name}:{idx} contains case_id {case_id!r} outside the frozen denominator",
                )
            )
        for field in ("run_id", "method_id"):
            if not _stringify(row.get(field)).strip():
                issues.append(
                    ValidationIssue(
                        "missing_governance_field",
                        f"{csv_path.name}:{idx} is missing required field {field!r}",
                    )
                )
        if _has_disallowed_claim(row):
            issues.append(
                ValidationIssue(
                    "row_claims_admitted_common_core",
                    f"{csv_path.name}:{idx} contains disallowed value 'admitted_common_core'",
                )
            )

    attempted_cases = manifest.get("attempted_cases")
    if attempted_cases == 40:
        if len(seen_case_ids) != 40:
            issues.append(
                ValidationIssue(
                    "silent_denominator_drop",
                    f"Manifest claims attempted_cases=40 but {csv_path.name} contains {len(seen_case_ids)} distinct cases",
                )
            )
    return issues, seen_case_ids


def _validate_same_engine_leaderboard(csv_path: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _, rows = _read_csv_rows(csv_path)
    for idx, row in enumerate(rows, start=2):
        haystacks = [
            _stringify(row.get("notes")),
            _stringify(row.get("route_id")),
            _stringify(row.get("route_scope")),
            _stringify(row.get("pool_scope")),
        ]
        if any("port_translation" in text.lower() for text in haystacks):
            issues.append(
                ValidationIssue(
                    "port_translation_mixed_into_same_engine",
                    f"{csv_path.name}:{idx} appears to mix PORT translation routes into same_engine_leaderboard",
                )
            )
        if _has_disallowed_claim(row):
            issues.append(
                ValidationIssue(
                    "row_claims_admitted_common_core",
                    f"{csv_path.name}:{idx} contains disallowed value 'admitted_common_core'",
                )
            )
    return issues


def validate_evaluation_package(
    *,
    denominator_path: Path = DEFAULT_DENOMINATOR,
    manifest_path: Path | None = None,
    run_event_long_path: Path | None = None,
    method_case_summary_path: Path | None = None,
    same_engine_leaderboard_path: Path | None = None,
    controls_summary_path: Path | None = None,
    port_translation_summary_path: Path | None = None,
    verifier_support_summary_path: Path | None = None,
    plan_observability_summary_path: Path | None = None,
    failure_bucket_summary_path: Path | None = None,
) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    denominator_case_ids = _load_denominator_case_ids(denominator_path)
    manifest = _load_manifest(manifest_path)

    issues.extend(_validate_manifest_shape(manifest))

    artifact_paths = {
        "run_event_long": run_event_long_path,
        "method_case_summary": method_case_summary_path,
        "same_engine_leaderboard": same_engine_leaderboard_path,
        "controls_summary": controls_summary_path,
        "port_translation_summary": port_translation_summary_path,
        "verifier_support_summary": verifier_support_summary_path,
        "plan_observability_summary": plan_observability_summary_path,
        "failure_bucket_summary": failure_bucket_summary_path,
    }

    distinct_run_event_cases: set[str] = set()
    distinct_summary_cases: set[str] = set()
    for csv_name, csv_path in artifact_paths.items():
        if csv_path is None:
            continue
        schema_path = CSV_SCHEMA_FILES[csv_name]
        issues.extend(_validate_schema_columns(csv_name, csv_path, schema_path))

        if csv_name == "run_event_long":
            run_issues, case_ids, _ = _validate_run_event_long(csv_path, denominator_case_ids, manifest)
            issues.extend(run_issues)
            distinct_run_event_cases = case_ids
        elif csv_name == "method_case_summary":
            summary_issues, case_ids = _validate_method_case_summary(csv_path, denominator_case_ids, manifest)
            issues.extend(summary_issues)
            distinct_summary_cases = case_ids
        elif csv_name == "same_engine_leaderboard":
            issues.extend(_validate_same_engine_leaderboard(csv_path))
        else:
            _, rows = _read_csv_rows(csv_path)
            for idx, row in enumerate(rows, start=2):
                if _has_disallowed_claim(row):
                    issues.append(
                        ValidationIssue(
                            "row_claims_admitted_common_core",
                            f"{csv_path.name}:{idx} contains disallowed value 'admitted_common_core'",
                        )
                    )

    attempted_cases = manifest.get("attempted_cases")
    if attempted_cases == 40:
        observed = len(distinct_summary_cases or distinct_run_event_cases)
        if observed and observed != 40:
            issues.append(
                ValidationIssue(
                    "silent_denominator_drop",
                    f"Manifest claims attempted_cases=40 but only {observed} distinct denominator cases are present",
                )
            )

    payload = {
        "ok": not issues,
        "denominator_id_expected": EXPECTED_DENOMINATOR_ID,
        "denominator_case_count": len(denominator_case_ids),
        "artifacts_checked": [name for name, path in artifact_paths.items() if path is not None],
        "issue_count": len(issues),
        "issues": [issue.as_dict() for issue in issues],
    }
    return payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Common-core v0 evaluation scaffolding artifacts.")
    parser.add_argument("--denominator", type=Path, default=DEFAULT_DENOMINATOR)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--run-event-long", type=Path)
    parser.add_argument("--method-case-summary", type=Path)
    parser.add_argument("--same-engine-leaderboard", type=Path)
    parser.add_argument("--controls-summary", type=Path)
    parser.add_argument("--port-translation-summary", type=Path)
    parser.add_argument("--verifier-support-summary", type=Path)
    parser.add_argument("--plan-observability-summary", type=Path)
    parser.add_argument("--failure-bucket-summary", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    payload = validate_evaluation_package(
        denominator_path=args.denominator,
        manifest_path=args.manifest,
        run_event_long_path=args.run_event_long,
        method_case_summary_path=args.method_case_summary,
        same_engine_leaderboard_path=args.same_engine_leaderboard,
        controls_summary_path=args.controls_summary,
        port_translation_summary_path=args.port_translation_summary,
        verifier_support_summary_path=args.verifier_support_summary,
        plan_observability_summary_path=args.plan_observability_summary,
        failure_bucket_summary_path=args.failure_bucket_summary,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"ok={payload['ok']} issue_count={payload['issue_count']}")
        for issue in payload["issues"]:
            print(f"[{issue['severity']}] {issue['code']}: {issue['message']}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
