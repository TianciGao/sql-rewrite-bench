# R-Bot Smoke Env Expected Artifacts

This document lists the expected artifacts from the smoke environment setup package.

It is environment recovery only.

The smoke environment intentionally keeps both PostgreSQL client package lines present:

- `psycopg` via `psycopg[binary]` for upstream `R-Bot` / `LLM4Rewrite`
- `psycopg2` via `psycopg2-binary` for existing smoke scaffolds, if needed

## Setup Artifacts

After a successful human run of
[setup_rbot_smoke_venv.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/setup_rbot_smoke_venv.sh),
the following should exist:

- smoke venv:
  `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- package snapshot:
  [smoke_env_package_snapshot.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/smoke_env_package_snapshot.txt)

## Verify Artifacts

After a successful human run of
[verify_rbot_smoke_venv.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/verify_rbot_smoke_venv.sh),
the following should exist:

- verification JSON:
  [smoke_env_verify.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/smoke_env_verify.json)

## Verification Contents

`smoke_env_verify.json` should report:

- smoke venv path
- Python executable path
- whether `smoke_env_package_snapshot.txt` exists
- import status for:
  - `chromadb`
  - `jpype`
  - `jsonlines`
  - `llama_index`
  - `psycopg`
  - `psycopg2`
  - `openai`
  - `sqlglot`
- visibility only, not values, for:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`
  - `OPENAI_API_BASE`

## Boundary

Even if all expected artifacts are present and all imports verify, actual `R-Bot` generation still remains blocked as current benchmark evidence until the separate actual-run gate is closed.
