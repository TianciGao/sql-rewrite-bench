# R-Bot Smoke Env Setup Plan

This package prepares a smoke-scoped Python environment for the `R-Bot` `PERF_0006 / pg` recovery canary.

It is environment recovery only.
It is not method execution.
It is not API execution.
It is not current benchmark evidence.

## Scope

- `method_id = r_bot`
- `route_id = r_bot_pg_rewrite`
- `case_id = PERF_0006`
- preferred smoke venv path:
  `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`

## Goal

Make the canary technically runnable at the Python-environment layer by:

1. creating or reusing a smoke-scoped venv
2. installing the smoke requirements from:
   [r_bot_recovery_requirements.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_recovery_requirements.txt)
3. snapshotting the installed packages
4. verifying the required imports and environment-variable visibility

The smoke dependency surface intentionally includes both PostgreSQL client lines:

- `psycopg` via `psycopg[binary]` for upstream `R-Bot` / `LLM4Rewrite`
- `psycopg2` via `psycopg2-binary` for existing smoke scaffolds, if needed

## Files In This Package

- [setup_rbot_smoke_venv.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/setup_rbot_smoke_venv.sh)
- [verify_rbot_smoke_venv.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/verify_rbot_smoke_venv.sh)
- [r_bot_smoke_env_expected_artifacts.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_smoke_env_expected_artifacts.md)

## Setup Script Responsibilities

The setup script is human-run only and should:

- create or reuse `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- upgrade `pip`
- install the smoke requirements
- write a package snapshot to:
  `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/smoke_env_package_snapshot.txt`

It must not:

- run `R-Bot`
- call an API
- execute SQL

## Verify Script Responsibilities

The verify script is human-run only and should:

- activate the smoke venv
- check imports:
  - `chromadb`
  - `jpype`
  - `jsonlines`
  - `llama_index`
  - `psycopg`
  - `psycopg2`
  - `openai`
  - `sqlglot`
- check whether these environment variables are visible without printing values:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`
  - `OPENAI_API_BASE`
- write machine-readable verification output to:
  `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/smoke_env_verify.json`

## Boundary

Even after human setup and verification succeed, actual `R-Bot` generation remains blocked as current benchmark evidence by:

- substrate retention gaps
- demo-policy/runtime logging gaps
- contamination-guard attestation gaps
- actual-run artifact-contract gaps

At best, successful environment setup closes only the Python dependency blocker.
