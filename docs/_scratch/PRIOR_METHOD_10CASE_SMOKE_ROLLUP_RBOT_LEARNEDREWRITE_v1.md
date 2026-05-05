# PRIOR_METHOD_10CASE_SMOKE_ROLLUP_RBOT_LEARNEDREWRITE_v1

## 0. Purpose And Boundary
This note rolls up a bounded 10-case prior-method smoke subset for `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite`. It is not leaderboard evidence, not full prior-method coverage, does not compute speedup, and does not perform registry writeback.

## 1. Denominator
Bounded 10-case denominator:
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
- base executed 3-case subset: `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md`
- expansion rationale and final denominator selection: `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_EXPANSION_PREFLIGHT_v1.md`
- Batch A execution: `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md`
- Batch B execution: `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md`

The source notes match the expected totals exactly. No discrepancy needed to be carried into this rollup.

## 2. Method-level Metrics
| method | denominator | candidate_generation_count | candidate_generation_rate@10 | candidate_execution_count | executable_rate@10 | checker_consistent_count | result_consistency_rate@10 | checker_failed_count | generation_or_method_failure_count | source_like_or_noop_count | nontrivial_checker_consistent_count | speedup_comparable_count | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | 10 | 8 | 8/10 | 8 | 8/10 | 7 | 7/10 | 1 | 2 | 0 | 7 | 7 | not_run | `bounded_10case_prior_method_smoke_subset_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | 10 | 10 | 10/10 | 10 | 10/10 | 10 | 10/10 | 0 | 0 | 8 | 2 | 2 | not_run | `bounded_10case_prior_method_smoke_subset_not_leaderboard` |

## 3. Per-case Result Table
| method | case_id | candidate_generated | candidate_executed | checker_status | consistency_status | candidate_type | failure_category | speedup_status | evidence_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | `PERF_0006` | yes | yes | inconsistent | inconsistent | `nontrivial_rewrite_candidate` | `result_mismatch_numeric_avg_precision` | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0008` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0013` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0017` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0019` | no | no | not_run | not_checked | `not_applicable` | `sql_template_generation_attribute_error` | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0024` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0033` | no | no | not_run | not_checked | `not_applicable` | `subprocess_nonzero_exit` | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0052` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0054` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `R-Bot / LLM4Rewrite` | `PERF_0063` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0006` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0008` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0013` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0017` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0019` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_A_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0024` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0033` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_3CASE_SMOKE_SUBSET_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0052` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0054` | yes | yes | consistent | consistent | `nontrivial_rewrite_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |
| `LearnedRewrite / embedded LLM4Rewrite` | `PERF_0063` | yes | yes | consistent | consistent | `source_echo_or_noop_candidate` | none | not_run | `docs/_scratch/PRIOR_METHOD_10CASE_SMOKE_BATCH_B_RBOT_LEARNEDREWRITE_v1.md` |

## 4. Interpretation
`R-Bot / LLM4Rewrite` produces more nontrivial candidates in this bounded denominator, but it also carries both generation-path risk and checker risk. It generated candidates on `8/10` cases, passed the checker on `7/10`, failed the checker once on `PERF_0006`, and failed before candidate capture twice on `PERF_0019` and `PERF_0033`.

`LearnedRewrite / embedded LLM4Rewrite` is more stable on candidate generation and checker passage in this subset: `10/10` generated, `10/10` executed, `10/10` checker-consistent. But most of that stability is source-like / no-op behavior rather than useful rewrite behavior: `8/10` candidates are explicitly classified as `source_echo_or_noop_candidate`, leaving only `2/10` checker-consistent nontrivial candidates.

Correctness-gated evaluation matters on both sides:
- `R-Bot / LLM4Rewrite` cannot carry the `PERF_0006` candidate into any speedup conversation because it is checker-inconsistent.
- `LearnedRewrite / embedded LLM4Rewrite` cannot have its `8/10` source-like / no-op candidates overclaimed as useful rewrite improvement, even though they are checker-consistent.

## 5. Metric Use
This rollup uses:
- `candidate_generation_rate@10`
- `executable_rate@10`
- `result_consistency_rate@10`
- `checker_failed_count`
- `generation_or_method_failure_count`
- `source_like_or_noop_count`
- `nontrivial_checker_consistent_count`
- `speedup_comparable_count`

This rollup does not compute:
- `gm_speedup`
- `regression_rate@20`

These are also not applicable in this bounded smoke rollup:
- cross-engine metrics
- verifier/plan/attribution support metrics

## 6. Paper-facing Wording
“On a bounded 10-case prior-method smoke subset, R-Bot / LLM4Rewrite generated nontrivial checker-consistent candidates on 7/10 cases but also showed one semantic checker failure and two generation-path failures. LearnedRewrite generated checker-consistent candidates on 10/10 cases, but 8/10 were source-like/no-op outputs. This illustrates why RewriteBench reports generation, execution, semantic consistency, and no-op behavior separately before speedup.”

## 7. Recommended Next Step
`stop and use this as bounded prior-method evidence`

Reason:
- the current project phase is consolidation rather than broad expansion
- the 10-case denominator already captures the main prior-method contrast cleanly
- any later speedup work should be explicitly approved and restricted to checker-consistent non-noop candidates

## 8. Non-Modification Note
No experiments were run for this rollup. No speedup was run. No registry, review, rules, or `docs/EXECUTION_STATUS.md` files were changed. No case files were modified. The long-standing taxonomy notes were untouched.
