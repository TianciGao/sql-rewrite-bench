# Status

This note records the bounded Batch 3B PERF PostgreSQL execution/scoring pass for the four paper-draft execution candidates.

# Case List

- `PERF_0027`
- `PERF_0028`
- `PERF_0030`
- `PERF_0031`

# Paper-Draft Override Basis

Execution used the paper-draft gate documented in `docs/_scratch/BATCH3B_PERF_REGISTRY_GATE_DECISION_v0.md`.

That override permits bounded PostgreSQL execution/scoring for these four cases without changing registry staging fields.

# Execution Summary

- total cases: `4`
- routes: `5`
- total execution records: `20`
- executed: `20`
- success: `17`
- failed: `3`
- skipped: `0`

Per-route execution:

- `NATIVE_IDENTITY`: `4/4` success
- `HUMAN_REFERENCE_POSITIVE`: `4/4` success
- `HARD_NEGATIVE_GUARD`: `4/4` success
- `SQLGLOT_OPT_SAME_DIALECT`: `1/4` success, `3/4` failed
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `4/4` success

Control scoring reused `checker.yaml` normalization in memory:

- source vs positive equal: `4/4`
- source vs negative differs: `4/4`
- false accept count: `0`
- checker mode: `value_normalized_in_memory_from_checker_yaml`

# SQLGlot Optimize Result

`SQLGLOT_OPT_SAME_DIALECT` again exposed the optimizer capability boundary.

- success: `1/4`
- failed: `3/4`
- failure category: `OptimizeError`
- failed cases:
  - `PERF_0027`
  - `PERF_0028`
  - `PERF_0030`

This keeps the same interpretation as Batch 2A and Batch 3A: optimize-route failures are method-boundary evidence, not package-health failure.

# SQLGlot No-Opt Checker Result

`SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` executed successfully on all four cases and remained exact-TSV consistent against source in the bounded in-memory checker pass.

- generation success: `4/4`
- source execution success: `4/4`
- candidate execution success: `4/4`
- checker consistent: `4/4`
- checker inconsistent: `0/4`
- checker failed: `0/4`
- `ResultConsistencyRate=1.0`
- row-count matches: `4/4`
- checker mode: `exact_tsv_in_memory`

# Speedup Preflight Result

No speedup repeats were run here. This step only checked readiness for the two routes allowed into the next runtime stage.

- `HUMAN_REFERENCE_POSITIVE`: ready `4/4`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: ready `4/4`

Frozen runtime policy remains:

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

# Failed Cases

- `PERF_0027`
  - route: `SQLGLOT_OPT_SAME_DIALECT`
  - category: `OptimizeError`
- `PERF_0028`
  - route: `SQLGLOT_OPT_SAME_DIALECT`
  - category: `OptimizeError`
- `PERF_0030`
  - route: `SQLGLOT_OPT_SAME_DIALECT`
  - category: `OptimizeError`

No control-route failures occurred.

No `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` checker inconsistency occurred.

# Boundaries

- paper-draft evidence only
- registry unchanged
- not admission
- not final common-core inclusion
- not final denominator
- PostgreSQL only
- not speedup run yet
- no LLM
- no MySQL
- no Spark
- no PORT
- no CONS

# Recommended Next Action

- run Batch 3B speedup for `HUMAN_REFERENCE_POSITIVE` and `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
