#!/usr/bin/env python3
"""
Human-run-only contamination hash checker for formal R-Bot gate closure.

This script does not call any LLM or API, does not run R-Bot, and does not
execute SQL. It reads denominator source SQL files, computes deterministic
normalized hashes, and compares them against visible corpus/generated outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def find_repo_root(start_path: Path) -> Path:
    marker_relpath = Path("reports") / "curation" / "common_core_v0_final_denominator.csv"
    for candidate in [start_path.resolve(), *start_path.resolve().parents]:
        if (candidate / ".git").is_dir() or (candidate / marker_relpath).is_file():
            return candidate
    raise RuntimeError(f"Unable to locate repo root from {start_path}")


FREEZE_DIR = Path(__file__).resolve().parent
ROOT = find_repo_root(FREEZE_DIR)

DENOMINATOR_CSV = ROOT / "reports" / "curation" / "common_core_v0_final_denominator.csv"
BASE_ATTESTATION_CSV = FREEZE_DIR / "formal_contamination_attestation_v1.csv"
MANIFEST_DRAFT_CSV = FREEZE_DIR / "formal_corpus_manifest_draft.csv"

OUT_ATTESTATION_CSV = FREEZE_DIR / "formal_contamination_attestation_checked_v1.csv"
OUT_SUMMARY_MD = FREEZE_DIR / "formal_contamination_attestation_checked_summary.md"
OUT_HASHES_JSON = FREEZE_DIR / "formal_contamination_hashes_v1.json"

GENERATED_FAMILIES = {
    "sqlglot": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "sqlglot_same_engine_generation_01" / "generated",
    "direct_llm": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "direct_llm_same_engine_generation_01" / "generated",
    "calcite": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "calcite_same_engine_generation_01" / "generated",
    "r_bot_pg1_recovery": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "r_bot_pg1_recovery_canary_01" / "generated",
}


@dataclass
class HashRecord:
    label: str
    path: str
    normalized_hash: str


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--[^\n\r]*", " ", sql)
    return sql


def normalize_sql(sql: str) -> str:
    sql = strip_sql_comments(sql)
    sql = sql.strip()
    sql = re.sub(r";+\s*$", "", sql)
    sql = sql.lower()
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_sql_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.sql") if path.is_file())


def safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError:
        return None


def load_manifest_text_hashes() -> tuple[list[HashRecord], list[str]]:
    rows = read_csv_rows(MANIFEST_DRAFT_CSV)
    records: list[HashRecord] = []
    blockers: list[str] = []
    for row in rows:
        if row.get("include_or_exclude") != "include":
            continue
        candidate = Path(row["path"])
        if not candidate.exists():
            blockers.append(f"manifest_path_missing:{candidate}")
            continue
        text = safe_read_text(candidate)
        if text is None:
            blockers.append(f"manifest_text_unavailable:{candidate}")
            continue
        normalized = normalize_sql(text)
        if not normalized:
            blockers.append(f"manifest_text_empty_after_normalization:{candidate}")
            continue
        records.append(
            HashRecord(
                label=row["manifest_item_id"],
                path=str(candidate),
                normalized_hash=sha256_text(normalized),
            )
        )
    return records, blockers


def load_generated_hashes() -> tuple[dict[str, list[HashRecord]], list[str]]:
    by_family: dict[str, list[HashRecord]] = {}
    blockers: list[str] = []
    for family, base_dir in GENERATED_FAMILIES.items():
        family_records: list[HashRecord] = []
        if not base_dir.exists():
            blockers.append(f"generated_source_missing:{family}:{base_dir}")
            by_family[family] = family_records
            continue
        for path in iter_sql_files(base_dir):
            text = safe_read_text(path)
            if text is None:
                blockers.append(f"generated_text_unavailable:{path}")
                continue
            normalized = normalize_sql(text)
            if not normalized:
                blockers.append(f"generated_text_empty_after_normalization:{path}")
                continue
            family_records.append(
                HashRecord(label=family, path=str(path), normalized_hash=sha256_text(normalized))
            )
        by_family[family] = family_records
    return by_family, blockers


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal contamination hash checker")
    parser.add_argument("--output-dir", default=str(FREEZE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / OUT_ATTESTATION_CSV.name
    out_md = output_dir / OUT_SUMMARY_MD.name
    out_json = output_dir / OUT_HASHES_JSON.name

    denominator_rows = [r for r in read_csv_rows(DENOMINATOR_CSV) if r["included_in_common_core_v0"] == "yes"]
    base_rows = {r["case_id"]: r for r in read_csv_rows(BASE_ATTESTATION_CSV)}

    manifest_records, manifest_blockers = load_manifest_text_hashes()
    generated_hashes, generated_blockers = load_generated_hashes()
    manifest_hash_set = {record.normalized_hash for record in manifest_records}
    generated_hash_set = {
        family: {record.normalized_hash for record in records} for family, records in generated_hashes.items()
    }

    checked_rows: list[dict[str, str]] = []
    hash_payload: dict[str, object] = {
        "normalization_policy": {
            "strip_line_comments": True,
            "strip_block_comments": True,
            "lowercase_all_text": True,
            "collapse_whitespace": True,
            "remove_trailing_semicolon": True,
        },
        "cases": [],
        "manifest_blockers": manifest_blockers,
        "generated_output_blockers": generated_blockers,
    }

    for row in denominator_rows:
        case_id = row["case_id"]
        pool = row["pool"]
        source_sql = ROOT / "cases" / case_id.split("_")[0] / case_id / "source.sql"
        checked = {
            "case_id": case_id,
            "pool": pool,
            "normalized_source_hash_available": "no",
            "normalized_source_hash": "",
            "excluded_from_retrieval": "blocked",
            "exact_match_checked": "no",
            "exact_match_found_in_manifest": "blocked",
            "exact_match_found_in_generated_outputs": "blocked",
            "near_duplicate_checked": "no",
            "generated_outputs_excluded": "blocked",
            "attestation_status": "blocked_missing_source_sql",
            "blocker_reason": "",
        }
        case_payload: dict[str, object] = {
            "case_id": case_id,
            "pool": pool,
            "source_sql_path": str(source_sql),
        }

        if not source_sql.exists():
            checked["blocker_reason"] = f"missing source SQL: {source_sql}"
            checked_rows.append(checked)
            hash_payload["cases"].append(case_payload)
            continue

        source_text = safe_read_text(source_sql)
        if source_text is None:
            checked["attestation_status"] = "blocked_missing_source_sql"
            checked["blocker_reason"] = f"unreadable source SQL: {source_sql}"
            checked_rows.append(checked)
            hash_payload["cases"].append(case_payload)
            continue

        normalized = normalize_sql(source_text)
        normalized_hash = sha256_text(normalized)
        checked["normalized_source_hash_available"] = "yes"
        checked["normalized_source_hash"] = normalized_hash
        checked["exact_match_checked"] = "yes"
        checked["exact_match_found_in_manifest"] = "yes" if normalized_hash in manifest_hash_set else "no"
        exact_generated_match = any(normalized_hash in hashes for hashes in generated_hash_set.values())
        checked["exact_match_found_in_generated_outputs"] = "yes" if exact_generated_match else "no"

        missing_generated_sources = [family for family, base_dir in GENERATED_FAMILIES.items() if not base_dir.exists()]
        if missing_generated_sources:
            checked["generated_outputs_excluded"] = "blocked"
        else:
            checked["generated_outputs_excluded"] = "no_exact_match_found" if not exact_generated_match else "exact_match_found"

        blocked_reasons: list[str] = []
        if checked["exact_match_found_in_manifest"] == "yes":
            blocked_reasons.append("exact normalized hash found in visible manifest text item")
        if checked["exact_match_found_in_generated_outputs"] == "yes":
            blocked_reasons.append("exact normalized hash found in visible generated outputs")
        if manifest_blockers:
            blocked_reasons.append("manifest text coverage incomplete")
        if generated_blockers:
            blocked_reasons.append("generated output coverage incomplete")
        blocked_reasons.append("near-duplicate check not implemented")

        checked["near_duplicate_checked"] = "no"
        checked["excluded_from_retrieval"] = (
            "blocked" if blocked_reasons else "yes"
        )
        checked["attestation_status"] = "blocked_pending_near_duplicate_check" if not blocked_reasons[:-1] else "blocked_partial_check_only"
        checked["blocker_reason"] = "; ".join(blocked_reasons)

        case_payload.update(
            {
                "normalized_source_hash": normalized_hash,
                "exact_match_in_manifest": checked["exact_match_found_in_manifest"] == "yes",
                "exact_match_in_generated_outputs": checked["exact_match_found_in_generated_outputs"] == "yes",
            }
        )
        checked_rows.append(checked)
        hash_payload["cases"].append(case_payload)

    fieldnames = [
        "case_id",
        "pool",
        "normalized_source_hash_available",
        "normalized_source_hash",
        "excluded_from_retrieval",
        "exact_match_checked",
        "exact_match_found_in_manifest",
        "exact_match_found_in_generated_outputs",
        "near_duplicate_checked",
        "generated_outputs_excluded",
        "attestation_status",
        "blocker_reason",
    ]
    write_csv(out_csv, checked_rows, fieldnames)

    passed = sum(1 for row in checked_rows if row["attestation_status"] == "passed")
    blocked = len(checked_rows) - passed
    out_md.write_text(
        "\n".join(
            [
                "# Formal Contamination Hash Check Summary",
                "",
                "## Status",
                "",
                f"- rows covered: `{len(checked_rows)}`",
                f"- rows passed: `{passed}`",
                f"- rows blocked: `{blocked}`",
                "",
                "## Normalization Policy",
                "",
                "- strip line comments: `yes`",
                "- strip block comments: `yes`",
                "- lowercase all text: `yes`",
                "- collapse whitespace: `yes`",
                "- remove trailing semicolon: `yes`",
                "",
                "## Coverage Gaps",
                "",
                f"- manifest blockers: `{len(manifest_blockers)}`",
                f"- generated-output blockers: `{len(generated_blockers)}`",
                "- near-duplicate check: `not implemented by this script`",
                "",
                "## Gate Impact",
                "",
                "- formal gate open: `no`",
                "- formal `R-Bot @120` generation may start: `no`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    out_json.write_text(json.dumps(hash_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
