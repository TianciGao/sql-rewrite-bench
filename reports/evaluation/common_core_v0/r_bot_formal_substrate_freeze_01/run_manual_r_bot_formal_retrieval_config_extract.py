#!/usr/bin/env python3
"""
Human-run-only retrieval config extractor for formal R-Bot gate closure.

This script inspects visible substrate/config files and reports extracted or
blocked retrieval settings without executing R-Bot.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    marker_relpath = Path("reports") / "curation" / "common_core_v0_final_denominator.csv"
    for candidate in [start_path.resolve(), *start_path.resolve().parents]:
        if (candidate / ".git").is_dir() or (candidate / marker_relpath).is_file():
            return candidate
    raise RuntimeError(f"Unable to locate repo root from {start_path}")


FREEZE_DIR = Path(__file__).resolve().parent
ROOT = find_repo_root(FREEZE_DIR)
SUBSTRATE_INVENTORY_CSV = ROOT / "reports" / "evaluation" / "common_core_v0" / "runs" / "r_bot_pg1_recovery_canary_01" / "r_bot_substrate_inventory.csv"
INDEX_CONTRACT_JSON = FREEZE_DIR / "formal_index_dimension_contract_v1.json"
OUT_JSON = FREEZE_DIR / "formal_retrieval_config_extracted_v1.json"
OUT_MD = FREEZE_DIR / "formal_retrieval_config_extraction_report.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_visible_paths() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for row in read_csv_rows(SUBSTRATE_INVENTORY_CSV):
        key = row["substrate_item"]
        value = row["path_or_identifier"]
        if value.startswith("/"):
            mapping[key] = Path(value)
    return mapping


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None
    except UnicodeDecodeError:
        return None


def regex_extract(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return match.group(1)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Human-run-only formal retrieval config extractor")
    parser.add_argument("--output-dir", default=str(FREEZE_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_json = output_dir / OUT_JSON.name
    out_md = output_dir / OUT_MD.name

    visible_paths = load_visible_paths()
    config_path = visible_paths.get("config_file")
    rag_prompt_path = visible_paths.get("prompt_file_rag")
    rewriter_prompt_path = visible_paths.get("prompt_file_rewriter")
    index_path = visible_paths.get("chroma_index_dir")

    texts: dict[str, str] = {}
    source_notes: list[str] = []
    for label, path in [
        ("config_file", config_path),
        ("prompt_file_rag", rag_prompt_path),
        ("prompt_file_rewriter", rewriter_prompt_path),
    ]:
        if path is None:
            source_notes.append(f"{label}: missing from substrate inventory")
            continue
        text = safe_read(path)
        if text is None:
            source_notes.append(f"{label}: unreadable or missing at {path}")
            continue
        texts[label] = text
        source_notes.append(f"{label}: visible at {path}")

    combined_text = "\n".join(texts.values())
    with INDEX_CONTRACT_JSON.open(encoding="utf-8") as handle:
        index_contract = json.load(handle)

    top_k = regex_extract(
        [
            r"\btop_k\s*=\s*(\d+)",
            r"[\"']top_k[\"']\s*:\s*(\d+)",
            r"\bretriever\([^)]*top_k\s*=\s*(\d+)",
        ],
        combined_text,
    )
    rerank = regex_extract(
        [
            r"\brerank(?:ing)?\s*=\s*[\"']([^\"']+)[\"']",
            r"[\"']rerank(?:ing)?[\"']\s*:\s*[\"']([^\"']+)[\"']",
        ],
        combined_text,
    )
    threshold = regex_extract(
        [
            r"\b(?:similarity_)?threshold\s*=\s*([0-9.]+)",
            r"[\"'](?:similarity_)?threshold[\"']\s*:\s*([0-9.]+)",
        ],
        combined_text,
    )
    explicit_no_threshold = bool(
        re.search(r"\bthreshold\s*=\s*none\b|[\"']threshold[\"']\s*:\s*null|\bno threshold\b", combined_text, flags=re.I)
    )
    embedding_model = regex_extract(
        [
            r"OpenAIEmbedding\([^)]*model\s*=\s*[\"']([^\"']+)[\"']",
            r"[\"']embedding_model[\"']\s*:\s*[\"']([^\"']+)[\"']",
            r"\bembedding_model\s*=\s*[\"']([^\"']+)[\"']",
        ],
        combined_text,
    )

    index_identifier = None
    index_status = "blocked_index_not_visible"
    index_notes = []
    if index_path is not None and index_path.exists():
        index_identifier = str(index_path)
        index_status = "scratch_only_visible_not_formal_evidence"
        index_notes.append("visible index path exists but is /tmp scratch lineage only")
    else:
        index_notes.append("visible index path missing")

    extracted = {
        "config_id": "formal_retrieval_config_extracted_v1",
        "denominator_id": "common_core_v0_40_same_engine_120",
        "method_id": "r_bot",
        "route_id": "r_bot_same_engine_rewrite",
        "top_k": {
            "value": int(top_k) if top_k is not None else None,
            "status": "extracted" if top_k is not None else "blocked_not_visible_in_config_text",
        },
        "reranking_mode": {
            "value": rerank,
            "status": "extracted" if rerank is not None else "blocked_not_visible_in_config_text",
        },
        "similarity_threshold": {
            "value": float(threshold) if threshold is not None else (None if explicit_no_threshold else None),
            "status": "extracted" if threshold is not None else ("explicit_none" if explicit_no_threshold else "blocked_not_visible_in_config_text"),
        },
        "embedding_model_identity": {
            "value": embedding_model,
            "status": "extracted" if embedding_model is not None else "blocked_exact_model_not_visible",
            "provider_family": "openai_compatible",
        },
        "index_identifier": {
            "value": index_identifier,
            "status": index_status,
            "notes": index_notes,
        },
        "rule_vector_width": {
            "value": index_contract["dimension_decomposition"]["rule_vector_width"],
            "status": "taken_from_formal_dimension_contract",
        },
        "total_dimension": {
            "value": index_contract["total_dimension"],
            "status": "taken_from_formal_dimension_contract",
        },
        "source_notes": source_notes,
        "gate_rule": "do not open formal gate from this extraction alone",
    }

    out_json.write_text(json.dumps(extracted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(
        "\n".join(
            [
                "# Formal Retrieval Config Extraction Report",
                "",
                "## Status",
                "",
                f"- top_k: `{extracted['top_k']['status']}`",
                f"- reranking_mode: `{extracted['reranking_mode']['status']}`",
                f"- similarity_threshold: `{extracted['similarity_threshold']['status']}`",
                f"- embedding_model_identity: `{extracted['embedding_model_identity']['status']}`",
                f"- index_identifier: `{extracted['index_identifier']['status']}`",
                "- rule_vector_width: `taken_from_formal_dimension_contract`",
                "- total_dimension: `taken_from_formal_dimension_contract`",
                "",
                "## Visible Sources",
                "",
                *[f"- {note}" for note in source_notes],
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
