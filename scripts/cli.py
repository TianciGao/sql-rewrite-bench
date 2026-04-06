from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports" / "cli"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_report_dir() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def write_report(command: str, payload: dict[str, Any]) -> Path:
    ensure_report_dir()
    report_path = REPORT_DIR / f"{command}.json"
    report_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report_path


def print_and_exit(payload: dict[str, Any], exit_code: int) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


def run_subprocess(command: str, argv: list[str]) -> tuple[dict[str, Any], int]:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    payload: dict[str, Any] = {
        "command": command,
        "cwd": str(ROOT),
        "ok": completed.returncode == 0,
        "ran_at_utc": utc_now(),
        "returncode": completed.returncode,
        "stderr": completed.stderr,
        "stdout": completed.stdout,
        "subprocess_argv": argv,
    }
    report_path = write_report(command, payload)
    payload["report_path"] = str(report_path.relative_to(ROOT))
    return payload, completed.returncode


def cmd_env_check(_: argparse.Namespace) -> int:
    checks = {
        "PGHOST": bool(os.environ.get("PGHOST")),
        "MYSQL_HOST": bool(os.environ.get("MYSQL_HOST")),
        "SPARK_LOCAL_IP": bool(os.environ.get("SPARK_LOCAL_IP")),
    }
    ok = all(checks.values())
    payload: dict[str, Any] = {
        "command": "env-check",
        "cwd": str(ROOT),
        "ok": ok,
        "ran_at_utc": utc_now(),
        "visible": checks,
    }
    report_path = write_report("env-check", payload)
    payload["report_path"] = str(report_path.relative_to(ROOT))
    return print_and_exit(payload, 0 if ok else 1)


def cmd_pg_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess("pg-check", ["bash", "scripts/check_postgres.sh"])
    return print_and_exit(payload, exit_code)


def cmd_mysql_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess("mysql-check", ["bash", "scripts/check_mysql.sh"])
    return print_and_exit(payload, exit_code)


def cmd_spark_check(_: argparse.Namespace) -> int:
    payload, exit_code = run_subprocess("spark-check", [sys.executable, "scripts/smoke_spark.py"])
    return print_and_exit(payload, exit_code)


def cmd_artifact_preflight(_: argparse.Namespace) -> int:
    required_paths = [
        "benchmark_spec/benchmark_spec_v0.md",
        "benchmark_spec/case_schema_v0.1.yaml",
        "taxonomy/coverage_taxonomy_v0.1.yaml",
        "cases/PERF/PERF_0001/manifest.yaml",
        "runs/smoke_case/",
        "runs/plans/",
    ]

    checks = []
    ok = True
    for rel_path in required_paths:
        normalized = rel_path.rstrip("/")
        path = ROOT / normalized
        is_dir = rel_path.endswith("/")
        exists = path.is_dir() if is_dir else path.is_file()
        ok = ok and exists
        checks.append(
            {
                "exists": exists,
                "path": rel_path,
                "type": "directory" if is_dir else "file",
            }
        )

    payload: dict[str, Any] = {
        "checks": checks,
        "command": "artifact-preflight",
        "cwd": str(ROOT),
        "ok": ok,
        "ran_at_utc": utc_now(),
    }
    report_path = write_report("artifact-preflight", payload)
    payload["report_path"] = str(report_path.relative_to(ROOT))
    return print_and_exit(payload, 0 if ok else 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m scripts.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    env_parser = subparsers.add_parser("env-check")
    env_parser.set_defaults(func=cmd_env_check)

    pg_parser = subparsers.add_parser("pg-check")
    pg_parser.set_defaults(func=cmd_pg_check)

    mysql_parser = subparsers.add_parser("mysql-check")
    mysql_parser.set_defaults(func=cmd_mysql_check)

    spark_parser = subparsers.add_parser("spark-check")
    spark_parser.set_defaults(func=cmd_spark_check)

    artifact_parser = subparsers.add_parser("artifact-preflight")
    artifact_parser.set_defaults(func=cmd_artifact_preflight)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
