# Status

This is a read-only Batch 2A SQLGlot same-dialect failure analysis based on the existing PostgreSQL execution report and case SQL only. No rerun, no checker pass, and no database execution was performed for this analysis.

# Input Evidence

- `reports/formal_expansion/batch2a_pg_execution_v0.json`
- `docs/_scratch/FORMAL_COMMON_CORE_BATCH2A_PG_EXECUTION_SUMMARY_v0.md`
- `cases/PERF/<CASE>/source.sql`
- `cases/PERF/<CASE>/manifest.yaml`

# Batch 2A Route Summary

- Batch 2A PERF cases: `19`
- Total Batch 2A route records: `76`
- Control-route health:
  - `NATIVE_IDENTITY`: `19/19` success
  - `HUMAN_REFERENCE_POSITIVE`: `19/19` success
  - `HARD_NEGATIVE_GUARD`: `19/19` success
- SQLGlot same-dialect:
  - `4/19` success
  - `15/19` failed

Interpretation: the Batch 2A packages and PostgreSQL validation environment look healthy. The failures are concentrated in the SQLGlot same-dialect method route.

# SQLGlot Failure Table

| case_id | failure_category | failure_stage | diagnosis | likely trigger patterns | recommended_action |
| --- | --- | --- | --- | --- | --- |
| PERF_0009 | UndefinedColumn | postgres_execution | sqlglot_alias_or_column_resolution_issue | subquery, correlated_subquery, aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0010 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | subquery, aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0011 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0012 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0014 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0015 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0016 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0018 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0019 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0020 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | subquery, aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0021 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0022 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | subquery, aggregation, date_time_expression, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0023 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | subquery, aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0025 | OptimizeError | optimize | sqlglot_optimizer_capability_boundary | subquery, correlated_subquery, aggregation, date_time_expression, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |
| PERF_0026 | UndefinedColumn | postgres_execution | sqlglot_alias_or_column_resolution_issue | subquery, correlated_subquery, aggregation, alias_resolution, column_resolution, tpc_h_pattern | split_sqlglot_optimize_vs_transpile_baseline |

# OptimizeError Cluster

- Case count: `13`
- Cases:
  - `PERF_0010`
  - `PERF_0011`
  - `PERF_0012`
  - `PERF_0014`
  - `PERF_0015`
  - `PERF_0016`
  - `PERF_0018`
  - `PERF_0019`
  - `PERF_0020`
  - `PERF_0021`
  - `PERF_0022`
  - `PERF_0023`
  - `PERF_0025`
- Stage: all `optimize`
- Signal from the existing report:
  - parse reached `success`
  - generation failed during the SQLGlot optimize path
  - the reported errors are unresolved-column optimizer exceptions such as `l_shipmode`, `p_type`, `s_acctbal`, `o_orderdate`, `ps_partkey`, `c_name`, and `s_name`

Interpretation: this cluster is best treated as a SQLGlot optimizer capability boundary under the current same-dialect optimize baseline, not as package health failure.

# UndefinedColumn Cluster

- Case count: `2`
- Cases:
  - `PERF_0009`
  - `PERF_0026`
- Stage: `postgres_execution`
- Signal from the existing report:
  - parse reached `success`
  - generation reached `success`
  - PostgreSQL then failed on invalid generated column references
- Concrete examples:
  - `PERF_0009`: generated SQL referred to `lineitem.o_orderkey`
  - `PERF_0026`: generated SQL referred to `orders.c_custkey`

Interpretation: these two failures should be separated from optimizer exceptions. They look like generated-SQL alias or column resolution faults that only surface at PostgreSQL execution time.

# Successful SQLGlot Cases

- `PERF_0007`: `row_count=1`, `runtime_ms=58`
- `PERF_0034`: `row_count=2`, `runtime_ms=60`
- `PERF_0035`: `row_count=2`, `runtime_ms=60`
- `PERF_0036`: `row_count=1`, `runtime_ms=59`

These four successes show that the same-dialect SQLGlot route is not universally broken, but its success region is narrow on this Batch 2A slice.

# Interpretation

- All three control routes passing suggests the Batch 2A case packages and PostgreSQL validation setup are sound.
- The dominant SQLGlot failure mode is optimizer-stage unresolved-column failure on a large TPC-H-heavy subset.
- The smaller secondary cluster is generated-SQL invalidity at PostgreSQL execution time, likely tied to alias or column resolution mistakes.
- The current evidence does not justify silently replacing the baseline. The safer reading is that `SQLGLOT_OPT_SAME_DIALECT` and any future no-opt or transpile fallback should be evaluated as separate method variants.

# Recommended Next Action

Run a small diagnostic dry-run that compares SQLGlot optimize against SQLGlot transpile / no-opt on the failed cases, while keeping the current optimize same-dialect baseline separate.

# Claim Boundaries

- This is an analysis from existing reports only.
- No SQL execution was performed.
- No PostgreSQL rerun was performed.
- No SQLGlot rerun or regeneration was performed.
- No checker, speedup, or plan collection was performed.
- This is not a correctness claim, speedup claim, or leaderboard update.

# Verification / Non-Modification Note

- Only this scratch analysis note was created.
- No database execution occurred.
- No model / LLM call occurred.
- No checker or speedup execution occurred.
- No registry, `docs/EXECUTION_STATUS.md`, or formal review file was changed.
- Taxonomy calibration notes were untouched.
