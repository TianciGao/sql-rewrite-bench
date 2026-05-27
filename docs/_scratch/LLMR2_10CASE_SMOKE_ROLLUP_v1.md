# LLMR2_10CASE_SMOKE_ROLLUP_v1

## 0. Purpose And Boundary
- bounded LLM-R2 10-case smoke rollup
- not leaderboard
- not full LLM-R2 coverage
- no speedup
- no registry writeback
- no new experiment

## 1. Denominator
Shared bounded denominator from the LLM-R2 10-case expansion preflight:
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

Source of inclusion:
- `docs/_scratch/LLMR2_10CASE_EXPANSION_PREFLIGHT_v1.md`

## 2. Method-level Metrics
| method | denominator | candidate_generation_count | candidate_generation_rate@10 | clean_candidate_recovered_count | candidate_execution_count | executable_rate@10 | checker_consistent_count | result_consistency_rate@10 | checker_failed_count | generation_or_method_failure_count | logical_plan_failure_count | output_extraction_failure_count | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `LLM-R2` | `10` | `9` | `9/10` | `9` | `9` | `9/10` | `9` | `9/10` | `0` | `1` | `1` | `0` | `not_run` | `bounded_10case_LLMR2_smoke_subset_not_leaderboard` |

## 3. Per-case Result Table
| case_id | dry_run_passed | logical_plan_probe_status | candidate_generated | clean_candidate_recovered | extraction_version_used | candidate_executed | checker_status | consistency_status | failure_category | speedup_status | evidence_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_CHECKER_HANDOFF_PERF_0006_v1.md` |
| `PERF_0008` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_A_v1.md` |
| `PERF_0013` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_A_v1.md` |
| `PERF_0017` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_A_v1.md` |
| `PERF_0019` | `true` | `passed` | `yes` | `yes` | `v2` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_B_v1.md`; `docs/_scratch/LLMR2_BATCH_B_EXTRACTION_FIX_CHECKER_RERUN_v1.md` |
| `PERF_0024` | `true` | `passed` | `yes` | `yes` | `v2` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_B_v1.md`; `docs/_scratch/LLMR2_BATCH_B_EXTRACTION_FIX_CHECKER_RERUN_v1.md` |
| `PERF_0033` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_B_v1.md` |
| `PERF_0052` | `true` | `passed` | `yes` | `yes` | `v2` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_C_v1.md` |
| `PERF_0054` | `true` | `passed` | `yes` | `yes` | `v1` | `yes` | `consistent` | `consistent` | `none` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_C_v1.md` |
| `PERF_0063` | `true` | `failed` | `no` | `no` | `none` | `not_run` | `not_run` | `not_checked` | `logical_plan_probe_failed` | `not_run` | `docs/_scratch/LLMR2_10CASE_SMOKE_BATCH_C_v1.md` |

## 4. Failure / Behavior Analysis
- `9/10` cases reached candidate generation, clean candidate recovery, successful execution, and checker consistency.
- `PERF_0063` stopped at the logical-plan probe stage before LLM-R2 candidate generation. This is the single `generation_or_method_failure_count` and the single `logical_plan_failure_count`.
- `PERF_0019` and `PERF_0024` show why output extraction is a first-class artifact risk in RewriteBench. Their original checker failures were caused by extraction artifact, not by rerunning or reclassifying the method itself.
- The original Batch B extraction rule used a “last `SELECT` wins” heuristic that was unsafe for nested queries. A deterministic `v2` earliest balanced `SELECT/WITH` recovery fixed both cases without rerunning LLM-R2.
- No checker inconsistency was observed among executable clean candidates.
- No speedup was computed.

## 5. Metric Use
This bounded rollup uses:
- `candidate_generation_rate@10`
- `executable_rate@10`
- `result_consistency_rate@10`
- `logical_plan_failure_count`
- `output_extraction_failure_count`
- `speedup_status = not_run`

This rollup does not compute:
- `gm_speedup`
- `regression_rate@20`
- leaderboard rank

## 6. Paper-facing Wording
“On the bounded 10-case LLM-R2 smoke subset, LLM-R2 generated clean checker-consistent candidates on 9/10 cases after one-row fast-path staging, CPU-only execution, schema-native contracts, and deterministic output extraction. The remaining case, PERF_0063, failed at the logical-plan probe stage before candidate generation. These results are not a leaderboard or speedup result; they show how RewriteBench separates substrate integration, candidate generation, output extraction, execution, and semantic consistency.”

## 7. Recommended Next Step
- update prior-method evidence summary with LLM-R2 @10

Justification:
- The bounded denominator is now closed.
- The current highest-value follow-on is cross-method documentation alignment rather than more LLM-R2 execution.
- The source evidence is already sufficient to update the prior-method evidence summary with LLM-R2’s bounded `@10` coverage, including the `PERF_0063` logical-plan blocker and the Batch B extraction-v2 correction.

## 8. Non-Modification Note
- no experiments were run
- no speedup was run
- no registry, review, rules, or `docs/EXECUTION_STATUS.md` changes were made
- no case files were modified
- the long-standing taxonomy notes were untouched
