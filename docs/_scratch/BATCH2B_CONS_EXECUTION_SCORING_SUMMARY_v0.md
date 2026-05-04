# Status

This note records the bounded Batch 2B CONS PostgreSQL execution and checker scoring run for:

- `CONS_0024`
- `CONS_0031`
- `CONS_0034`

Scope is PostgreSQL only and limited to:

- `NATIVE_IDENTITY`
- `HUMAN_REFERENCE_POSITIVE`
- `HARD_NEGATIVE_GUARD`

# Execution Summary

Dry-run entrypoint executed first:

- `python -m scripts.cli formal-batch2b-cons-execution-scoring`

Canary execution:

- `CONS_0024`
- all three routes executed successfully
- `source.sql` row count: `1`
- `rewrite_pos_01.sql` row count: `1`
- `rewrite_neg_01.sql` row count: `0`

Full execution result:

- cases: `3`
- routes per case: `3`
- total execution records: `9`
- successes: `9`
- failures: `0`

Per case:

- `CONS_0024`
  - native: success, row count `1`
  - positive: success, row count `1`
  - negative: success, row count `0`
- `CONS_0031`
  - native: success, row count `0`
  - positive: success, row count `0`
  - negative: success, row count `4`
- `CONS_0034`
  - native: success, row count `2`
  - positive: success, row count `2`
  - negative: success, row count `1`

# Checker Scoring Summary

Checker mode:

- `value_normalized_in_memory_from_checker_yaml`

Scoring result:

- `native_executable_rate=1.0`
- `human_positive_executable_rate=1.0`
- `hard_negative_executable_rate=1.0`
- `result_consistency_rate=1.0`
- `negative_rejection_rate=1.0`
- `false_accept_rate=0.0`

Per-case scoring:

- `CONS_0024`
  - `source_positive_equal=true`
  - `source_negative_differs=true`
- `CONS_0031`
  - `source_positive_equal=true`
  - `source_negative_differs=true`
- `CONS_0034`
  - `source_positive_equal=true`
  - `source_negative_differs=true`

# Failed Or Mismatched Cases

- none

# Boundaries

- PostgreSQL only
- consistency expansion only
- not admission
- not registry writeback
- not speedup
- not formal review update

# Recommended Next Action

- update expanded common-core results rollup with Batch 2A + Batch 2B
