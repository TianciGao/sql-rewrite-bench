#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from openai import OpenAI


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_ROOT = Path(__file__).resolve().parent
PROMPT_TEMPLATE_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md"
RUN_PLAN_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_run_plan.json"
COMMAND_MATRIX_PATH = RUN_ROOT / "generation_command_matrix.csv"
RESULTS_PATH = RUN_ROOT / "run_results.json"

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MAX_TOKENS = 2048
TEMPERATURE = 0
TOP_P = 1
DENOMINATOR_ID = "common_core_v0_40"
METHOD_ID = "direct_llm"
ROUTE_ID = "direct_llm_same_engine_rewrite"
REQUIRED_ENV_VARS = ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_API_BASE")
SQL_START_KEYWORDS = (
    "select",
    "with",
    "values",
    "(",  # Allow wrapped selects.
    "/*",
    "--",
)
PROSE_MARKERS = (
    "here is",
    "here's",
    "the rewritten",
    "rewrite:",
    "explanation",
    "i rewrote",
    "this query",
    "sql rewrite",
)


@dataclass
class Row:
    case_id: str
    pool: str
    engine: str
    route_id: str
    source_sql_path: str
    schema_path: str
    prompt_path: str
    raw_response_path: str
    generated_sql_path: str
    denominator_id: str
    method_id: str
    temperature: int
    top_p: int
    max_tokens: int


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_run_plan() -> dict[str, Any]:
    return json.loads(RUN_PLAN_PATH.read_text(encoding="utf-8"))


def require_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE") or ""
    return {"api_key": api_key, "base_url": base_url}


def sanitize_base_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    netloc = parts.hostname or parts.netloc
    if parts.port:
        netloc = f"{netloc}:{parts.port}"
    return urlunsplit((parts.scheme, netloc, parts.path, "", ""))


def provider_from_base_url(base_url: str) -> str:
    parts = urlsplit(base_url)
    return parts.hostname or "openai_compatible"


def load_rows() -> list[Row]:
    with COMMAND_MATRIX_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [
            Row(
                case_id=row["case_id"],
                pool=row["pool"],
                engine=row["engine"],
                route_id=row["route_id"],
                source_sql_path=row["source_sql_path"],
                schema_path=row["schema_path"],
                prompt_path=row["prompt_path"],
                raw_response_path=row["raw_response_path"],
                generated_sql_path=row["generated_sql_path"],
                denominator_id=row["denominator_id"],
                method_id=row["method_id"],
                temperature=int(row["temperature"]),
                top_p=int(row["top_p"]),
                max_tokens=int(row["max_tokens"]),
            )
            for row in reader
        ]
    return rows


def read_text(path_str: str) -> str:
    return (REPO_ROOT / path_str).read_text(encoding="utf-8").strip()


def build_prompt(template: str, row: Row) -> str:
    schema_sql = read_text(row.schema_path)
    source_sql = read_text(row.source_sql_path)
    prompt = template.replace("{{target_engine}}", row.engine)
    prompt = prompt.replace("{{schema_sql}}", schema_sql)
    prompt = prompt.replace("{{source_sql}}", source_sql)
    return prompt.rstrip() + "\n"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def classify_output(text: str) -> tuple[str, list[str]]:
    stripped = text.strip()
    reasons: list[str] = []
    if not stripped:
        return "generation_failed", ["empty_output"]
    if "```" in stripped:
        reasons.append("markdown_fence_detected")
    lowered = stripped.lower()
    if any(marker in lowered for marker in PROSE_MARKERS):
        reasons.append("obvious_prose_marker_detected")
    first_meaningful = ""
    for raw_line in stripped.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        first_meaningful = line
        break
    if first_meaningful:
        first_lower = first_meaningful.lower()
        if not any(first_lower.startswith(keyword) for keyword in SQL_START_KEYWORDS):
            reasons.append("first_line_not_sql_like")
    else:
        reasons.append("empty_output")
    if reasons:
        return "format_violation", reasons
    return "success", []


