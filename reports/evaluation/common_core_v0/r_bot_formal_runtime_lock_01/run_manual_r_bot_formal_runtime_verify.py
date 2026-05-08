#!/usr/bin/env python3
"""
Human-run-only R-Bot formal runtime/dependency verification helper.

This script does not run databases, does not execute SQL, and does not run
R-Bot. It verifies the formal runtime lock against the current Python
environment and the retained formal Chroma index identifier.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import platform
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


BUILD_DIR = Path(__file__).resolve().parent
DEFAULT_LOCK_PATH = BUILD_DIR / "r_bot_formal_requirements_lock.txt"
DEFAULT_SCHEMA_PATH = BUILD_DIR / "runtime_environment_snapshot_schema.json"
DEFAULT_IDENTIFIER_PATH = (
    Path(__file__).resolve().parents[1]
    / "r_bot_formal_index_build_01"
    / "formal_chroma_index_identifier_v1.json"
)
DEFAULT_SNAPSHOT_OUTPUT = BUILD_DIR / "runtime_environment_snapshot_v1.json"
DEFAULT_REPORT_OUTPUT = BUILD_DIR / "runtime_verify_report_v1.md"

EXPECTED_INDEX_ID = "r_bot_formal_chroma_index_01"
EXPECTED_DIMENSION = 3172
EXPECTED_RULE_VECTOR_WIDTH = 100
EXPECTED_EMBEDDING_MODEL = "text-embedding-3-small"

IMPORT_TARGETS = {
    "chromadb": "chromadb",
    "jsonlines": "jsonlines",
    "jpype1": "jpype",
    "llama-index": "llama_index",
    "llama-index-core": "llama_index.core",
    "llama-index-embeddings-huggingface": "llama_index.embeddings.huggingface",
    "llama-index-embeddings-openai": "llama_index.embeddings.openai",
    "llama-index-instrumentation": "llama_index.instrumentation",
    "llama-index-llms-openai": "llama_index.llms.openai",
    "llama-index-llms-openai-like": "llama_index.llms.openai_like",
    "llama-index-vector-stores-chroma": "llama_index.vector_stores.chroma",
    "llama-index-workflows": "llama_index.workflows",
    "numpy": "numpy",
    "openai": "openai",
    "prettytable": "prettytable",
    "psycopg": "psycopg",
    "psycopg-binary": "psycopg",
    "psycopg2-binary": "psycopg2",
    "scipy": "scipy",
    "sentence-transformers": "sentence_transformers",
    "sqlalchemy": "sqlalchemy",
    "sqlglot": "sqlglot",
    "torch": "torch",
    "transformers": "transformers",
}


class RuntimeVerifyError(RuntimeError):
    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_requirements_lock(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        raise RuntimeVerifyError("requirements_lock_missing", f"Requirements lock not found: {path}")
    rows: list[tuple[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise RuntimeVerifyError(
                "requirements_lock_parse_error",
                f"Requirements lock line is not pinned with == : {line}",
            )
        name, version = line.split("==", 1)
        rows.append((name.strip(), version.strip()))
    return rows


def load_index_identifier(path: Path) -> dict[str, object]:
    if not path.exists():
        raise RuntimeVerifyError("index_identifier_missing", f"Index identifier not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeVerifyError("index_identifier_json_error", f"Unable to parse index identifier: {path}") from exc

    if payload.get("index_id") != EXPECTED_INDEX_ID:
        raise RuntimeVerifyError(
            "index_identifier_value_mismatch",
            f"Index identifier id mismatch: expected {EXPECTED_INDEX_ID}, observed {payload.get('index_id')}",
        )
    if int(payload.get("total_dimension", -1)) != EXPECTED_DIMENSION:
        raise RuntimeVerifyError(
            "index_identifier_value_mismatch",
            f"Index identifier total dimension mismatch: expected {EXPECTED_DIMENSION}, observed {payload.get('total_dimension')}",
        )
    if int(payload.get("rule_vector_width", -1)) != EXPECTED_RULE_VECTOR_WIDTH:
        raise RuntimeVerifyError(
            "index_identifier_value_mismatch",
            f"Index identifier rule-vector width mismatch: expected {EXPECTED_RULE_VECTOR_WIDTH}, observed {payload.get('rule_vector_width')}",
        )
    if payload.get("embedding_model") != EXPECTED_EMBEDDING_MODEL:
        raise RuntimeVerifyError(
            "index_identifier_value_mismatch",
            f"Index identifier embedding model mismatch: expected {EXPECTED_EMBEDDING_MODEL}, observed {payload.get('embedding_model')}",
        )
    return payload


def check_packages(requirements: list[tuple[str, str]]) -> tuple[list[dict[str, object]], list[str]]:
    results: list[dict[str, object]] = []
    errors: list[str] = []
    for distribution, expected_version in requirements:
        import_target = IMPORT_TARGETS.get(distribution, distribution.replace("-", "_"))
        observed_version: str | None = None
        import_ok = False
        version_match = False
        error: str | None = None
        try:
            importlib.import_module(import_target)
            import_ok = True
            observed_version = metadata.version(distribution)
            version_match = observed_version == expected_version
            if not version_match:
                error = f"version mismatch: expected {expected_version}, observed {observed_version}"
        except Exception as exc:
            error = str(exc)

        row = {
            "distribution": distribution,
            "expected_version": expected_version,
            "observed_version": observed_version,
            "import_target": import_target,
            "import_ok": import_ok,
            "version_match": version_match,
            "error": error,
        }
        results.append(row)
        if not import_ok or not version_match:
            errors.append(f"{distribution}: {error}")
    return results, errors


def build_snapshot(
    *,
    lock_path: Path,
    identifier_path: Path,
    package_checks: list[dict[str, object]],
    package_errors: list[str],
    identifier: dict[str, object] | None,
    status: str,
    errors: list[str],
) -> dict[str, object]:
    provider_family = None
    provider_name = None
    base_url = None
    index_directory = None
    collection_name = None
    index_id = None
    rule_vector_width = None
    total_dimension = None
    index_visible = False

    if identifier is not None:
        provider_family = identifier.get("embedding_provider_base_url_family")
        provider_name = provider_family
        base_url = None
        index_directory = identifier.get("index_directory")
        collection_name = identifier.get("chroma_collection_name")
        index_id = identifier.get("index_id")
        rule_vector_width = identifier.get("rule_vector_width")
        total_dimension = identifier.get("total_dimension")
        if isinstance(index_directory, str):
            index_visible = Path(index_directory).exists()

    return {
        "snapshot_id": "r_bot_formal_runtime_environment_snapshot_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "python": {
            "version": sys.version,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
            },
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "platform": platform.platform(),
        },
        "runtime_lock": {
            "requirements_lock_path": str(lock_path),
            "requirements_lock_sha256": sha256_file(lock_path),
            "schema_path": str(DEFAULT_SCHEMA_PATH),
        },
        "provider_metadata": {
            "provider_family": provider_family,
            "provider_name": provider_name,
            "base_url": base_url,
            "secrets_present": False,
        },
        "formal_index": {
            "identifier_path": str(identifier_path),
            "index_id": index_id,
            "index_directory": index_directory,
            "index_directory_visible": index_visible,
            "collection_name": collection_name,
            "rule_vector_width": rule_vector_width,
            "total_dimension": total_dimension,
        },
        "package_checks": package_checks,
        "status": status,
        "errors": errors + package_errors,
        "current_benchmark_gate_ready": False,
        "formal_generation_may_start": False,
    }


def write_report(path: Path, snapshot: dict[str, object]) -> None:
    package_checks = snapshot["package_checks"]
    failures = [row for row in package_checks if not row["import_ok"] or not row["version_match"]]
    lines = [
        "# R-Bot Formal Runtime Verify Report v1",
        "",
        "## Status",
        "",
        f"- status: `{snapshot['status']}`",
        f"- python executable: `{snapshot['python']['executable']}`",
        f"- python version: `{snapshot['python']['version_info']['major']}.{snapshot['python']['version_info']['minor']}.{snapshot['python']['version_info']['micro']}`",
        f"- platform: `{snapshot['platform']['platform']}`",
        f"- requirements lock: `{snapshot['runtime_lock']['requirements_lock_path']}`",
        f"- requirements lock sha256: `{snapshot['runtime_lock']['requirements_lock_sha256']}`",
        f"- provider family: `{snapshot['provider_metadata']['provider_family']}`",
        f"- index identifier: `{snapshot['formal_index']['identifier_path']}`",
        f"- index id: `{snapshot['formal_index']['index_id']}`",
        f"- index directory visible: `{snapshot['formal_index']['index_directory_visible']}`",
        f"- total dimension: `{snapshot['formal_index']['total_dimension']}`",
        f"- package checks: `{len(package_checks)}`",
        f"- package failures: `{len(failures)}`",
        "",
        "## Gate Note",
        "",
        "- runtime/dependency lock blocker closed by this report alone: `no`",
        "- current benchmark gate ready: `false`",
        "- formal `R-Bot @120` generation may start: `no`",
    ]
    if snapshot["errors"]:
        lines.extend(["", "## Errors", ""])
        for error in snapshot["errors"]:
            lines.append(f"- `{error}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only R-Bot formal runtime verify helper")
    parser.add_argument("--requirements-lock", default=str(DEFAULT_LOCK_PATH))
    parser.add_argument("--index-identifier", default=str(DEFAULT_IDENTIFIER_PATH))
    parser.add_argument("--snapshot-output", default=str(DEFAULT_SNAPSHOT_OUTPUT))
    parser.add_argument("--report-output", default=str(DEFAULT_REPORT_OUTPUT))
    args = parser.parse_args()

    lock_path = Path(args.requirements_lock)
    identifier_path = Path(args.index_identifier)
    snapshot_output = Path(args.snapshot_output)
    report_output = Path(args.report_output)

    status = "runtime_verify_failed"
    errors: list[str] = []
    identifier: dict[str, object] | None = None

    try:
        requirements = parse_requirements_lock(lock_path)
        identifier = load_index_identifier(identifier_path)
        package_checks, package_errors = check_packages(requirements)
        index_dir = identifier.get("index_directory")
        if not isinstance(index_dir, str) or not Path(index_dir).exists():
            raise RuntimeVerifyError("index_directory_not_visible", f"Formal index directory not visible: {index_dir}")
        status = "runtime_verify_passed_gate_still_closed" if not package_errors else "runtime_verify_failed"
    except RuntimeVerifyError as exc:
        requirements = parse_requirements_lock(lock_path)
        package_checks, package_errors = check_packages(requirements)
        status = exc.status
        errors.append(str(exc))

    snapshot = build_snapshot(
        lock_path=lock_path,
        identifier_path=identifier_path,
        package_checks=package_checks,
        package_errors=package_errors,
        identifier=identifier,
        status=status,
        errors=errors,
    )
    snapshot_output.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(report_output, snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
