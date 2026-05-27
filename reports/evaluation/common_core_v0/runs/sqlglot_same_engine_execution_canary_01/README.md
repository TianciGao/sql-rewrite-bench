# SQLGlot Same-Engine Execution Canary 01

This package is a human-run only execution canary for a narrow non-PORT SQLGlot same-engine slice.

Codex must not execute this script.

## Scope

- cases:
  - `PERF_0006`
  - `CONS_0007`
  - `LONGTAIL_0011`
- engines:
  - `pg`
  - `mysql`
  - `spark`
- routes:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`

## Boundaries

- no `PORT`
- no timing
- no leaderboard metrics
- no plan collection
- no `tmp_repo`
- no case-file modification by design

The script stages source/generated/schema/witness inputs into run-local workspaces under this run directory and executes from there.

## Outputs

The human-run script writes:

- `logs/`
- `records.tmp.jsonl`
- `run_results.json`
- run-local staged execution workspaces under `workspaces/`

This package does not produce leaderboard artifacts by itself.

Later materialization, if the human run succeeds, would be a separate step.
