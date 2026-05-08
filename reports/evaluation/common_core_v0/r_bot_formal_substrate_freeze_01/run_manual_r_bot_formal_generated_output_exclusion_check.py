#!/usr/bin/env python3
"""
Human-run-only generated-output exclusion checker for formal R-Bot gate closure.

This script does not call any LLM or API, does not run R-Bot, and does not
execute SQL. It reads known generated SQL outputs, computes deterministic
normalized hashes, and checks whether those generated outputs are present in
visible text-readable included corpus manifest entries.
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

MANIFEST_DRAFT_CSV = FREEZE_DIR / "formal_corpus_manifest_draft.csv"

OUT_CSV = FREEZE_DIR / "formal_generated_output_exclusion_v1.csv"
OUT_SUMMARY_MD = FREEZE_DIR / "formal_generated_output_exclusion_summary.md"
OUT_HASHES_JSON = FREEZE_DIR / "formal_generated_output_hashes_v1.json"

GENERATED_FAMILIES = {
    "sqlglot": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "sqlglot_same_engine_generation_01" / "generated",
    "direct_llm": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "direct_llm_same_engine_generation_01" / "generated",
    "calcite": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "calcite_same_engine_generation_01" / "generated",
    "r_bot_pg1_recovery": ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "r_bot_pg1_recovery_canary_01" / "generated",
}


@dataclass
class HashRecord:
    item_id: str
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
                item_id=row["manifest_item_id"],
                path=str(candidate),
                normalized_hash=sha256_text(normalized),
            )
        )
    return records, blockers


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal generated-output exclusion checker")
    parser.add_argument("--output-dir", default=str(FREEZE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / OUT_CSV.name
    out_md = output_dir / OUT_SUMMARY_MD.name
    out_json = output_dir / OUT_HASHES_JSON.name

    manifest_records, manifest_blockers = load_manifest_text_hashes()
    manifest_hash_to_items: dict[str, list[dict[str, str]]] = {}
    for record in manifest_records:
        manifest_hash_to_items.setdefault(record.normalized_hash, []).append(
            {"manifest_item_id": record.item_id, "path": record.path}
        )

    checked_rows: list[dict[str, str]] = []
    hash_payload: dict[str, object] = {
        "normalization_policy": {
            "strip_line_comments": True,
            "strip_block_comments": True,
            "lowercase_all_text": True,
            "collapse_whitespace": True,
            "remove_trailing_semicolon": True,
        },
        "manifest_blockers": manifest_blockers,
        "generated_output_rows": [],
        "generated_output_blockers": [],
    }

    for family, base_dir in GENERATED_FAMILIES.items():
        if not base_dir.exists():
            blocker = f"generated_source_missing:{family}:{base_dir}"
            hash_payload["generated_output_blockers"].append(blocker)
            checked_rows.append(
                {
                    "generated_output_family": family,
                    "generated_output_path": "",
                    "normalized_hash_available": "no",
                    "normalized_hash": "",
                    "corpus_text_available": "no",
                    "present_in_candidate_corpus": "blocked",
                    "matching_manifest_item_ids": "",
                    "attestation_status": "blocked_missing_generated_output_source",
                    "blocker_reason": blocker,
                }
            )
            continue

        for path in iter_sql_files(base_dir):
            checked = {
                "generated_output_family": family,
                "generated_output_path": str(path),
                "normalized_hash_available": "no",
                "normalized_hash": "",
                "corpus_text_available": "no",
                "present_in_candidate_corpus": "blocked",
                "matching_manifest_item_ids": "",
                "attestation_status": "blocked_generated_output_unreadable",
                "blocker_reason": "",
            }
            payload_row: dict[str, object] = {
                "generated_output_family": family,
                "generated_output_path": str(path),
            }

            text = safe_read_text(path)
            if text is None:
                checked["blocker_reason"] = f"generated_text_unavailable:{path}"
                checked_rows.append(checked)
                hash_payload["generated_output_rows"].append(payload_row)
                continue

            normalized = normalize_sql(text)
            if not normalized:
                checked["blocker_reason"] = f"generated_text_empty_after_normalization:{path}"
                checked_rows.append(checked)
                hash_payload["generated_output_rows"].append(payload_row)
                continue

            normalized_hash = sha256_text(normalized)
            checked["normalized_hash_available"] = "yes"
            checked["normalized_hash"] = normalized_hash
            payload_row["normalized_hash"] = normalized_hash

            matches = manifest_hash_to_items.get(normalized_hash, [])
            if matches:
                checked["matching_manifest_item_ids"] = ",".join(item["manifest_item_id"] for item in matches)

            if manifest_blockers or not manifest_records:
                checked["attestation_status"] = "blocked_corpus_text_unavailable"
                checked["present_in_candidate_corpus"] = "blocked"
                checked["blocker_reason"] = "; ".join(
                    manifest_blockers or ["no text-readable included corpus manifest entries available"]
                )
            else:
                checked["corpus_text_available"] = "yes"
                checked["present_in_candidate_corpus"] = "yes" if matches else "no"
                if matches:
                    checked["attestation_status"] = "failed_generated_output_present_in_corpus"
                    checked["blocker_reason"] = (
                        f"generated output normalized hash present in visible corpus manifest items {checked['matching_manifest_item_ids']}"
                    )
                else:
                    checked["attestation_status"] = "passed"
                    checked["blocker_reason"] = ""

            checked_rows.append(checked)
            hash_payload["generated_output_rows"].append(payload_row)

    fieldnames = [
        "generated_output_family",
        "generated_output_path",
        "normalized_hash_available",
        "normalized_hash",
        "corpus_text_available",
        "present_in_candidate_corpus",
        "matching_manifest_item_ids",
        "attestation_status",
        "blocker_reason",
    ]
    write_csv(out_csv, checked_rows, fieldnames)

    passed = sum(1 for row in checked_rows if row["attestation_status"] == "passed")
    failed = sum(1 for row in checked_rows if row["attestation_status"] == "failed_generated_output_present_in_corpus")
    blocked = len(checked_rows) - passed - failed
    out_md.write_text(
        "\n".join(
            [
                "# Formal Generated-Output Exclusion Summary",
                "",
                "## Status",
                "",
                f"- rows covered: `{len(checked_rows)}`",
                f"- rows passed: `{passed}`",
                f"- rows failed generated-output exclusion: `{failed}`",
                f"- rows blocked: `{blocked}`",
                "",
                "## Corpus Availability",
                "",
                f"- visible text-readable included manifest items: `{len(manifest_records)}`",
                f"- manifest blockers: `{len(manifest_blockers)}`",
                f"- generated-output family blockers: `{len(hash_payload['generated_output_blockers'])}`",
                "",
                "## Coverage Scope",
                "",
                "- generated-output families checked: `sqlglot`, `direct_llm`, `calcite`, `r_bot_pg1_recovery`",
                "- matching rule: `exact normalized hash match against visible included corpus text items`",
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