def extract_response_text(response: Any) -> str:
    if getattr(response, "choices", None):
        message = response.choices[0].message
        content = getattr(message, "content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                text = getattr(item, "text", None)
                if text:
                    parts.append(text)
                elif isinstance(item, dict) and item.get("text"):
                    parts.append(str(item["text"]))
            return "\n".join(parts)
    return ""


def main() -> int:
    env_config = require_env()
    run_plan = load_run_plan()
    rows = load_rows()
    prompt_template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8").strip() + "\n"

    model = os.environ.get("DIRECT_LLM_MODEL", DEFAULT_MODEL)
    max_tokens = DEFAULT_MAX_TOKENS
    if isinstance(run_plan.get("model_config_to_fill_later"), dict):
        plan_max_tokens = run_plan["model_config_to_fill_later"].get("max_tokens", "")
        if str(plan_max_tokens).strip():
            max_tokens = int(plan_max_tokens)

    sanitized_base_url = sanitize_base_url(env_config["base_url"])
    run_timestamp = utc_now()
    client = OpenAI(api_key=env_config["api_key"], base_url=env_config["base_url"])

    row_results: list[dict[str, Any]] = []
    generated_output_paths: list[str] = []

    for row in rows:
        prompt = build_prompt(prompt_template, row)
        prompt_path = REPO_ROOT / row.prompt_path
        raw_response_path = REPO_ROOT / row.raw_response_path
        generated_sql_path = REPO_ROOT / row.generated_sql_path
        write_text(prompt_path, prompt)

        raw_text = ""
        api_error = ""
        status = "generation_failed"
        status_reasons: list[str] = []
        usage_prompt_tokens = None
        usage_completion_tokens = None
        usage_total_tokens = None

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=max_tokens,
            )
            raw_text = extract_response_text(response).strip()
            usage = getattr(response, "usage", None)
            if usage is not None:
                usage_prompt_tokens = getattr(usage, "prompt_tokens", None)
                usage_completion_tokens = getattr(usage, "completion_tokens", None)
                usage_total_tokens = getattr(usage, "total_tokens", None)
            status, status_reasons = classify_output(raw_text)
        except Exception as exc:
            api_error = f"{type(exc).__name__}: {exc}"
            status = "generation_failed"
            status_reasons = ["api_error"]

        write_text(raw_response_path, raw_text + ("\n" if raw_text else ""))

        generated_sql_written = False
        if status == "success":
            write_text(generated_sql_path, raw_text + "\n")
            generated_sql_written = True
            generated_output_paths.append(str(generated_sql_path.relative_to(REPO_ROOT)))

        row_results.append(
            {
                "case_id": row.case_id,
                "pool": row.pool,
                "engine": row.engine,
                "route_id": row.route_id,
                "denominator_id": row.denominator_id,
                "method_id": row.method_id,
                "source_sql_path": row.source_sql_path,
                "schema_path": row.schema_path,
                "prompt_path": row.prompt_path,
                "raw_response_path": row.raw_response_path,
                "generated_sql_path": row.generated_sql_path,
                "status": status,
                "status_reasons": status_reasons,
                "generated_sql_written": generated_sql_written,
                "response_non_empty": bool(raw_text.strip()),
                "api_error": api_error,
                "token_usage": {
                    "prompt_tokens": usage_prompt_tokens,
                    "completion_tokens": usage_completion_tokens,
                    "total_tokens": usage_total_tokens,
                },
            }
        )

    summary = {
        "planned_rows": len(rows),
        "generation_success": sum(1 for row in row_results if row["status"] == "success"),
        "format_violation": sum(1 for row in row_results if row["status"] == "format_violation"),
        "generation_failed": sum(1 for row in row_results if row["status"] == "generation_failed"),
        "generated_output_paths": generated_output_paths,
    }

    payload = {
        "run_id": RUN_ROOT.name,
        "run_scope": "direct_llm_same_engine_generation_canary",
        "run_timestamp": run_timestamp,
        "denominator_id": DENOMINATOR_ID,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "model_settings": {
            "provider": provider_from_base_url(env_config["base_url"]),
            "base_url": sanitized_base_url,
            "model": model,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": max_tokens,
            "seed_if_available": None,
        },
        "summary": summary,
        "rows": row_results,
    }
    write_text(RESULTS_PATH, json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"summary": summary, "model_used": model, "results_path": str(RESULTS_PATH.relative_to(REPO_ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
