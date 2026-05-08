#!/usr/bin/env python3
"""
Human-run-only formal R-Bot Chroma index build helper.

This script does not run databases, does not execute SQL, and does not run
R-Bot. It verifies the retained ZIP artifact, reuses the frozen extracted-text
manifest package, and either:

1. performs a dry-run that writes identifier/report metadata only, or
2. fails closed for execute-build until real embedding/index population is
   explicitly implemented as a formal path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
BUILD_DIR = Path(__file__).resolve().parent

DEFAULT_ZIP_PATH = Path("/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/stackoverflow-rewrite-embed.zip")
DEFAULT_INDEX_DIR = Path("/tmp/rewritebench_rbot_formal_chroma_index_01")
DEFAULT_COLLECTION = "r_bot_formal_stackoverflow"

IDENTIFIER_OUTPUT = BUILD_DIR / "formal_chroma_index_identifier_v1.json"
BUILD_REPORT_OUTPUT = BUILD_DIR / "formal_chroma_index_build_report_v1.md"
MANIFEST_CSV = (
    ROOT
    / "reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_manifest_v1.csv"
)
MANIFEST_HASHES_JSON = (
    ROOT
    / "reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_zip_text_hashes_v1.json"
)
ZIP_RETENTION_MANIFEST_JSON = (
    ROOT
    / "reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.json"
)
ZIP_RETENTION_MANIFEST_CSV = (
    ROOT
    / "reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_stackoverflow_zip_retention_manifest_v2.csv"
)

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


class FormalIndexBuildError(RuntimeError):
    """Base error for formal index build helper failures."""


class MissingProviderFamilyError(FormalIndexBuildError):
    """Raised when formal metadata is missing an explicit provider family."""


class ExecuteBuildNotImplementedError(FormalIndexBuildError):
    """Raised when execute-build is requested before a real build path exists."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def load_frozen_manifest_metadata() -> dict[str, Any]:
    if not MANIFEST_HASHES_JSON.exists():
        raise FileNotFoundError(f"Frozen manifest hashes JSON not found: {MANIFEST_HASHES_JSON}")
    if not MANIFEST_CSV.exists():
        raise FileNotFoundError(f"Frozen manifest CSV not found: {MANIFEST_CSV}")

    hash_payload = json.loads(MANIFEST_HASHES_JSON.read_text(encoding="utf-8"))
    row_count_from_csv = 0
    row_counts_by_entry_from_csv: dict[str, int] = {name: 0 for name in ALLOWED_TEXT_ENTRIES}

    with MANIFEST_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row_count_from_csv += 1
            entry_name = row.get("zip_entry_name", "")
            row_counts_by_entry_from_csv[entry_name] = row_counts_by_entry_from_csv.get(entry_name, 0) + 1

    manifest_row_count = int(hash_payload["row_count"])
    manifest_row_counts_by_entry = {
        name: int(hash_payload["row_counts_by_entry"].get(name, 0)) for name in ALLOWED_TEXT_ENTRIES
    }

    if row_count_from_csv != manifest_row_count:
        raise RuntimeError(
            f"Frozen manifest row-count mismatch: CSV={row_count_from_csv}, hashes_json={manifest_row_count}"
        )
    if row_counts_by_entry_from_csv != manifest_row_counts_by_entry:
        raise RuntimeError("Frozen manifest per-entry row-count mismatch between CSV and hashes JSON")

    return {
        "manifest_csv_path": str(MANIFEST_CSV),
        "manifest_hashes_json_path": str(MANIFEST_HASHES_JSON),
        "extracted_text_row_count": manifest_row_count,
        "extracted_rows_by_entry": manifest_row_counts_by_entry,
        "normalization_policy": hash_payload.get("normalization_policy", {}),
        "manifest_retention_blocker": hash_payload.get("formal_retention_blocker"),
        "manifest_retention_blocker_reason": hash_payload.get("retention_blocker_reason"),
    }


