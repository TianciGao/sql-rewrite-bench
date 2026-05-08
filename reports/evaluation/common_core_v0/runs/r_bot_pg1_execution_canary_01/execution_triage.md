# R-Bot PG1 Execution/Validity Canary Triage

## Scope

This is a read-only triage of `r_bot_pg1_execution_canary_01` against the existing canary artifacts and `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`.

It does not upgrade any benchmark status, does not create timing evidence, and does not create leaderboard evidence.

## Inputs Read

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/result_check.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/source.tsv`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/generated.tsv`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/logs/*.log`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`
- `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`

## Observed Facts

- planned rows: `1`
- executed rows: `1`
- execution_failed rows: `0`
- match_exact rows: `1`
- mismatch rows: `0`
- claim_boundary: `exploratory_smoke_only_not_current_common_core_metric_evidence`
- current_benchmark_metric_evidence: `false`
- result_check status: `match_exact`

Artifact paths:

- source TSV: `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/source.tsv`
- generated TSV: `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/generated.tsv`
- result check: `reports/evaluation/common_core_v0/runs/r_bot_pg1_execution_canary_01/workspaces/PERF_0006/pg/r_bot_pg_rewrite/result_check.json`
- retained generated SQL from recovery canary: `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`

Execution/log observations:

- The execution canary recorded `execution_status_observed=executed`.
- The result checker recorded `exact_match=true` and `consistency_check_status=match_exact`.
- `source.tsv` and `generated.tsv` contain the same two result rows.
- The PG preflight recorded `returncode=0`.
- The execution row used retained recovery SQL without modification, matching the run notes.

## Triage Judgment

The canary closes the narrow question of whether the retained PG recovery SQL for `PERF_0006` can be executed once and produce an exact result match in the current local path. On that narrow question, the answer is yes.

This does **not** convert the packet into current Common-core benchmark metric evidence. The run manifest itself marks the packet as `exploratory_smoke_only_not_current_common_core_metric_evidence`, and the protocol allows no upgrade from a one-row exploratory validity canary to denominator-grade benchmark reporting.

## Decision Fields

- `planned_rows = 1`
- `executed_rows = 1`
- `execution_failed_rows = 0`
- `match_exact_rows = 1`
- `mismatch_rows = 0`
- `result_check_status = match_exact`
- `claim_boundary = exploratory_smoke_only_not_current_common_core_metric_evidence`
- `current_benchmark_metric_evidence = false`
- `pg1_timing_can_be_attempted_as_exploratory_evidence = no`
- `pg3_expansion_recommended = no`

## Why Timing Is Not Yet Greenlit

The single-row execution/match canary removes the specific historical mismatch concern for this retained SQL on `PERF_0006`, but the repository evidence still does not support timing yet:

- `r_bot_pg1_recovery_canary_01/run_results.json` still records `current_benchmark_gate_ready=false`, `exploratory_actual_run_allowed=false`, and `dry_run_can_execute_next=false`.
- The prior-method candidate matrix for `r_bot,PERF_0006,performance,pg` still says: restore retrieval/control stack and rerun before any timing.
- The evaluation protocol and current ledger both separate validity/execution evidence from timing/speedup evidence.

Therefore the correct read is: the canary is useful exploratory validity evidence, but PG1 timing should not yet be attempted from this packet alone.

## Why PG3 Expansion Is Not Recommended

- This packet covers only one PG row and one case.
- The evidence boundary remains exploratory-only.
- The repository currently treats R-Bot prior-method evidence as bounded PG-only evidence and warns against broader extension without explicit stack recovery and evaluation design work.
- The current project phase is consolidation and governance hardening, not automatic expansion from a one-row canary.

Accordingly, PG3 expansion is not recommended on the basis of this artifact alone.

## What Remains Required Before Current Benchmark Metric Evidence

1. Restore a runnable repo-local R-Bot retrieval/control stack rather than relying on retained recovery output only.
2. Clear the current recovery-gate blockers recorded in `r_bot_pg1_recovery_canary_01/run_results.json`, including `current_benchmark_gate_ready=false` and `exploratory_actual_run_allowed=false`.
3. Materialize fresh denominator-aware method-run artifacts, not just a retained one-row execution replay.
4. Produce timing-bearing same-engine method packages with explicit validity/exclusion bookkeeping before any timing or speedup claim.
5. Rerun beyond the single-row canary on an explicitly approved bounded PG overlap slice before considering any broader benchmark interpretation.

## Bottom Line

`PERF_0006` PG retained-sql execution canary is successful as a one-row exploratory validity smoke. It is not current Common-core metric evidence, it does not justify timing yet, and it does not justify PG3 expansion yet.
