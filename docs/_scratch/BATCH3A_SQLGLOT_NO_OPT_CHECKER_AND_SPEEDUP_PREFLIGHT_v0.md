# Status

This is a Batch 3A formal report-local checker plus speedup preflight summary for the bounded PERF expansion slice.

It covers:

- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` exact TSV checking against source
- speedup-runtime readiness preflight for:
  - `HUMAN_REFERENCE_POSITIVE`
  - `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Why This Was Run

Batch 3A execution already showed the same SQLGlot route split seen in Batch 2A:

- `SQLGLOT_OPT_SAME_DIALECT`: `2/11` PostgreSQL execution success
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`: `11/11` PostgreSQL execution success

That made the next gating step straightforward:

- verify exact source-vs-no-opt consistency across the full 11-case slice
- verify speedup-runtime readiness for the human positive and no-opt routes

# Batch 3A Case List

- `PERF_0043`
- `PERF_0044`
- `PERF_0047`
- `PERF_0050`
- `PERF_0052`
- `PERF_0053`
- `PERF_0056`
- `PERF_0062`
- `PERF_0063`
- `PERF_0065`
- `PERF_0066`

# SQLGlot No-Opt Checker Result

- generation success: `11/11`
- generation failed: `0/11`
- source execution success: `11/11`
- candidate execution success: `11/11`
- candidate execution failed: `0/11`
- checker mode: `exact_tsv_report_local`
- checker consistent: `11/11`
- checker inconsistent: `0/11`
- checker failed: `0/11`
- result consistency rate: `1.0`
- row-count match count: `11`
- row-count mismatch count: `0`

Interpretation:

- the no-opt SQLGlot route closes exact source-vs-candidate consistency across the full Batch 3A PERF slice
- this is checker-backed route evidence, not just execution-only evidence
- this still does not justify silently replacing `SQLGLOT_OPT_SAME_DIALECT`

# Comparison To Batch 3A Optimize Route

- `SQLGLOT_OPT_SAME_DIALECT`
  - PostgreSQL execution success: `2/11`
  - PostgreSQL execution failed: `9/11`
  - failure category observed: `OptimizeError`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - generation success: `11/11`
  - PostgreSQL execution success: `11/11`
  - exact TSV consistency: `11/11`

Interpretation:

- the optimize-route capability boundary remains intact on Batch 3A
- the no-opt route again behaves like a broader executable SQLGlot baseline candidate
- the two SQLGlot routes should continue to be tracked separately

# Speedup Preflight Result

Routes inspected:

- `HUMAN_REFERENCE_POSITIVE`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

Readiness summary:

- `HUMAN_REFERENCE_POSITIVE`
  - ready: `11/11`
  - blocked: `0/11`
  - gate basis: `passed_existing_pg_execution`
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`
  - ready: `11/11`
  - blocked: `0/11`
  - gate basis: `passed_exact_tsv_report_local`

Interpretation:

- both routes are fully eligible for the next repeat-runtime step on the Batch 3A slice

# Runtime Policy

Recorded runtime policy for the next step:

- repeat count proposed: `5`
- warmup count proposed: `1`
- statement timeout proposed: `30000`
- primary statistic proposed: `median`
- tie threshold proposed: `0.05`
- regression threshold proposed: `1.2`

# Planned Output Paths

Planned runtime observation outputs:

- `reports/formal_expansion/runtime_observation_batch3a_human_reference_positive.json`
- `reports/formal_expansion/runtime_observation_batch3a_sqlglot_transpile_same_dialect_no_opt.json`

Planned scoring outputs:

- `reports/formal_expansion/batch3a_speedup_scoring_human_reference_positive.json`
- `reports/formal_expansion/batch3a_speedup_scoring_sqlglot_transpile_same_dialect_no_opt.json`

# Recommended Next Action

- run Batch 3A repeat runtime for `HUMAN_REFERENCE_POSITIVE` and `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT`

# Boundaries

- no speedup execution yet
- no speedup scoring yet
- no LLM
- no MySQL
- no Spark
- no PORT
- no CONS
- no SQLGlot optimize
- no registry update
- not a leaderboard claim
- `SQLGLOT_TRANSPILE_SAME_DIALECT_NO_OPT` remains a separate route, not a silent replacement

# Verification / Non-Modification Note

- only this scratch summary was created
- no reports were force-added
- no case-local artifacts were written
- no registry, `docs/EXECUTION_STATUS.md`, or formal review files were changed
- taxonomy calibration notes were untouched
