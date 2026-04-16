#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_exists(path: Path) -> bool:
    return path.exists()


def add_check(results: List[Dict[str, Any]], name: str, ok: bool, detail: str) -> None:
    results.append({
        "name": name,
        "ok": ok,
        "detail": detail,
    })


def validate_case(case_dir: Path) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    manifest_path = case_dir / "manifest.yaml"

    if not manifest_path.exists():
        return {
            "case_dir": str(case_dir),
            "ok": False,
            "error": "manifest.yaml not found",
            "checks": [],
        }

    manifest = load_yaml(manifest_path)

    case_id = manifest.get("case_id", case_dir.name)
    pool = manifest.get("pool", "")

    # Required top-level files
    add_check(results, "manifest_exists", True, str(manifest_path))
    add_check(results, "source_sql_exists", check_exists(case_dir / "source.sql"), "source.sql")
    add_check(results, "data_profile_exists", check_exists(case_dir / "data_profile.json"), "data_profile.json")

    # Rewrite presence
    positives = manifest.get("variants", {}).get("positives", [])
    negatives = manifest.get("variants", {}).get("negatives", [])
    add_check(results, "has_positive_variant", bool(positives), f"positives={positives}")
    add_check(results, "has_negative_variant", bool(negatives), f"negatives={negatives}")

    for rel in positives:
        add_check(results, f"positive_file::{rel}", check_exists(case_dir / rel), rel)
    for rel in negatives:
        add_check(results, f"negative_file::{rel}", check_exists(case_dir / rel), rel)

    # Manifest sections
    required_sections = [
        "provenance",
        "source",
        "targets",
        "variants",
        "features",
        "validation",
        "artifacts",
        "status",
    ]
    for section in required_sections:
        add_check(
            results,
            f"manifest_section::{section}",
            section in manifest,
            section,
        )

    # Required current pilot compatibility keys
    add_check(results, "top_level_case_id", "case_id" in manifest, "case_id")
    add_check(results, "top_level_pool", "pool" in manifest, "pool")

    # Schema files
    schema = manifest.get("schema", {})
    for key in ["pg_ddl", "mysql_ddl", "spark_ddl"]:
        rel = schema.get(key)
        ok = bool(rel) and check_exists(case_dir / rel)
        add_check(results, f"schema::{key}", ok, str(rel))

    # Metadata files
    metadata = manifest.get("metadata", {})
    engine_meta = metadata.get("engine_metadata")
    add_check(
        results,
        "metadata::engine_metadata",
        bool(engine_meta) and check_exists(case_dir / engine_meta),
        str(engine_meta),
    )

    # Validation files
    validation = manifest.get("validation", {})
    checker = validation.get("checker")
    witness = validation.get("witness_dataset")
    add_check(
        results,
        "validation::checker",
        bool(checker) and check_exists(case_dir / checker),
        str(checker),
    )
    add_check(
        results,
        "validation::witness_dataset",
        bool(witness) and check_exists(case_dir / witness),
        str(witness),
    )

    # Status flags
    status = manifest.get("status", {})
    for key in [
        "parse_checked",
        "exec_checked_pg",
        "exec_checked_mysql",
        "exec_checked_spark",
        "plan_checked",
        "schema_ready",
        "validation_ready",
        "release_grade",
    ]:
        add_check(
            results,
            f"status::{key}",
            key in status,
            f"{key}={status.get(key)}",
        )

    # Artifact paths (existence only if declared)
    artifacts = manifest.get("artifacts", {})
    for key, rel in artifacts.items():
        if isinstance(rel, str):
            add_check(
                results,
                f"artifact::{key}",
                check_exists(ROOT / rel),
                rel,
            )

    ok = all(item["ok"] for item in results)

    return {
        "case_id": case_id,
        "pool": pool,
        "case_dir": str(case_dir),
        "ok": ok,
        "checks": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", help="Path to case directory, e.g. cases/CONS/CONS_0003")
    parser.add_argument("--out", default="", help="Optional JSON output path")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    result = validate_case(case_dir)

    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")

    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())