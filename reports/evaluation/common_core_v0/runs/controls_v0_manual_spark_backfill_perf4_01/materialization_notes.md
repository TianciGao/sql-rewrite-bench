**Summary**
This package materializes the successful Spark PERF4 backfill manual run into Common-core v0 controls tables.

Scope:
- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- engine: `spark`
- routes: `native_source`, `human_positive`, `hard_negative`

Materialization rules:
- Route rows were derived from each case-local `runs/spark/result_check.json`.
- `native_source` uses the validator success plus `source.tsv` presence as engine-local control evidence.
- `human_positive` uses `checks.source_positive_equal`.
- `hard_negative` uses `checks.source_negative_different`.
- This package makes no admission or leaderboard claim.

Validation note:
- The Common-core validator is expected to pass here on schema and governance grounds.
- This package is a 4-case subset with `attempted_cases=4`, not a denominator-complete `@40` Spark run.