def load_zip_retention_metadata() -> dict[str, Any]:
    if not ZIP_RETENTION_MANIFEST_JSON.exists():
        raise FileNotFoundError(f"ZIP retention manifest JSON not found: {ZIP_RETENTION_MANIFEST_JSON}")
    if not ZIP_RETENTION_MANIFEST_CSV.exists():
        raise FileNotFoundError(f"ZIP retention manifest CSV not found: {ZIP_RETENTION_MANIFEST_CSV}")

    retention_payload = json.loads(ZIP_RETENTION_MANIFEST_JSON.read_text(encoding="utf-8"))
    csv_rows: list[dict[str, str]] = []
    with ZIP_RETENTION_MANIFEST_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        csv_rows = list(reader)

    if not csv_rows:
        raise RuntimeError("ZIP retention manifest CSV is empty")

    outer_rows = [row for row in csv_rows if row.get("artifact_scope") == "outer_zip"]
    if len(outer_rows) != 1:
        raise RuntimeError(f"Expected exactly one outer_zip row in ZIP retention manifest CSV, found {len(outer_rows)}")
    outer_row = outer_rows[0]

    expected_uri = CORPUS_ARTIFACT_URI
    expected_filename = EXPECTED_FILENAME
    expected_sha = EXPECTED_ZIP_SHA256
    json_closed = bool(retention_payload.get("zip_external_provenance_closed"))
    status = str(retention_payload.get("retention_status", ""))
    uri = str(retention_payload.get("external_artifact_uri", ""))
    filename = str(retention_payload.get("expected_filename", ""))
    outer_sha = str(retention_payload.get("outer_zip_sha256", ""))

    if uri != expected_uri:
        raise RuntimeError(f"ZIP retention manifest URI mismatch: expected {expected_uri}, observed {uri}")
    if filename != expected_filename:
        raise RuntimeError(f"ZIP retention manifest filename mismatch: expected {expected_filename}, observed {filename}")
    if outer_sha != expected_sha:
        raise RuntimeError(f"ZIP retention manifest SHA-256 mismatch: expected {expected_sha}, observed {outer_sha}")
    if status != "externally_retained_with_checksum":
        raise RuntimeError(
            "ZIP retention manifest status mismatch: expected externally_retained_with_checksum, "
            f"observed {status}"
        )
    if not json_closed:
        raise RuntimeError("ZIP retention manifest does not mark external provenance as closed")

    csv_uri = outer_row.get("external_artifact_uri", "")
    csv_filename = outer_row.get("expected_filename", "")
    csv_sha = outer_row.get("outer_zip_sha256", "")
    csv_status = outer_row.get("retention_status", "")
    csv_closed = outer_row.get("zip_external_provenance_closed", "").strip().lower()
    if csv_uri != expected_uri:
        raise RuntimeError(f"ZIP retention manifest CSV URI mismatch: expected {expected_uri}, observed {csv_uri}")
    if csv_filename != expected_filename:
        raise RuntimeError(
            f"ZIP retention manifest CSV filename mismatch: expected {expected_filename}, observed {csv_filename}"
        )
    if csv_sha != expected_sha:
        raise RuntimeError(f"ZIP retention manifest CSV SHA-256 mismatch: expected {expected_sha}, observed {csv_sha}")
    if csv_status != "externally_retained_with_checksum":
        raise RuntimeError(
            "ZIP retention manifest CSV status mismatch: expected externally_retained_with_checksum, "
            f"observed {csv_status}"
        )
    if csv_closed != "yes":
        raise RuntimeError("ZIP retention manifest CSV does not mark external provenance as closed")

    return {
        "zip_external_artifact_uri": uri,
        "zip_retention_status": status,
        "zip_provenance_closed": True,
        "zip_retention_manifest_path": str(ZIP_RETENTION_MANIFEST_JSON),
        "zip_retention_manifest_csv_path": str(ZIP_RETENTION_MANIFEST_CSV),
        "zip_retention_scope": retention_payload.get("scope"),
        "zip_retention_notes": retention_payload.get("notes", []),
    }


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


def resolve_provider_family(provider_family: str | None, *, formal_required: bool) -> tuple[str | None, str]:
    normalized = provider_family.strip() if provider_family and provider_family.strip() else None
    if normalized:
        return normalized, "provider_family_recorded"
    if formal_required:
        raise MissingProviderFamilyError(
            "embedding provider/base_url family must be supplied for formal index metadata; use --provider-family"
        )
    return None, "missing_provider_family"


def try_build_index(index_dir: Path, collection_name: str, provider_family: str) -> None:
    _ = (index_dir, collection_name, provider_family)
    raise ExecuteBuildNotImplementedError(
        "Real embedding/index population is not implemented in this helper; execute-build remains disabled."
    )


