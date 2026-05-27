**SQLGlot Timing Preflight**

This preflight prepares a timing-bearing SQLGlot same-engine run on `common_core_v0_40` without executing any SQL and without computing speedup yet.

**Headline**
- total rows: `240`
- timing_eligible rows: `137`
- speedup_eligible rows: `137`

Eligibility rules applied:
- only `executed_success` rows are timing-eligible
- `generation_failed` rows remain explicit and excluded
- `executed_failed` rows remain explicit and excluded
- `skipped_unsupported` rows remain explicit and excluded
- `noop_generated` rows remain visible but are excluded from the speedup denominator by default

**Exclusion Counts**
- `executed_failed`: `16`
- `generation_failed`: `27`
- `noop_generated_not_executed`: `24`
- `skipped_unsupported`: `36`

**Counts By Engine**
- `mysql`: `80`
- `pg`: `80`
- `spark`: `80`

**Counts By Route**
- `sqlglot_optimize_same_dialect`: `120`
- `sqlglot_transpile_same_dialect_noop`: `120`

**Counts By Pool**
- `consistency`: `54`
- `longtail`: `36`
- `performance`: `96`
- `portability`: `54`

**Main Caveats**
- This preflight is built on execution-only SQLGlot evidence; it does not prove result consistency for method outputs yet.
- `noop_generated` same-dialect boundary rows should remain explicit but are not speedup-eligible by default.
- PORT rows with execution success stay timing-eligible only with portability-stress caveat framing preserved.
- Performance metrics in the readiness matrix remain `not ready` until a real timing-bearing run is materialized and validated.
- No `GM_Speedup`, `RegressionRate@20%`, or `same_engine_leaderboard.csv` is created in this step.
