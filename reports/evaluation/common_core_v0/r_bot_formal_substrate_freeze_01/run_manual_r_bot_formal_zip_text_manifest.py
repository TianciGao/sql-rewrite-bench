#!/usr/bin/env python3
"""
Human-run-only streamed ZIP text manifest materializer for formal R-Bot gate work.

This script does not call any LLM or API, does not run R-Bot, and does not
execute SQL. It streams four known JSONL members directly from the ZIP archive,
extracts only contamination-relevant text fields, and writes checker-consumable
manifest artifacts without unpacking large archive contents into the repo.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
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

ZIP_PATH = Path("/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip")
EXPECTED_ZIP_SHA256 = "e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a"

ZIP_ENTRY_SHA256 = {
    "stackoverflow-rewrite-query-optimization.jsonl": "cabe00234f4f4e92707b6490e0b540f5aabf97708dd128355243815b772bc4aa",
    "stackoverflow-rewrite-rules-query-optimization.jsonl": "cd95e4645c675226c04c2f8c722b6006847778dbf5c6bd27243e304ff2c16c14",
    "stackoverflow-rewrite-sql-templates-query-optimization.jsonl": "0b2592bb1c748c7c4ab644ecba330c33c1d0174e54a8b91d1443375955aa2c3e",
    "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl": "91b45329be8922e8141fdb98f36f9d87d5525eac6b687bec5becb1569b9c83c6",
}

ALLOWED_TEXT_ENTRIES = (
    "stackoverflow-rewrite-query-optimization.jsonl",
    "stackoverflow-rewrite-rules-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl",
)

OUT_MANIFEST_CSV = FREEZE_DIR / "formal_zip_text_manifest_v1.csv"
OUT_HASHES_JSON = FREEZE_DIR / "formal_zip_text_hashes_v1.json"
OUT_SUMMARY_MD = FREEZE_DIR / "formal_zip_text_manifest_summary.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_text(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"--[^\n\r]*", " ", text)
    text = text.strip()
    text = re.sub(r";+\s*$", "", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def maybe_add_row(
    rows: list[dict[str, str]],
    counts: dict[str, int],
    *,
    zip_sha256: str,
    entry_name: str,
    record_index: int,
    field_selector: str,
    source_record_locator: str,
    text_value: str | None,
) -> None:
    if text_value is None:
        return
    text = str(text_value).strip()
    if not text:
        return
    normalized = normalize_text(text)
    if not normalized:
        return
    counts[entry_name] = counts.get(entry_name, 0) + 1
    item_number = counts[entry_name]
    row_id = f"{entry_name}|{field_selector}|{record_index}|{item_number}"
    rows.append(
        {
            "zip_text_item_id": sha256_text(row_id),
            "source_family": "retrieval_archive_member_text",
            "zip_path": str(ZIP_PATH),
            "zip_sha256": zip_sha256,
            "zip_entry_name": entry_name,
            "entry_sha256": ZIP_ENTRY_SHA256.get(entry_name, ""),
            "source_record_locator": source_record_locator,
            "json_field_selector": field_selector,
            "path_status": "tmp_only",
            "text_readable": "yes",
            "included_for_formal_retrieval": "yes",
            "included_for_contamination_check": "yes",
            "formal_retention_blocker": "true",
            "retention_blocker_reason": "tmp_only_archive_text_without_retained_external_provenance",
            "text_length": str(len(text)),
            "normalized_hash": sha256_text(normalized),
            "extracted_text": text,
        }
    )


def iter_extracted_rows(zip_sha256: str) -> tuple[list[dict[str, str]], dict[str, int]]:
    rows: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for entry_name in ALLOWED_TEXT_ENTRIES:
            with archive.open(entry_name) as handle:
                for record_index, raw_line in enumerate(handle, start=1):
                    payload = json.loads(raw_line.decode("utf-8"))
                    source_record_locator = (
                        f"id={payload.get('id','')};answer_id={payload.get('answer_id','')};index={payload.get('index','')}"
                    ).strip(";")

                    if entry_name == "stackoverflow-rewrite-query-optimization.jsonl":
                        for item in payload.get("question_body_sqls", []):
                            maybe_add_row(
                                rows,
                                counts,
                                zip_sha256=zip_sha256,
                                entry_name=entry_name,
                                record_index=record_index,
                                field_selector="question_body_sqls[]",
                                source_record_locator=source_record_locator,
                                text_value=item,
                            )
                        continue

                    if entry_name == "stackoverflow-rewrite-rules-query-optimization.jsonl":
                        maybe_add_row(
                            rows,
                            counts,
                            zip_sha256=zip_sha256,
                            entry_name=entry_name,
                            record_index=record_index,
                            field_selector="sql",
                            source_record_locator=source_record_locator,
                            text_value=payload.get("sql"),
                        )
                        maybe_add_row(
                            rows,
                            counts,
                            zip_sha256=zip_sha256,
                            entry_name=entry_name,
                            record_index=record_index,
                            field_selector="schema",
                            source_record_locator=source_record_locator,
                            text_value=payload.get("schema"),
                        )
                        for item in payload.get("rules", []):
                            maybe_add_row(
                                rows,
                                counts,
                                zip_sha256=zip_sha256,
                                entry_name=entry_name,
                                record_index=record_index,
                                field_selector="rules[]",
                                source_record_locator=source_record_locator,
                                text_value=item,
                            )
                        continue

                    if entry_name == "stackoverflow-rewrite-sql-templates-query-optimization.jsonl":
                        for item in payload.get("question_body_sqls", []):
                            maybe_add_row(
                                rows,
                                counts,
                                zip_sha256=zip_sha256,
                                entry_name=entry_name,
                                record_index=record_index,
                                field_selector="question_body_sqls[]",
                                source_record_locator=source_record_locator,
                                text_value=item,
                            )
                        for item in payload.get("sql_templates", []):
                            maybe_add_row(
                                rows,
                                counts,
                                zip_sha256=zip_sha256,
                                entry_name=entry_name,
                                record_index=record_index,
                                field_selector="sql_templates[].template",
                                source_record_locator=source_record_locator,
                                text_value=item.get("template") if isinstance(item, dict) else None,
                            )
                        continue

                    if entry_name == "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl":
                        maybe_add_row(
                            rows,
                            counts,
                            zip_sha256=zip_sha256,
                            entry_name=entry_name,
                            record_index=record_index,
                            field_selector="sql_template",
                            source_record_locator=source_record_locator or f"line={record_index}",
                            text_value=payload.get("sql_template"),
                        )
    return rows, counts


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only streamed ZIP text manifest materializer")
    parser.add_argument("--output-dir", default=str(FREEZE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_manifest = output_dir / OUT_MANIFEST_CSV.name
    out_hashes = output_dir / OUT_HASHES_JSON.name
    out_summary = output_dir / OUT_SUMMARY_MD.name

    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"ZIP archive not found: {ZIP_PATH}")

    zip_sha256 = sha256_file(ZIP_PATH)
    if zip_sha256 != EXPECTED_ZIP_SHA256:
        raise RuntimeError(
            f"ZIP SHA-256 mismatch for {ZIP_PATH}: expected {EXPECTED_ZIP_SHA256}, observed {zip_sha256}"
        )

    rows, counts = iter_extracted_rows(zip_sha256)

    fieldnames = [
        "zip_text_item_id",
        "source_family",
        "zip_path",
        "zip_sha256",
        "zip_entry_name",
        "entry_sha256",
        "source_record_locator",
        "json_field_selector",
        "path_status",
        "text_readable",
        "included_for_formal_retrieval",
        "included_for_contamination_check",
        "formal_retention_blocker",
        "retention_blocker_reason",
        "text_length",
        "normalized_hash",
        "extracted_text",
    ]
    write_csv(out_manifest, rows, fieldnames)

    hash_payload = {
        "zip_path": str(ZIP_PATH),
        "zip_sha256": zip_sha256,
        "expected_zip_sha256": EXPECTED_ZIP_SHA256,
        "streamed_entries": list(ALLOWED_TEXT_ENTRIES),
        "row_count": len(rows),
        "row_counts_by_entry": counts,
        "normalization_policy": {
            "strip_line_comments": True,
            "strip_block_comments": True,
            "lowercase_all_text": True,
            "collapse_whitespace": True,
            "remove_trailing_semicolon": True,
        },
        "formal_retention_blocker": True,
        "retention_blocker_reason": "tmp_only_archive_text_without_retained_external_provenance",
    }
    out_hashes.write_text(json.dumps(hash_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    out_summary.write_text(
        "\n".join(
            [
                "# Formal ZIP Text Manifest Summary",
                "",
                "## Status",
                "",
                f"- ZIP path: `{ZIP_PATH}`",
                f"- ZIP SHA-256 verified: `yes`",
                f"- extracted text rows: `{len(rows)}`",
                f"- formal retention blocker: `true`",
                "",
                "## Streamed Members",
                "",
                *[f"- `{entry}`: `{counts.get(entry, 0)}` extracted rows" for entry in ALLOWED_TEXT_ENTRIES],
                "",
                "## Extracted Fields",
                "",
                "- `sql`",
                "- `schema`",
                "- `rules[]`",
                "- `question_body_sqls[]`",
                "- `sql_templates[].template`",
                "- `sql_template`",
                "",
                "## Notes",
                "",
                "- `__MACOSX` sidecars are ignored",
                "- embedding vectors are ignored",
                "- the ZIP remains `/tmp`-only and still needs retained external provenance closure",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
