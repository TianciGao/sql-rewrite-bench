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


class FormalIndexInspectError(RuntimeError):
    """Inspect error with a retained status."""

    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


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


def coerce_vector_component_to_list(value: object, *, component_name: str, locator: str) -> list[object]:
    if value is None:
        raise FormalIndexInspectError(
            "missing_vector_component",
            f"{component_name} is missing at {locator}",
        )
    if hasattr(value, "tolist"):
        value = value.tolist()
    elif isinstance(value, tuple):
        value = list(value)
    if not isinstance(value, list):
        raise FormalIndexInspectError(
            "invalid_vector_component_type",
            f"{component_name} has invalid type at {locator}: {type(value).__name__}",
        )
    if len(value) == 0:
        raise FormalIndexInspectError(
            "empty_vector_component",
            f"{component_name} is empty at {locator}",
        )
    return value


def validate_embedding(value: object, *, expected_dim: int, component_name: str, locator: str) -> list[float]:
    value = coerce_vector_component_to_list(value, component_name=component_name, locator=locator)
    if len(value) != expected_dim:
        raise FormalIndexInspectError(
            "vector_component_dimension_mismatch",
            f"{component_name} dimension mismatch at {locator}: expected {expected_dim}, observed {len(value)}",
        )
    try:
        return [float(item) for item in value]
    except Exception as exc:
        raise FormalIndexInspectError(
            "invalid_vector_component",
            f"{component_name} contains non-numeric values at {locator}",
        ) from exc


def inspect_collection(index_dir: Path, collection_name: str) -> dict[str, int]:
    try:
        import chromadb  # type: ignore
    except Exception as exc:
        raise FormalIndexInspectError("chromadb_unavailable", "chromadb is not importable for collection inspection") from exc

    client = chromadb.PersistentClient(path=str(index_dir))
    collection = client.get_collection(collection_name)
    collection_count = int(collection.count())
    if collection_count <= 0:
        raise FormalIndexInspectError("empty_collection", f"Collection {collection_name} is empty")

    sample = collection.get(limit=1, include=["embeddings"])
    embeddings = sample.get("embeddings") if isinstance(sample, dict) else None
    embeddings = coerce_vector_component_to_list(
        embeddings,
        component_name="collection_sample_embeddings",
        locator=collection_name,
    )
    sample_embedding = validate_embedding(
        embeddings[0],
        expected_dim=TOTAL_DIMENSION,
        component_name="collection_sample_embedding",
        locator=collection_name,
    )
    sample_dimension = len(sample_embedding)
    return {
        "collection_document_count": collection_count,
        "collection_verified_dimension": sample_dimension,
    }


def write_report(path: Path, identifier: dict[str, object]) -> None:
    lines = [
        "# Formal Chroma Index Inspect Report v1",
        "",
        "## Status",
        "",
        f"- index directory: `{identifier['index_directory']}`",
        f"- index file count: `{len(identifier['index_file_hashes'])}`",
        f"- collection name: `{identifier['chroma_collection_name']}`",
        f"- collection document count: `{identifier.get('collection_document_count')}`",
        f"- verified embedding dimension: `{identifier.get('collection_verified_dimension')}`",
        f"- embedding model: `{identifier['embedding_model']}`",
        f"- status: `{identifier['status']}`",
        "",
        "## Gate Note",
        "",
        "- formal Chroma index blocker closed: `no`",
        "- current benchmark gate ready: `false`",
        "- formal `R-Bot @120` generation may start: `no`",
    ]
    if "error" in identifier:
        lines.extend(["", "## Error", "", f"- `{identifier['error']}`"])
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
    identifier_output = Path(args.identifier_output)
    report_output = Path(args.report_output)

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
        "index_file_hashes": compute_directory_hashes(index_dir) if index_dir.exists() else [],
        "current_benchmark_gate_ready": False,
        "formal_generation_may_start": False,
        "build_script_command": " ".join(sys.argv),
        "status": "inspect_failed",
    }

    try:
        if not index_dir.exists():
            raise FormalIndexInspectError("index_directory_missing", f"Index directory not found: {index_dir}")

        collection_stats = inspect_collection(index_dir, args.collection_name)
        identifier["collection_document_count"] = collection_stats["collection_document_count"]
        identifier["collection_verified_dimension"] = collection_stats["collection_verified_dimension"]

        if identifier["collection_verified_dimension"] != TOTAL_DIMENSION:
            raise FormalIndexInspectError(
                "vector_component_dimension_mismatch",
                f"Collection dimension mismatch: expected {TOTAL_DIMENSION}, observed {identifier['collection_verified_dimension']}",
            )

        identifier["status"] = "inspected_existing_index_gate_still_closed"
    except FormalIndexInspectError as exc:
        identifier["status"] = exc.status
        identifier["error"] = str(exc)

    identifier_output.write_text(json.dumps(identifier, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(report_output, identifier)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
