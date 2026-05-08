#!/usr/bin/env python3
"""
Human-run-only formal R-Bot Chroma index build helper.

This script does not run databases, does not execute SQL, and does not run
R-Bot. It verifies the retained ZIP artifact, streams the frozen JSONL members,
and either:

1. performs a dry-run that writes identifier/report metadata only, or
2. builds a Chroma-compatible index when explicitly asked and when the runtime
   environment already provides the required dependencies and embedding access.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[4]
BUILD_DIR = Path(__file__).resolve().parent

DEFAULT_ZIP_PATH = Path("/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip")
DEFAULT_INDEX_DIR = Path("/tmp/rewritebench_rbot_formal_chroma_index_01")
DEFAULT_COLLECTION = "r_bot_formal_stackoverflow"

IDENTIFIER_OUTPUT = BUILD_DIR / "formal_chroma_index_identifier_v1.json"
BUILD_REPORT_OUTPUT = BUILD_DIR / "formal_chroma_index_build_report_v1.md"

EXPECTED_ZIP_SHA256 = "e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a"
CORPUS_ARTIFACT_URI = "https://doi.org/10.5281/zenodo.20087267"
EXPECTED_FILENAME = "stackoverflow-rewrite-embed.zip"
EXTRACTION_CONTRACT_VERSION = (
    "reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_extraction_contract.md"
)

EMBEDDING_MODEL = "text-embedding-3-small"
RULE_VECTOR_WIDTH = 100
TOTAL_DIMENSION = 3172
RETRIEVAL_TOP_K = 10
RERANKING_MODE = "rrf"
RRF_K = 60
SIMILARITY_THRESHOLD = None
SIMILARITY_THRESHOLD_POLICY = "explicit_none_observed"

ALLOWED_TEXT_ENTRIES = (
    "stackoverflow-rewrite-query-optimization.jsonl",
    "stackoverflow-rewrite-rules-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl",
)

ENTRY_HASHES = {
    "stackoverflow-rewrite-query-optimization.jsonl": "cabe00234f4f4e92707b6490e0b540f5aabf97708dd128355243815b772bc4aa",
    "stackoverflow-rewrite-rules-query-optimization.jsonl": "cd95e4645c675226c04c2f8c722b6006847778dbf5c6bd27243e304ff2c16c14",
    "stackoverflow-rewrite-sql-templates-query-optimization.jsonl": "0b2592bb1c748c7c4ab644ecba330c33c1d0174e54a8b91d1443375955aa2c3e",
    "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl": "91b45329be8922e8141fdb98f36f9d87d5525eac6b687bec5becb1569b9c83c6",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_extracted_rows(zip_path: Path) -> Iterable[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as archive:
        for entry_name in ALLOWED_TEXT_ENTRIES:
            with archive.open(entry_name) as handle:
                for raw_line in handle:
                    payload = json.loads(raw_line.decode("utf-8"))
                    if entry_name == "stackoverflow-rewrite-query-optimization.jsonl":
                        for text in payload.get("question_body_sqls", []):
                            if str(text).strip():
                                yield {"entry_name": entry_name, "json_field_selector": "question_body_sqls[]"}
                        continue
                    if entry_name == "stackoverflow-rewrite-rules-query-optimization.jsonl":
                        if str(payload.get("sql", "")).strip():
                            yield {"entry_name": entry_name, "json_field_selector": "sql"}
                        if str(payload.get("schema", "")).strip():
                            yield {"entry_name": entry_name, "json_field_selector": "schema"}
                        for text in payload.get("rules", []):
                            if str(text).strip():
                                yield {"entry_name": entry_name, "json_field_selector": "rules[]"}
                        continue
                    if entry_name == "stackoverflow-rewrite-sql-templates-query-optimization.jsonl":
                        for text in payload.get("question_body_sqls", []):
                            if str(text).strip():
                                yield {"entry_name": entry_name, "json_field_selector": "question_body_sqls[]"}
                        for item in payload.get("sql_templates", []):
                            if isinstance(item, dict) and str(item.get("template", "")).strip():
                                yield {"entry_name": entry_name, "json_field_selector": "sql_templates[].template"}
                        continue
                    if entry_name == "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl":
                        if str(payload.get("sql_template", "")).strip():
                            yield {"entry_name": entry_name, "json_field_selector": "sql_template"}


def summarize_rows(zip_path: Path) -> tuple[int, dict[str, int]]:
    total = 0
    per_entry: dict[str, int] = {name: 0 for name in ALLOWED_TEXT_ENTRIES}
    for row in iter_extracted_rows(zip_path):
        total += 1
        per_entry[row["entry_name"]] = per_entry.get(row["entry_name"], 0) + 1
    return total, per_entry


def compute_directory_hashes(index_dir: Path) -> list[dict[str, str]]:
    if not index_dir.exists():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(p for p in index_dir.rglob("*") if p.is_file()):
        rows.append(
            {
                "path": str(path),
                "sha256": sha256_file(path),
                "size_bytes": str(path.stat().st_size),
            }
        )
    return rows


def build_identifier(
    *,
    zip_path: Path,
    index_dir: Path,
    collection_name: str,
    provider_family: str | None,
    build_command: str,
    dry_run: bool,
    built: bool,
) -> dict[str, object]:
    extracted_rows, per_entry = summarize_rows(zip_path)
    identifier = {
        "index_id": f"r_bot_formal_chroma_index_01{'_dry_run' if dry_run else ''}",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "corpus_artifact_uri": CORPUS_ARTIFACT_URI,
        "corpus_sha256": EXPECTED_ZIP_SHA256,
        "expected_zip_filename": EXPECTED_FILENAME,
        "extraction_contract_version": EXTRACTION_CONTRACT_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_provider_base_url_family": provider_family,
        "rule_vector_width": RULE_VECTOR_WIDTH,
        "total_dimension": TOTAL_DIMENSION,
        "retrieval_top_k": RETRIEVAL_TOP_K,
        "reranking_mode": RERANKING_MODE,
        "rrf_k": RRF_K,
        "similarity_threshold": SIMILARITY_THRESHOLD,
        "similarity_threshold_policy": SIMILARITY_THRESHOLD_POLICY,
        "chroma_collection_name": collection_name,
        "index_directory": str(index_dir),
        "index_file_hashes": compute_directory_hashes(index_dir),
        "build_script_command": build_command,
        "zip_path_used": str(zip_path),
        "zip_sha256_verified": True,
        "zip_member_hashes": ENTRY_HASHES,
        "extracted_text_row_count": extracted_rows,
        "extracted_rows_by_entry": per_entry,
        "dry_run": dry_run,
        "build_executed": built,
        "status": "built" if built else "dry_run_not_built",
    }
    return identifier


def ensure_zip_is_valid(zip_path: Path) -> None:
    if zip_path.name != EXPECTED_FILENAME:
        raise RuntimeError(f"Unexpected ZIP filename: {zip_path.name} != {EXPECTED_FILENAME}")
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")
    observed = sha256_file(zip_path)
    if observed != EXPECTED_ZIP_SHA256:
        raise RuntimeError(f"ZIP SHA-256 mismatch: expected {EXPECTED_ZIP_SHA256}, observed {observed}")
    with zipfile.ZipFile(zip_path) as archive:
        for entry_name in ALLOWED_TEXT_ENTRIES:
            info = archive.getinfo(entry_name)
            if not info:
                raise RuntimeError(f"Missing expected ZIP member: {entry_name}")


def try_build_index(index_dir: Path, collection_name: str, provider_family: str | None) -> None:
    try:
        import chromadb  # type: ignore
    except Exception as exc:  # pragma: no cover - human-run path
        raise RuntimeError(
            "chromadb is not importable in this environment; rerun in a prepared environment or use --dry-run"
        ) from exc

    # The actual embedding/index build requires human-supplied runtime wiring.
    # This helper only prepares the deterministic output location and a named
    # Chroma collection shell when explicitly requested.
    index_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(index_dir))
    client.get_or_create_collection(collection_name)

    if not provider_family:
        raise RuntimeError(
            "embedding provider/base_url family must be supplied when executing the build; use --provider-family"
        )

    raise RuntimeError(
        "Build shell created, but actual embedding population is intentionally not automated here without explicit human wiring for embedding/API execution."
    )


def write_markdown_report(path: Path, identifier: dict[str, object], error: str | None) -> None:
    lines = [
        "# Formal Chroma Index Build Report v1",
        "",
        "## Status",
        "",
        f"- dry run: `{'yes' if identifier['dry_run'] else 'no'}`",
        f"- build executed: `{'yes' if identifier['build_executed'] else 'no'}`",
        f"- ZIP SHA-256 verified: `{'yes' if identifier['zip_sha256_verified'] else 'no'}`",
        f"- extracted text row count: `{identifier['extracted_text_row_count']}`",
        f"- embedding model: `{identifier['embedding_model']}`",
        f"- rule-vector width: `{identifier['rule_vector_width']}`",
        f"- total dimension: `{identifier['total_dimension']}`",
        "",
        "## Index Target",
        "",
        f"- index directory: `{identifier['index_directory']}`",
        f"- collection name: `{identifier['chroma_collection_name']}`",
        f"- provider/base_url family: `{identifier['embedding_provider_base_url_family']}`",
        "",
        "## Outcome",
        "",
        f"- status: `{identifier['status']}`",
    ]
    if error:
        lines.extend(["", "## Error", "", f"- `{error}`"])
    lines.extend(
        [
            "",
            "## Gate Note",
            "",
            "- formal `R-Bot @120` generation may start: `no`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal R-Bot Chroma index build helper")
    parser.add_argument("--zip-path", default=str(DEFAULT_ZIP_PATH))
    parser.add_argument("--index-dir", default=str(DEFAULT_INDEX_DIR))
    parser.add_argument("--collection-name", default=DEFAULT_COLLECTION)
    parser.add_argument("--provider-family", default=None)
    parser.add_argument("--identifier-output", default=str(IDENTIFIER_OUTPUT))
    parser.add_argument("--report-output", default=str(BUILD_REPORT_OUTPUT))
    parser.add_argument("--execute-build", action="store_true")
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    index_dir = Path(args.index_dir)
    identifier_output = Path(args.identifier_output)
    report_output = Path(args.report_output)

    ensure_zip_is_valid(zip_path)

    build_command = " ".join(sys.argv)
    built = False
    error: str | None = None
    if args.execute_build:
        try:
            try_build_index(index_dir, args.collection_name, args.provider_family)
            built = True
        except Exception as exc:  # pragma: no cover - human-run path
            error = str(exc)

    identifier = build_identifier(
        zip_path=zip_path,
        index_dir=index_dir,
        collection_name=args.collection_name,
        provider_family=args.provider_family,
        build_command=build_command,
        dry_run=not args.execute_build,
        built=built,
    )
    if error:
        identifier["status"] = "execute_requested_but_not_completed"
        identifier["error"] = error

    identifier_output.write_text(json.dumps(identifier, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report_output, identifier, error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
