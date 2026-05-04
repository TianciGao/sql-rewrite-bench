# Status

This is a read-only Batch 2A speedup preflight for two routes:

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

It checks only route readiness, gating evidence, validation schema readiness, and planned output paths. No SQL execution, runtime rerun, or speedup scoring was performed.

# Inputs Inspected

- `reports/formal_expansion/batch2a_pg_execution_v0.json`
- `reports/formal_expansion/batch2a_sqlglot_no_opt_checker_v0.json`
- `cases/PERF/<CASE>/source.sql`
- `cases/PERF/<CASE>/rewrite_pos_01.sql` or first `rewrite_pos_*.sql`
- `scripts/cli.py` route and validation helpers

# Current Batch 2A Scope

- PERF cases: `19`
- routes inspected: `2`
  - `HUMAN_REFERENCE_POSITIVE`
  - `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Readiness Summary

- `HUMAN_REFERENCE_POSITIVE`
  - ready: `19/19`
  - blocked: `0/19`
  - gate basis: existing PostgreSQL execution success on all 19 PERF Batch 2A cases
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - ready: `19/19`
  - blocked: `0/19`
  - gate basis: exact TSV checker consistency on all 19 PERF Batch 2A cases

Interpretation: both routes are fully eligible for the next repeat-runtime batch under the current Batch 2A slice.

# Per-Route Gating Basis

## HUMAN_REFERENCE_POSITIVE

- source SQL exists: `19/19`
- candidate SQL source available: `19/19`
- consistency gate status: `passed_existing_pg_execution`
- validation schema ready: `19/19`
- route eligibility: `eligible_for_batch2a_speedup_runtime`

## SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT

- source SQL exists: `19/19`
- candidate SQL source available: `19/19`
- consistency gate status: `passed_exact_tsv_report_local`
- validation schema ready: `19/19`
- route eligibility: `eligible_for_batch2a_speedup_runtime`

# Runtime Policy

The preflight records a runtime policy for the next step:

- repeat count proposed: `5`
- warmup count proposed: `1`
- statement timeout proposed: `30000`
- primary statistic proposed: `median`
- tie threshold proposed: `0.05`
- regression threshold proposed: `1.2`

`runtime_policy_exists=true`

# Planned Output Paths

Planned runtime observation outputs:

- `reports/formal_expansion/runtime_observation_batch2a_human_reference_positive.json`
- `reports/formal_expansion/runtime_observation_batch2a_sqlglot_transpile_same_dialect_no_opt.json`

Planned scoring outputs:

- `reports/formal_expansion/batch2a_speedup_scoring_human_reference_positive.json`
- `reports/formal_expansion/batch2a_speedup_scoring_sqlglot_transpile_same_dialect_no_opt.json`

# Recommended Next Step

Run Batch 2A repeat runtime for:

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

using the 19 PERF Batch 2A cases and the recorded runtime policy.

# Boundaries

- no SQL execution
- no runtime rerun
- no speedup computation
- no checker execution
- no LLM, MySQL, Spark, PORT, or CONS work
- not a leaderboard claim
- not a baseline replacement decision

# Verification / Non-Modification Note

- only this summary note was created
- no registry or `docs/EXECUTION_STATUS.md` changes were made
- no formal review files were changed
- taxonomy calibration notes were untouched
