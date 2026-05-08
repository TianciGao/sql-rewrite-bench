#!/usr/bin/env python3
"""
Human-run-only near-duplicate contamination checker for formal R-Bot gate closure.

This script does not call any LLM or API, does not run R-Bot, and does not
execute SQL. It reads denominator source SQL files, computes deterministic
normalized text features, and compares them against visible text-readable
included corpus manifest entries.
"""

from __future__ import annotations

import argparse
import csv
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
CORPUS_TEXT_MANIFEST_CSV = FREEZE_DIR / "formal_corpus_text_manifest_v1.csv"

OUT_CSV = FREEZE_DIR / "formal_near_duplicate_check_v1.csv"
OUT_SUMMARY_MD = FREEZE_DIR / "formal_near_duplicate_check_summary.md"

TOKEN_JACCARD_THRESHOLD = 0.90
TRIGRAM_JACCARD_THRESHOLD = 0.85
STRUCTURAL_SIMILARITY_THRESHOLD = 0.95
COMBINED_SIMILARITY_THRESHOLD = 0.90

KEYWORDS = (
    "select",
    "from",
    "where",
    "join",
    "group",
    "order",
    "having",
    "union",
    "exists",
    "in",
)


@dataclass
class FeatureRecord:
    item_id: str
    path: str
    normalized_text: str
    token_set: set[str]
    trigram_set: set[str]
    structural_features: dict[str, int]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_yes(value: str | None) -> bool:
    return (value or "").strip().lower() in {"yes", "true", "1"}


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


def tokenize_sql(sql: str) -> list[str]:
    return re.findall(r"[a-z_][a-z0-9_]*|\d+|!=|<=|>=|<>|[=<>(),.*+\-/]", sql)


def token_ngrams(tokens: list[str], n: int) -> set[str]:
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def build_structural_features(tokens: list[str], normalized_sql: str) -> dict[str, int]:
    features = {
        "token_count": len(tokens),
        "distinct_token_count": len(set(tokens)),
        "open_paren_count": normalized_sql.count("("),
        "close_paren_count": normalized_sql.count(")"),
    }
    for keyword in KEYWORDS:
        features[f"kw_{keyword}"] = tokens.count(keyword)
    return features


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def structural_similarity(left: dict[str, int], right: dict[str, int]) -> float:
    keys = sorted(set(left) | set(right))
    if not keys:
        return 1.0
    total = 0.0
    for key in keys:
        lv = left.get(key, 0)
        rv = right.get(key, 0)
        denom = max(lv, rv, 1)
        total += 1.0 - (abs(lv - rv) / denom)
    return total / len(keys)


def safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError:
        return None


def build_feature_record(item_id: str, path: str, text: str) -> FeatureRecord:
    normalized = normalize_sql(text)
    tokens = tokenize_sql(normalized)
    return FeatureRecord(
        item_id=item_id,
        path=path,
        normalized_text=normalized,
        token_set=set(tokens),
        trigram_set=token_ngrams(tokens, 3),
        structural_features=build_structural_features(tokens, normalized),
    )