def determine_status(*, dry_run: bool, provider_status: str, error: str | None) -> str:
    if error:
        if provider_status == "missing_provider_family":
            return "missing_provider_family"
        if "Real embedding/index population is not implemented" in error:
            return "execute_build_not_implemented_real_index"
        return "execute_build_failed"
    if dry_run:
        return provider_status
    return "built"


def build_identifier(
    *,
    zip_path: Path,
    index_dir: Path,
    collection_name: str,
    provider_family: str | None,
    provider_status: str,
    build_command: str,
    dry_run: bool,
    status: str,
    error: str | None,
) -> dict[str, object]:
    manifest_metadata = load_frozen_manifest_metadata()
    zip_retention_metadata = load_zip_retention_metadata()
    index_id: str | None = None
    if dry_run:
        index_id = "r_bot_formal_chroma_index_01_dry_run_preview"
    elif status == "built":
        index_id = "r_bot_formal_chroma_index_01"

    identifier = {
        "index_id": index_id,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "corpus_artifact_uri": CORPUS_ARTIFACT_URI,
        "corpus_sha256": EXPECTED_ZIP_SHA256,
        "expected_zip_filename": EXPECTED_FILENAME,
        "extraction_contract_version": EXTRACTION_CONTRACT_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_provider_base_url_family": provider_family,
        "embedding_provider_status": provider_status,
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
        "zip_external_artifact_uri": zip_retention_metadata["zip_external_artifact_uri"],
        "zip_retention_status": zip_retention_metadata["zip_retention_status"],
        "zip_provenance_closed": zip_retention_metadata["zip_provenance_closed"],
        "zip_retention_manifest_path": zip_retention_metadata["zip_retention_manifest_path"],
        "zip_retention_manifest_csv_path": zip_retention_metadata["zip_retention_manifest_csv_path"],
        "manifest_csv_path": manifest_metadata["manifest_csv_path"],
        "manifest_hashes_json_path": manifest_metadata["manifest_hashes_json_path"],
        "extracted_text_row_count": manifest_metadata["extracted_text_row_count"],
        "extracted_rows_by_entry": manifest_metadata["extracted_rows_by_entry"],
        "manifest_normalization_policy": manifest_metadata["normalization_policy"],
        "manifest_retention_blocker": not zip_retention_metadata["zip_provenance_closed"],
        "manifest_retention_blocker_reason": None,
        "dry_run": dry_run,
        "build_executed": status == "built",
        "status": status,
    }
    if error:
        identifier["error"] = error
    return identifier


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
        f"- provider status: `{identifier['embedding_provider_status']}`",
        f"- rule-vector width: `{identifier['rule_vector_width']}`",
        f"- total dimension: `{identifier['total_dimension']}`",
        "",
        "## Frozen Manifest",
        "",
        f"- manifest CSV: `{identifier['manifest_csv_path']}`",
        f"- manifest hashes JSON: `{identifier['manifest_hashes_json_path']}`",
        f"- manifest retention blocker: `{identifier['manifest_retention_blocker']}`",
        f"- zip external artifact URI: `{identifier['zip_external_artifact_uri']}`",
        f"- zip retention status: `{identifier['zip_retention_status']}`",
        f"- zip provenance closed: `{identifier['zip_provenance_closed']}`",
        f"- zip retention manifest: `{identifier['zip_retention_manifest_path']}`",
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
            "- formal Chroma index blocker closed: `no`",
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
    error: str | None = None
    provider_status = "missing_provider_family"
    provider_family: str | None = None
    try:
        provider_family, provider_status = resolve_provider_family(
            args.provider_family,
            formal_required=args.execute_build,
        )
        if args.execute_build:
            assert provider_family is not None
            try_build_index(index_dir, args.collection_name, provider_family)
    except FormalIndexBuildError as exc:  # pragma: no cover - control-flow path
        error = str(exc)

    status = determine_status(
        dry_run=not args.execute_build,
        provider_status=provider_status,
        error=error,
    )

    identifier = build_identifier(
        zip_path=zip_path,
        index_dir=index_dir,
        collection_name=args.collection_name,
        provider_family=provider_family,
        provider_status=provider_status,
        build_command=build_command,
        dry_run=not args.execute_build,
        status=status,
        error=error,
    )

    identifier_output.write_text(json.dumps(identifier, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report_output, identifier, error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
