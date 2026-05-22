# Calcite HEP PG40 Generation Plan

## Scope

- `method_id = calcite_hep`
- `denominator_id = common_core_v0_40_pg40`
- `route_id = calcite_hep_pg_rewrite`
- `engine = pg`
- planned rows: `40`
- pools: `performance`, `consistency`, `portability`, `longtail`

This package is a fresh current-denominator generation packet for PostgreSQL on the frozen Common-core v0 40-case set.

It does not reuse old `prior_method_pg10`, `seed9`, or other bounded-slice numeric results as current metrics.

## Input Basis

- frozen denominator: [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)
- rerun policy: [prior_methods_rerun_policy_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_rerun_policy_v1.md)
- reusable wrapper candidate: [CalciteHepRewriteSmoke.java](/home/tianci_gao/code/sql-rewrite-bench/tools/calcite_hep/CalciteHepRewriteSmoke.java)
- reusable scaffold evidence:
  - [calcite_hep_wrapper_scaffold_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_wrapper_scaffold_v0.json)
  - [calcite_hep_real_route_canary_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/calcite_hep_real_route_canary_v0.json)

## Execution Intent

The script attempts generation on all 40 PG rows.

Interpretation rules:

- `PERF` rows are the strongest historically supported Calcite HEP family rows.
- `CONS`, `PORT`, and `LONGTAIL` rows are still included in the denominator and matrix.
- If those out-of-family rows fail, they must be reported explicitly as current-denominator failures or unsupported shapes, not silently dropped.

## Wrapper Status

Repo-local wrapper/scaffold was found:

- Java wrapper source exists at `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- prior scaffold artifacts show successful bounded parse and bounded `calcite_rel_to_sql` generation
- the package therefore treats the runner as `present_but_needing_fresh_current_denominator_execution`, not `missing`

## Planned Output Layout

- matrix: `generation_command_matrix.csv`
- runner: `run_manual_calcite_hep_pg40_generation.sh`
- summary output: `run_results.json`
- per-row generated SQL:
  - `generated/<case_id>/pg/calcite_hep_pg_rewrite.sql`
- per-row logs:
  - `logs/<case_id>_pg.stdout.log`
  - `logs/<case_id>_pg.stderr.log`
- per-row machine-readable status:
  - `row_results/<case_id>/pg/result.json`

## Status Contract

The runner should preserve these classes explicitly:

- `generation_success`
- `generation_success_noop`
- `generation_failed_parse`
- `generation_failed_unsupported_sql`
- `generation_failed_no_output`
- `generation_failed_command`
- `blocked_runner_missing`

## No-op Detection Plan

No-op detection is generation-only and does not execute SQL.

The runner will:

1. normalize source and generated SQL by trimming, collapsing whitespace, and removing a final semicolon
2. classify rows as `generation_success_noop` when normalized generated SQL matches normalized source SQL
3. keep those rows explicit in `run_results.json` rather than promoting them to successful nontrivial rewrites

## Boundaries

- no database execution
- no SQL execution
- no timing
- no speedup
- no leaderboard
- no reuse of historical bounded numeric results as current PG40 metrics
