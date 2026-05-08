#!/usr/bin/env python3
"""
Human-run-only formal R-Bot Chroma index inspection helper.

This script inspects an already-built index directory, records file hashes, and
materializes a retained identifier JSON without rebuilding the index.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


BUILD_DIR = Path(__file__).resolve().parent
DEFAULT_INDEX_DIR = Path("/tmp/rewritebench_rbot_formal_chroma_index_01")
DEFAULT_IDENTIFIER_OUTPUT = BUILD_DIR / "formal_chroma_index_identifier_v1.json"
DEFAULT_REPORT_OUTPUT = BUILD_DIR / "formal_chroma_index_inspect_report_v1.md"

CORPUS_ARTIFACT_URI = "https://doi.org/10.5281/zenodo.20087267"
CORPUS_SHA256 = "e7e68b08a4283467f899f05a3150c485e2bf615ccdde4f4ab76e0f08734e546a"
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_directory_hashes(index_dir: Path) -> list[dict[str, str]]:
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


def write_report(path: Path, identifier: dict[str, object]) -> None:
    lines = [
        "# Formal Chroma Index Inspect Report v1",
        "",
        "## Status",
        "",
        f"- index directory: `{identifier['index_directory']}`",
        f"- index file count: `{len(identifier['index_file_hashes'])}`",
        f"- collection name: `{identifier['chroma_collection_name']}`",
        f"- embedding model: `{identifier['embedding_model']}`",
        "",
        "## Gate Note",
        "",
        "- formal `R-Bot @120` generation may start: `no`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal Chroma index inspect helper")
    parser.add_argument("--index-dir", default=str(DEFAULT_INDEX_DIR))
    parser.add_argument("--collection-name", required=True)
    parser.add_argument("--provider-family", required=True)
    parser.add_argument("--index-id", required=True)
    parser.add_argument("--identifier-output", default=str(DEFAULT_IDENTIFIER_OUTPUT))
    parser.add_argument("--report-output", default=str(DEFAULT_REPORT_OUTPUT))
    args = parser.parse_args()

    index_dir = Path(args.index_dir)
    if not index_dir.exists():
        raise FileNotFoundError(f"Index directory not found: {index_dir}")

    identifier = {
        "index_id": args.index_id,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "corpus_artifact_uri": CORPUS_ARTIFACT_URI,
        "corpus_sha256": CORPUS_SHA256,
        "expected_zip_filename": EXPECTED_FILENAME,
        "extraction_contract_version": EXTRACTION_CONTRACT_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_provider_base_url_family": args.provider_family,
        "rule_vector_width": RULE_VECTOR_WIDTH,
        "total_dimension": TOTAL_DIMENSION,
        "retrieval_top_k": RETRIEVAL_TOP_K,
        "reranking_mode": RERANKING_MODE,
        "rrf_k": RRF_K,
        "similarity_threshold": None,
        "similarity_threshold_policy": "explicit_none_observed",
        "chroma_collection_name": args.collection_name,
        "index_directory": str(index_dir),
        "index_file_hashes": compute_directory_hashes(index_dir),
        "build_script_command": " ".join(sys.argv),
        "status": "inspected_existing_index",
    }

    identifier_output = Path(args.identifier_output)
    report_output = Path(args.report_output)
    identifier_output.write_text(json.dumps(identifier, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(report_output, identifier)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
