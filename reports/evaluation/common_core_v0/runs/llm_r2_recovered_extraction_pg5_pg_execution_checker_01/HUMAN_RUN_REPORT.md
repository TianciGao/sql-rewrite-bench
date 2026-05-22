# LLM-R2 recovered-extraction PG5 PostgreSQL execution/checker human-run report

## Scope

Approved PG5 execution/checker only.

Approved rows:
- PERF_0017:pg
- PERF_0019:pg
- PERF_0033:pg
- PERF_0052:pg
- PERF_0054:pg

Not approved / not run:
- timing
- speedup
- MySQL/Spark
- PG40/full120
- result card / proposed row

## Result reconstruction note

PostgreSQL setup/source/generated execution completed before a Python boolean typo prevented `result_check.json` writing. The result JSON files and ledger were reconstructed from retained exit-code files and TSV outputs.

## Ledger

See `llm_r2_recovered_extraction_pg5_pg_execution_checker_ledger.csv`.

## Per-row result checks

See `workspaces/*/pg/result_check.json`.

## Governance note

These outputs are not paper-table evidence until reviewed.
