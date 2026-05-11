# Table 10 Plan Attribution Preflight Recommendation V1

This is a preflight memo only. No DB/checker/timing/EXPLAIN/LLM/verifier run was performed in this step.

## What Table 5 Can Now Say

The new route-level Table 5 can safely say that the benchmark retains observability evidence beyond scalar labels:

- candidate SQL artifacts are retained for all main same-engine routes
- row-level event ledgers are retained strongly for Direct LLM and Direct LLM + Repair, and partially/route-specifically for SQLGlot and Calcite
- checker / failure artifacts are retained strongly enough to support route-level failure accounting
- timing traces are retained for the exact-timed subsets of the main routes
- plan evidence remains selected-case only
- attribution remains a separate next-step analysis

## PG Attribution Candidate Pool

- total candidates inspected: 146
- attribution-ready candidates: 113
- blocked candidates: 33
- ready candidates cover all 5 main routes:
  - direct_llm / direct_llm_same_engine_rewrite: 32
  - direct_llm / direct_llm_execute_repair_1shot: 2
  - sqlglot / sqlglot_transpile_same_dialect_noop: 26
  - sqlglot / sqlglot_optimize_same_dialect: 22
  - calcite_hep / calcite_hep_fail_closed_120: 31

## Recommended First EXPLAIN ANALYZE BUFFERS Run

Recommended size: **24 PG rows**.

Recommended candidate IDs:

- `direct_llm__direct_llm_same_engine_rewrite__PERF_0007__pg`
- `direct_llm__direct_llm_same_engine_rewrite__CONS_0012__pg`
- `direct_llm__direct_llm_same_engine_rewrite__PERF_0008__pg`
- `direct_llm__direct_llm_same_engine_rewrite__PORT_0003__pg`
- `direct_llm__direct_llm_same_engine_rewrite__CONS_0037__pg`
- `direct_llm__direct_llm_same_engine_rewrite__PERF_0034__pg`
- `direct_llm__direct_llm_execute_repair_1shot__LONGTAIL_0023__pg`
- `direct_llm__direct_llm_execute_repair_1shot__PERF_0019__pg`
- `sqlglot__sqlglot_transpile_same_dialect_noop__CONS_0005__pg`
- `sqlglot__sqlglot_transpile_same_dialect_noop__LONGTAIL_0011__pg`
- `sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0082__pg`
- `sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0017__pg`
- `sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0035__pg`
- `sqlglot__sqlglot_optimize_same_dialect__LONGTAIL_0011__pg`
- `sqlglot__sqlglot_optimize_same_dialect__LONGTAIL_0022__pg`
- `sqlglot__sqlglot_optimize_same_dialect__PERF_0082__pg`
- `sqlglot__sqlglot_optimize_same_dialect__CONS_0010__pg`
- `sqlglot__sqlglot_optimize_same_dialect__CONS_0037__pg`
- `calcite_hep__calcite_hep_fail_closed_120__PERF_0007__pg`
- `calcite_hep__calcite_hep_fail_closed_120__CONS_0011__pg`
- `calcite_hep__calcite_hep_fail_closed_120__LONGTAIL_0013__pg`
- `calcite_hep__calcite_hep_fail_closed_120__PERF_0013__pg`
- `calcite_hep__calcite_hep_fail_closed_120__PERF_0054__pg`
- `calcite_hep__calcite_hep_fail_closed_120__PERF_0024__pg`

Selection rule used here is mechanical and route-stratified:

- per route, include best speedup, worst regression, nearest neutral rows, then fill with next-best / next-worst rows
- keep the repair route limited to the 2 rows with route-specific repair timing
- keep failure-diagnostic rows out of the first exact-timed attribution run

## What Must Stay Bounded

- Do not claim full-denominator plan attribution from this preflight.
- Do not claim route-specific repair attribution for the 32 preserved original-exact PG rows inside the repair route.
- Do not merge the failure diagnostic row into the exact-timed attribution denominator.
- Do not refresh Table 10 yet; the next step should be a reviewed EXPLAIN ANALYZE BUFFERS packet first.
