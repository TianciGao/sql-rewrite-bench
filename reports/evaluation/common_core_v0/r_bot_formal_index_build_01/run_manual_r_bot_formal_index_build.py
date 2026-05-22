#!/usr/bin/env python3
"""
Human-run-only formal R-Bot Chroma index build helper.

This script does not run databases, does not execute SQL, and does not run
R-Bot. It verifies the retained ZIP artifact, reuses the frozen extracted-text
manifest package, and either:

1. performs a dry-run that writes identifier/report metadata only, or
2. builds a real Chroma-compatible index from retained ZIP contents without
   calling an embedding provider.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
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
FORMAL_RULE_VECTOR_CATALOG_JSON = BUILD_DIR / "formal_rule_vector_catalog_v1.json"
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
EMBED_DIM = 1536
RETRIEVAL_TOP_K = 10
RERANKING_MODE = "rrf"
RRF_K = 60
SIMILARITY_THRESHOLD = None
SIMILARITY_THRESHOLD_POLICY = "explicit_none_observed"
CHROMA_BATCH_SIZE = 128

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
    """Build error with a retained status."""

    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_json_value(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


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


def ensure_zip_is_valid(zip_path: Path) -> None:
    if zip_path.name != EXPECTED_FILENAME:
        raise FormalIndexBuildError(
            "unexpected_zip_filename",
            f"Unexpected ZIP filename: {zip_path.name} != {EXPECTED_FILENAME}",
        )
    if not zip_path.exists():
        raise FormalIndexBuildError("zip_not_found", f"ZIP file not found: {zip_path}")
    observed = sha256_file(zip_path)
    if observed != EXPECTED_ZIP_SHA256:
        raise FormalIndexBuildError(
            "zip_sha256_mismatch",
            f"ZIP SHA-256 mismatch: expected {EXPECTED_ZIP_SHA256}, observed {observed}",
        )
    with zipfile.ZipFile(zip_path) as archive:
        for entry_name in ALLOWED_TEXT_ENTRIES:
            try:
                archive.getinfo(entry_name)
            except KeyError as exc:
                raise FormalIndexBuildError(
                    "missing_zip_member",
                    f"Missing expected ZIP member: {entry_name}",
                ) from exc


def load_frozen_manifest_metadata() -> dict[str, Any]:
    if not MANIFEST_HASHES_JSON.exists():
        raise FormalIndexBuildError(
            "manifest_hashes_json_missing",
            f"Frozen manifest hashes JSON not found: {MANIFEST_HASHES_JSON}",
        )
    if not MANIFEST_CSV.exists():
        raise FormalIndexBuildError(
            "manifest_csv_missing",
            f"Frozen manifest CSV not found: {MANIFEST_CSV}",
        )

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
        raise FormalIndexBuildError(
            "manifest_row_count_mismatch",
            f"Frozen manifest row-count mismatch: CSV={row_count_from_csv}, hashes_json={manifest_row_count}",
        )
    if row_counts_by_entry_from_csv != manifest_row_counts_by_entry:
        raise FormalIndexBuildError(
            "manifest_entry_count_mismatch",
            "Frozen manifest per-entry row-count mismatch between CSV and hashes JSON",
        )

    return {
        "manifest_csv_path": str(MANIFEST_CSV),
        "manifest_hashes_json_path": str(MANIFEST_HASHES_JSON),
        "extracted_text_row_count": manifest_row_count,
        "extracted_rows_by_entry": manifest_row_counts_by_entry,
        "normalization_policy": hash_payload.get("normalization_policy", {}),
    }


def load_zip_retention_metadata() -> dict[str, Any]:
    if not ZIP_RETENTION_MANIFEST_JSON.exists():
        raise FormalIndexBuildError(
            "zip_retention_manifest_json_missing",
            f"ZIP retention manifest JSON not found: {ZIP_RETENTION_MANIFEST_JSON}",
        )
    if not ZIP_RETENTION_MANIFEST_CSV.exists():
        raise FormalIndexBuildError(
            "zip_retention_manifest_csv_missing",
            f"ZIP retention manifest CSV not found: {ZIP_RETENTION_MANIFEST_CSV}",
        )

    retention_payload = json.loads(ZIP_RETENTION_MANIFEST_JSON.read_text(encoding="utf-8"))
    with ZIP_RETENTION_MANIFEST_CSV.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))

    outer_rows = [row for row in csv_rows if row.get("artifact_scope") == "outer_zip"]
    if len(outer_rows) != 1:
        raise FormalIndexBuildError(
            "zip_retention_manifest_outer_zip_row_error",
            f"Expected exactly one outer_zip row, found {len(outer_rows)}",
        )
    outer_row = outer_rows[0]

    expected_uri = CORPUS_ARTIFACT_URI
    expected_filename = EXPECTED_FILENAME
    expected_sha = EXPECTED_ZIP_SHA256
    json_closed = bool(retention_payload.get("zip_external_provenance_closed"))
    status = str(retention_payload.get("retention_status", ""))
    uri = str(retention_payload.get("external_artifact_uri", ""))
    filename = str(retention_payload.get("expected_filename", ""))
    outer_sha = str(retention_payload.get("outer_zip_sha256", ""))

    if uri != expected_uri or filename != expected_filename or outer_sha != expected_sha:
        raise FormalIndexBuildError(
            "zip_retention_manifest_identity_mismatch",
            "ZIP retention manifest JSON does not match the retained DOI/filename/SHA-256 identity",
        )
    if status != "externally_retained_with_checksum" or not json_closed:
        raise FormalIndexBuildError(
            "zip_retention_manifest_not_closed",
            "ZIP retention manifest JSON does not record retained external provenance closure",
        )

    if (
        outer_row.get("external_artifact_uri", "") != expected_uri
        or outer_row.get("expected_filename", "") != expected_filename
        or outer_row.get("outer_zip_sha256", "") != expected_sha
        or outer_row.get("retention_status", "") != "externally_retained_with_checksum"
        or outer_row.get("zip_external_provenance_closed", "").strip().lower() != "yes"
    ):
        raise FormalIndexBuildError(
            "zip_retention_manifest_csv_mismatch",
            "ZIP retention manifest CSV does not match the retained DOI/filename/SHA-256 closure facts",
        )

    return {
        "zip_external_artifact_uri": uri,
        "zip_retention_status": status,
        "zip_provenance_closed": True,
        "zip_retention_manifest_path": str(ZIP_RETENTION_MANIFEST_JSON),
        "zip_retention_manifest_csv_path": str(ZIP_RETENTION_MANIFEST_CSV),
    }


def resolve_provider_family(provider_family: str | None, *, formal_required: bool) -> tuple[str | None, str]:
    normalized = provider_family.strip() if provider_family and provider_family.strip() else None
    if normalized:
        return normalized, "provider_family_recorded"
    if formal_required:
        raise FormalIndexBuildError(
            "missing_provider_family",
            "embedding provider/base_url family must be supplied for formal index metadata; use --provider-family",
        )
    return None, "missing_provider_family"


def load_frozen_rule_vector_catalog() -> dict[str, Any]:
    if not FORMAL_RULE_VECTOR_CATALOG_JSON.exists():
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_missing",
            f"Frozen rule-vector catalog not found: {FORMAL_RULE_VECTOR_CATALOG_JSON}",
        )

    try:
        payload = json.loads(FORMAL_RULE_VECTOR_CATALOG_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_json_error",
            f"Unable to parse frozen rule-vector catalog JSON: {FORMAL_RULE_VECTOR_CATALOG_JSON}",
        ) from exc

    if not payload.get("catalog_fully_frozen", False):
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_not_frozen",
            "Frozen rule-vector catalog JSON does not mark the canonical catalog as fully frozen",
        )

    if int(payload.get("rule_vector_width", -1)) != RULE_VECTOR_WIDTH:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_width_mismatch",
            f"Frozen rule-vector catalog width mismatch: expected {RULE_VECTOR_WIDTH}, observed {payload.get('rule_vector_width')}",
        )
    if int(payload.get("nl_rule_count", -1)) != 30:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_nl_count_mismatch",
            f"Frozen NL rule count mismatch: expected 30, observed {payload.get('nl_rule_count')}",
        )
    if int(payload.get("calcite_rule_count", -1)) != 70:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_calcite_count_mismatch",
            f"Frozen Calcite rule count mismatch: expected 70, observed {payload.get('calcite_rule_count')}",
        )
    if int(payload.get("unresolved_slot_count", -1)) != 0:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_unresolved_slots",
            f"Frozen rule-vector catalog has unresolved slots: {payload.get('unresolved_slot_count')}",
        )

    slot_partition = payload.get("slot_partition", {})
    if slot_partition.get("nl_vector_slots") != [0, 29] or slot_partition.get("calcite_vector_slots") != [30, 99]:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_slot_partition_mismatch",
            "Frozen rule-vector catalog slot partition does not match NL 0-29 and Calcite 30-99",
        )

    nl_slots = payload.get("nl_slots")
    calcite_slots = payload.get("calcite_slots")
    if not isinstance(nl_slots, list) or not isinstance(calcite_slots, list):
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_slots_missing",
            "Frozen rule-vector catalog JSON is missing nl_slots or calcite_slots arrays",
        )

    if len(nl_slots) != 30 or len(calcite_slots) != 70:
        raise FormalIndexBuildError(
            "frozen_rule_vector_catalog_slot_count_mismatch",
            f"Frozen rule-vector catalog slot arrays have invalid lengths: nl={len(nl_slots)}, calcite={len(calcite_slots)}",
        )

    def normalize_slots(
        slots: list[Any],
        *,
        family: str,
        expected_vector_start: int,
        expected_count: int,
        family_slot_key: str,
    ) -> list[str]:
        names: list[str] = []
        seen_names: set[str] = set()
        seen_vector_slots: set[int] = set()
        seen_family_slots: set[int] = set()
        for expected_offset, slot in enumerate(slots):
            if not isinstance(slot, dict):
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_invalid_slot",
                    f"Frozen {family} slot entry {expected_offset} is not an object",
                )
            vector_slot = slot.get("vector_slot")
            family_slot = slot.get(family_slot_key)
            rule_name = slot.get("rule_name")
            status = slot.get("status")

            expected_vector_slot = expected_vector_start + expected_offset
            if vector_slot != expected_vector_slot:
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_nondeterministic_order",
                    f"Frozen {family} vector slot mismatch at offset {expected_offset}: expected {expected_vector_slot}, observed {vector_slot}",
                )
            if family_slot != expected_offset:
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_nondeterministic_order",
                    f"Frozen {family} family slot mismatch at offset {expected_offset}: expected {expected_offset}, observed {family_slot}",
                )
            if not isinstance(rule_name, str) or not rule_name:
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_invalid_rule_name",
                    f"Frozen {family} slot {expected_offset} has invalid rule_name",
                )
            if status == "unresolved":
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_unresolved_slots",
                    f"Frozen {family} slot {expected_offset} remains unresolved: {rule_name}",
                )
            if status not in {"recovered_from_java", "recovered_from_structured_jsonl", "alias_resolved"}:
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_invalid_status",
                    f"Frozen {family} slot {expected_offset} has invalid status: {status}",
                )
            if rule_name in seen_names or vector_slot in seen_vector_slots or family_slot in seen_family_slots:
                raise FormalIndexBuildError(
                    "frozen_rule_vector_catalog_duplicate_slot",
                    f"Frozen {family} slot duplication detected at {rule_name}",
                )
            seen_names.add(rule_name)
            seen_vector_slots.add(vector_slot)
            seen_family_slots.add(family_slot)
            names.append(rule_name)

        if len(names) != expected_count:
            raise FormalIndexBuildError(
                "frozen_rule_vector_catalog_slot_count_mismatch",
                f"Frozen {family} slot normalization length mismatch: expected {expected_count}, observed {len(names)}",
            )
        return names

    nl_rules = normalize_slots(
        nl_slots,
        family="NL",
        expected_vector_start=0,
        expected_count=30,
        family_slot_key="nl_slot",
    )
    calcite_rules = normalize_slots(
        calcite_slots,
        family="Calcite",
        expected_vector_start=30,
        expected_count=70,
        family_slot_key="calcite_slot",
    )

    return {
        "nl_rules": nl_rules,
        "calcite_rules": calcite_rules,
        "rule_vector_width": RULE_VECTOR_WIDTH,
        "rule_catalog_source": {
            "catalog_json_path": str(FORMAL_RULE_VECTOR_CATALOG_JSON),
            "catalog_id": payload.get("catalog_id"),
            "nl_catalog_count": len(nl_rules),
            "calcite_catalog_count": len(calcite_rules),
            "catalog_fully_frozen": True,
            "slot_order_basis": payload.get("calcite_slot_order_basis", {}),
        },
    }


def read_jsonl_member(archive: zipfile.ZipFile, entry_name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with archive.open(entry_name) as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            try:
                decoded = raw_line.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise FormalIndexBuildError(
                    "zip_member_decode_error",
                    f"Unable to decode {entry_name} line {line_number} as UTF-8",
                ) from exc
            try:
                rows.append(json.loads(decoded))
            except json.JSONDecodeError as exc:
                raise FormalIndexBuildError(
                    "zip_member_json_error",
                    f"Unable to parse JSON in {entry_name} line {line_number}",
                ) from exc
    return rows


def coerce_vector_component_to_list(value: Any, *, component_name: str, locator: str) -> list[Any]:
    if value is None:
        raise FormalIndexBuildError(
            "missing_vector_component",
            f"{component_name} is missing at {locator}",
        )

    if hasattr(value, "tolist"):
        value = value.tolist()
    elif isinstance(value, tuple):
        value = list(value)

    if not isinstance(value, list):
        raise FormalIndexBuildError(
            "invalid_vector_component_type",
            f"{component_name} has invalid type at {locator}: {type(value).__name__}",
        )
    if len(value) == 0:
        raise FormalIndexBuildError(
            "empty_vector_component",
            f"{component_name} is empty at {locator}",
        )
    return value


def validate_embedding(value: Any, *, expected_dim: int, component_name: str, locator: str) -> list[float]:
    value = coerce_vector_component_to_list(value, component_name=component_name, locator=locator)
    if len(value) != expected_dim:
        raise FormalIndexBuildError(
            "vector_component_dimension_mismatch",
            f"{component_name} dimension mismatch at {locator}: expected {expected_dim}, observed {len(value)}",
        )
    try:
        return [float(item) for item in value]
    except Exception as exc:
        raise FormalIndexBuildError(
            "invalid_vector_component",
            f"{component_name} contains non-numeric values at {locator}",
        ) from exc


def get_one_hot(rule_catalog: list[str], matched_rules: list[str], *, locator: str, family: str) -> list[float]:
    unknown_rules = sorted({rule for rule in matched_rules if rule not in rule_catalog})
    if unknown_rules:
        raise FormalIndexBuildError(
            "unknown_rule_label",
            f"Unknown {family} rule labels at {locator}: {unknown_rules}",
        )
    one_hot = [0.0] * len(rule_catalog)
    index_by_rule = {rule: idx for idx, rule in enumerate(rule_catalog)}
    for rule in matched_rules:
        one_hot[index_by_rule[rule]] = 1.0
    one_count = sum(one_hot)
    if one_count > 0:
        one_hot = [value / math.sqrt(one_count) for value in one_hot]
    return one_hot


def ensure_target_index_dir_ready(index_dir: Path) -> Path:
    temp_dir = Path(f"{index_dir}_build_tmp")
    if temp_dir.exists():
        raise FormalIndexBuildError(
            "temp_index_dir_exists",
            f"Temporary build directory already exists: {temp_dir}",
        )
    if index_dir.exists() and any(index_dir.iterdir()):
        raise FormalIndexBuildError(
            "target_index_dir_not_empty",
            f"Target index directory is not empty: {index_dir}",
        )
    return temp_dir


def finalize_index_dir(temp_dir: Path, index_dir: Path) -> None:
    if index_dir.exists():
        if any(index_dir.iterdir()):
            raise FormalIndexBuildError(
                "target_index_dir_not_empty",
                f"Target index directory became non-empty before finalize: {index_dir}",
            )
        index_dir.rmdir()
    temp_dir.rename(index_dir)


def build_real_index(
    *,
    zip_path: Path,
    index_dir: Path,
    collection_name: str,
    provider_family: str,
) -> dict[str, Any]:
    try:
        import chromadb  # type: ignore
    except Exception as exc:
        raise FormalIndexBuildError(
            "chromadb_unavailable",
            "chromadb is not importable in this environment",
        ) from exc

    rule_catalog = load_frozen_rule_vector_catalog()
    zero_rule_vector = [0.0] * RULE_VECTOR_WIDTH
    zero_template_embedding = [0.0] * EMBED_DIM
    zero_template_fingerprint = fingerprint_json_value(zero_template_embedding)

    temp_dir = ensure_target_index_dir_ready(index_dir)
    stats: dict[str, Any] = {
        "inserted_node_count": 0,
        "query_row_count": 0,
        "zero_fill_rule_vector_count": 0,
        "zero_fill_template_embedding_count": 0,
        "empty_sql_record_count": 0,
        "empty_sql_template_record_count": 0,
        "collection_verified_dimension": None,
        "collection_count": 0,
        "build_mode": "provider_free_reuse_retained_zip_embeddings",
        "rule_catalog_source": rule_catalog["rule_catalog_source"],
    }

    batch_ids: list[str] = []
    batch_docs: list[str] = []
    batch_metadatas: list[dict[str, Any]] = []
    batch_embeddings: list[list[float]] = []
    first_inserted_id: str | None = None

    try:
        with zipfile.ZipFile(zip_path) as archive:
            query_rows = read_jsonl_member(archive, "stackoverflow-rewrite-query-optimization.jsonl")
            rule_rows = read_jsonl_member(archive, "stackoverflow-rewrite-rules-query-optimization.jsonl")
            template_rows = read_jsonl_member(archive, "stackoverflow-rewrite-sql-templates-query-optimization.jsonl")
            template_embed_rows = read_jsonl_member(
                archive,
                "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl",
            )

        template_embed_map: dict[str, list[float]] = {}
        template_embed_fingerprints: dict[str, str] = {}
        for row in template_embed_rows:
            template = str(row.get("sql_template", ""))
            locator = f"template_embed:{template[:80]}"
            template_embedding = validate_embedding(
                row.get("embedding"),
                expected_dim=EMBED_DIM,
                component_name="sql_template_embedding",
                locator=locator,
            )
            template_embed_map[template] = template_embedding
            template_embed_fingerprints[template] = fingerprint_json_value(template_embedding)

        sql_to_rule_vector: dict[str, list[float]] = {}
        rule_vector_fingerprints: dict[str, str] = {}
        for row in rule_rows:
            sql = str(row.get("sql", ""))
            nl_rules = [str(item) for item in row.get("nl_rules", [])]
            calcite_rules = [str(item) for item in row.get("rules", [])]
            rule_locator = f"rule_rows sql_fingerprint={fingerprint_json_value(sql)[:12]}"
            one_hot = get_one_hot(
                rule_catalog["nl_rules"],
                nl_rules,
                locator=rule_locator,
                family="NL",
            ) + get_one_hot(
                rule_catalog["calcite_rules"],
                calcite_rules,
                locator=rule_locator,
                family="Calcite",
            )
            if len(one_hot) != RULE_VECTOR_WIDTH:
                raise FormalIndexBuildError(
                    "dimension_mismatch",
                    f"Rule vector dimension mismatch for SQL fingerprint {fingerprint_json_value(sql)[:12]}",
                )
            sql_to_rule_vector[sql] = one_hot
            rule_vector_fingerprints[sql] = fingerprint_json_value(one_hot)

        sql_to_templates: dict[str, list[str]] = {}
        for row in template_rows:
            myid = f"{row.get('id', '')}-{row.get('answer_id', '')}"
            per_sql: dict[str, list[str]] = {}
            for item in row.get("sql_templates", []):
                if not isinstance(item, dict):
                    continue
                sql = str(item.get("sql", ""))
                template = str(item.get("template", ""))
                per_sql.setdefault(sql, []).append(template)
            for sql, templates in per_sql.items():
                sql_to_templates[f"{myid}-{sql}"] = templates

        temp_dir.mkdir(parents=True)
        client = chromadb.PersistentClient(path=str(temp_dir))
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={
                "embedding_model": EMBEDDING_MODEL,
                "provider_family": provider_family,
                "rule_vector_width": RULE_VECTOR_WIDTH,
                "total_dimension": TOTAL_DIMENSION,
                "build_mode": "provider_free_reuse_retained_zip_embeddings",
            },
        )

        def flush_batch() -> None:
            nonlocal first_inserted_id
            if not batch_ids:
                return
            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metadatas,
                embeddings=batch_embeddings,
            )
            if first_inserted_id is None:
                first_inserted_id = batch_ids[0]
            batch_ids.clear()
            batch_docs.clear()
            batch_metadatas.clear()
            batch_embeddings.clear()

        for row in query_rows:
            stats["query_row_count"] += 1
            myid = f"{row.get('id', '')}-{row.get('answer_id', '')}"
            summary = str(row.get("summary", ""))
            summary_embedding = validate_embedding(
                row.get("embedding"),
                expected_dim=EMBED_DIM,
                component_name="summary_embedding",
                locator=myid,
            )

            sqls = [str(item) for item in row.get("question_body_sqls", [])]
            if len(sqls) == 0:
                stats["empty_sql_record_count"] += 1
                sqls = [""]

            sql_structure_fingerprints: set[str] = set()
            for sql in sqls:
                rule_vector = sql_to_rule_vector.get(sql)
                rule_fingerprint = rule_vector_fingerprints.get(sql)
                if rule_vector is None:
                    stats["zero_fill_rule_vector_count"] += 1
                    rule_vector = zero_rule_vector
                    rule_fingerprint = fingerprint_json_value(zero_rule_vector)

                sql_templates = sql_to_templates.get(f"{myid}-{sql}", [])
                if len(sql_templates) == 0:
                    stats["empty_sql_template_record_count"] += 1
                    sql_templates = [""]

                for sql_template in sql_templates:
                    sql_template_embedding = template_embed_map.get(sql_template)
                    template_fingerprint = template_embed_fingerprints.get(sql_template)
                    if sql_template_embedding is None:
                        if sql_template == "":
                            stats["zero_fill_template_embedding_count"] += 1
                            sql_template_embedding = zero_template_embedding
                            template_fingerprint = zero_template_fingerprint
                        else:
                            raise FormalIndexBuildError(
                                "missing_vector_component",
                                f"Missing SQL-template embedding for non-empty template at {myid}",
                            )

                    sql_structure_fingerprint = f"{rule_fingerprint}|{template_fingerprint}"
                    if sql_structure_fingerprint in sql_structure_fingerprints:
                        continue

                    final_embedding = [value / math.sqrt(3.0) for value in (summary_embedding + rule_vector + sql_template_embedding)]
                    if len(final_embedding) != TOTAL_DIMENSION:
                        raise FormalIndexBuildError(
                            "dimension_mismatch",
                            f"Final embedding dimension mismatch at {myid}: expected {TOTAL_DIMENSION}, observed {len(final_embedding)}",
                        )

                    content = f"{summary}\n{sql}\n{sql_template}"
                    node_id = hashlib.sha256(
                        f"{myid}\n{content}\n{sql_structure_fingerprint}".encode("utf-8")
                    ).hexdigest()
                    metadata = {
                        "references": str([myid]),
                        "source_record_id": myid,
                        "build_mode": "provider_free_reuse_retained_zip_embeddings",
                    }

                    batch_ids.append(node_id)
                    batch_docs.append(content)
                    batch_metadatas.append(metadata)
                    batch_embeddings.append(final_embedding)
                    stats["inserted_node_count"] += 1
                    sql_structure_fingerprints.add(sql_structure_fingerprint)

                    if len(batch_ids) >= CHROMA_BATCH_SIZE:
                        flush_batch()

        flush_batch()

        stats["collection_count"] = int(collection.count())
        if stats["collection_count"] != stats["inserted_node_count"]:
            raise FormalIndexBuildError(
                "collection_count_mismatch",
                f"Collection count mismatch: inserted={stats['inserted_node_count']}, collection={stats['collection_count']}",
            )
        if first_inserted_id is None:
            raise FormalIndexBuildError("empty_index_build", "No documents were inserted into the Chroma collection")

        sample = collection.get(ids=[first_inserted_id], include=["embeddings"])
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
        if sample_dimension != TOTAL_DIMENSION:
            raise FormalIndexBuildError(
                "dimension_mismatch",
                f"Stored collection embedding dimension mismatch: expected {TOTAL_DIMENSION}, observed {sample_dimension}",
            )
        stats["collection_verified_dimension"] = sample_dimension

        finalize_index_dir(temp_dir, index_dir)
        stats["index_file_hashes"] = compute_directory_hashes(index_dir)
        return stats
    except Exception:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise


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
    build_stats: dict[str, Any] | None,
) -> dict[str, object]:
    manifest_metadata = load_frozen_manifest_metadata()
    zip_retention_metadata = load_zip_retention_metadata()
    index_id: str | None = None
    if dry_run:
        index_id = "r_bot_formal_chroma_index_01_dry_run_preview"
    elif status == "built_real_index_gate_still_closed":
        index_id = "r_bot_formal_chroma_index_01"

    index_file_hashes = build_stats["index_file_hashes"] if build_stats else compute_directory_hashes(index_dir)
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
        "index_file_hashes": index_file_hashes,
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
        "build_executed": status == "built_real_index_gate_still_closed",
        "current_benchmark_gate_ready": False,
        "formal_generation_may_start": False,
        "status": status,
    }
    if build_stats:
        identifier.update(
            {
                "collection_document_count": build_stats["collection_count"],
                "collection_verified_dimension": build_stats["collection_verified_dimension"],
                "build_mode": build_stats["build_mode"],
                "query_row_count": build_stats["query_row_count"],
                "inserted_node_count": build_stats["inserted_node_count"],
                "zero_fill_rule_vector_count": build_stats["zero_fill_rule_vector_count"],
                "zero_fill_template_embedding_count": build_stats["zero_fill_template_embedding_count"],
                "empty_sql_record_count": build_stats["empty_sql_record_count"],
                "empty_sql_template_record_count": build_stats["empty_sql_template_record_count"],
                "rule_catalog_source": build_stats["rule_catalog_source"],
            }
        )
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
    if "collection_document_count" in identifier:
        lines.extend(
            [
                "",
                "## Build Facts",
                "",
                f"- collection document count: `{identifier['collection_document_count']}`",
                f"- verified embedding dimension: `{identifier['collection_verified_dimension']}`",
                f"- zero-fill rule vector count: `{identifier['zero_fill_rule_vector_count']}`",
                f"- zero-fill template embedding count: `{identifier['zero_fill_template_embedding_count']}`",
            ]
        )
    if error:
        lines.extend(["", "## Error", "", f"- `{error}`"])
    lines.extend(
        [
            "",
            "## Gate Note",
            "",
            "- formal Chroma index blocker closed: `no`",
            "- current benchmark gate ready: `false`",
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
    status = "missing_provider_family"
    build_stats: dict[str, Any] | None = None

    try:
        provider_family, provider_status = resolve_provider_family(
            args.provider_family,
            formal_required=args.execute_build,
        )
        if args.execute_build:
            assert provider_family is not None
            build_stats = build_real_index(
                zip_path=zip_path,
                index_dir=index_dir,
                collection_name=args.collection_name,
                provider_family=provider_family,
            )
            status = "built_real_index_gate_still_closed"
        else:
            status = provider_status
    except FormalIndexBuildError as exc:
        status = exc.status
        error = str(exc)

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
        build_stats=build_stats,
    )

    identifier_output.write_text(json.dumps(identifier, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report_output, identifier, error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