def load_manifest_feature_records() -> tuple[list[FeatureRecord], list[str]]:
    rows = read_csv_rows(CORPUS_TEXT_MANIFEST_CSV)
    records: list[FeatureRecord] = []
    blockers: list[str] = []
    for row in rows:
        if not is_yes(row.get("included_for_contamination_check")):
            continue
        if row.get("path_status") == "missing":
            continue
        candidate = Path(row["path"])
        if not is_yes(row.get("text_readable")):
            blockers.append(f"binary_or_unavailable_text_corpus:{candidate}")
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
        records.append(build_feature_record(row["corpus_item_id"], str(candidate), text))
    return records, blockers


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal near-duplicate checker")
    parser.add_argument("--output-dir", default=str(FREEZE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / OUT_CSV.name
    out_md = output_dir / OUT_SUMMARY_MD.name

    denominator_rows = [r for r in read_csv_rows(DENOMINATOR_CSV) if r["included_in_common_core_v0"] == "yes"]
    manifest_records, manifest_blockers = load_manifest_feature_records()

    checked_rows: list[dict[str, str]] = []

    for row in denominator_rows:
        case_id = row["case_id"]
        pool = row["pool"]
        source_sql = ROOT / "cases" / case_id.split("_")[0] / case_id / "source.sql"
        checked = {
            "case_id": case_id,
            "pool": pool,
            "source_sql_path": str(source_sql),
            "corpus_text_available": "no",
            "near_duplicate_checked": "no",
            "near_duplicate_found": "blocked",
            "closest_manifest_item_id": "",
            "closest_manifest_path": "",
            "token_set_jaccard": "",
            "token_trigram_jaccard": "",
            "structural_similarity": "",
            "combined_similarity": "",
            "attestation_status": "blocked_missing_source_sql",
            "blocker_reason": "",
        }

        if not source_sql.exists():
            checked["blocker_reason"] = f"missing source SQL: {source_sql}"
            checked_rows.append(checked)
            continue

        source_text = safe_read_text(source_sql)
        if source_text is None:
            checked["blocker_reason"] = f"unreadable source SQL: {source_sql}"
            checked_rows.append(checked)
            continue

        source_record = build_feature_record(case_id, str(source_sql), source_text)

        best_match: FeatureRecord | None = None
        best_scores = {
            "token_set_jaccard": 0.0,
            "token_trigram_jaccard": 0.0,
            "structural_similarity": 0.0,
            "combined_similarity": 0.0,
        }
        for manifest_record in manifest_records:
            token_score = jaccard_similarity(source_record.token_set, manifest_record.token_set)
            trigram_score = jaccard_similarity(source_record.trigram_set, manifest_record.trigram_set)
            structural_score = structural_similarity(
                source_record.structural_features, manifest_record.structural_features
            )
            combined_score = (token_score + trigram_score + structural_score) / 3.0
            if combined_score > best_scores["combined_similarity"]:
                best_match = manifest_record
                best_scores = {
                    "token_set_jaccard": token_score,
                    "token_trigram_jaccard": trigram_score,
                    "structural_similarity": structural_score,
                    "combined_similarity": combined_score,
                }

        if best_match is not None:
            checked["closest_manifest_item_id"] = best_match.item_id
            checked["closest_manifest_path"] = best_match.path
            checked["token_set_jaccard"] = f"{best_scores['token_set_jaccard']:.6f}"
            checked["token_trigram_jaccard"] = f"{best_scores['token_trigram_jaccard']:.6f}"
            checked["structural_similarity"] = f"{best_scores['structural_similarity']:.6f}"
            checked["combined_similarity"] = f"{best_scores['combined_similarity']:.6f}"

        if manifest_blockers or not manifest_records:
            checked["attestation_status"] = "blocked_corpus_text_unavailable"
            checked["near_duplicate_found"] = "blocked"
            checked["blocker_reason"] = "; ".join(
                manifest_blockers or ["no text-readable included corpus manifest entries available"]
            )
            checked_rows.append(checked)
            continue

        checked["corpus_text_available"] = "yes"
        checked["near_duplicate_checked"] = "yes"
        is_near_duplicate = (
            best_scores["token_set_jaccard"] >= TOKEN_JACCARD_THRESHOLD
            and best_scores["token_trigram_jaccard"] >= TRIGRAM_JACCARD_THRESHOLD
            and best_scores["structural_similarity"] >= STRUCTURAL_SIMILARITY_THRESHOLD
            and best_scores["combined_similarity"] >= COMBINED_SIMILARITY_THRESHOLD
        )
        checked["near_duplicate_found"] = "yes" if is_near_duplicate else "no"
        if is_near_duplicate:
            checked["attestation_status"] = "failed_near_duplicate_detected"
            checked["blocker_reason"] = (
                f"visible near-duplicate candidate found in manifest item {checked['closest_manifest_item_id']}"
            )
        else:
            checked["attestation_status"] = "passed"
            checked["blocker_reason"] = ""

        checked_rows.append(checked)

    fieldnames = [
        "case_id",
        "pool",
        "source_sql_path",
        "corpus_text_available",
        "near_duplicate_checked",
        "near_duplicate_found",
        "closest_manifest_item_id",
        "closest_manifest_path",
        "token_set_jaccard",
        "token_trigram_jaccard",
        "structural_similarity",
        "combined_similarity",
        "attestation_status",
        "blocker_reason",
    ]
    write_csv(out_csv, checked_rows, fieldnames)

    passed = sum(1 for row in checked_rows if row["attestation_status"] == "passed")
    failed = sum(1 for row in checked_rows if row["attestation_status"] == "failed_near_duplicate_detected")
    blocked = len(checked_rows) - passed - failed
    out_md.write_text(
        "\n".join(
            [
                "# Formal Near-Duplicate Check Summary",
                "",
                "## Status",
                "",
                f"- rows covered: `{len(checked_rows)}`",
                f"- rows passed: `{passed}`",
                f"- rows failed near-duplicate detection: `{failed}`",
                f"- rows blocked: `{blocked}`",
                "",
                "## Heuristic Features",
                "",
                "- token-set similarity: `jaccard`",
                "- token-3-gram similarity: `jaccard`",
                "- structural similarity: `keyword-count and shape overlap`",
                f"- token-set trigger threshold: `{TOKEN_JACCARD_THRESHOLD}`",
                f"- token-3-gram trigger threshold: `{TRIGRAM_JACCARD_THRESHOLD}`",
                f"- structural trigger threshold: `{STRUCTURAL_SIMILARITY_THRESHOLD}`",
                f"- combined trigger threshold: `{COMBINED_SIMILARITY_THRESHOLD}`",
                "",
                "## Corpus Availability",
                "",
                f"- visible text-readable included manifest items: `{len(manifest_records)}`",
                f"- manifest blockers: `{len(manifest_blockers)}`",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
