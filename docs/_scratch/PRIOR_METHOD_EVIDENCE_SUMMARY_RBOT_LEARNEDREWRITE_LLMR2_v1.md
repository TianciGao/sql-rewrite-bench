# PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1

## 0. Purpose And Boundary
This note is a prior-method evidence summary only. It is not leaderboard evidence, not full prior-method coverage, runs no new experiment, and does not perform registry writeback.

## 1. Current Coverage Snapshot
| method | substrate_status | denominator | candidate_generation | candidate_execution | checker_consistency | nontrivial_checker_consistent | source_like_or_noop | failures | speedup_eligible_denominator | pg_witness_scale_gm_speedup | pg_witness_scale_w_t_l | pg_witness_scale_regression@20 | speedup_status | claim_boundary | speedup_claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | integrated bounded external path | 10 | 8/10 | 8/10 | 7/10 | 7/10 | 0/10 | 1 checker failure + 2 generation/path failures | 7 | 0.8804340264675553 | 0/2/5 | 2 | measured_for_correctness_gated_pg_only_witness_scale_slice | `bounded_10case_prior_method_smoke_subset_not_leaderboard` | `bounded_pg_only_rbot_speedup_slice_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | integrated embedded path | 10 | 10/10 | 10/10 | 10/10 | 2/10 | 8/10 | 0 checker failures, but mostly no-op/source-like behavior | 2 | 0.6295872209675301 | 0/0/2 | 2 | measured_for_correctness_gated_pg_only_witness_scale_slice | `bounded_10case_prior_method_smoke_subset_not_leaderboard` | `bounded_pg_only_learnedrewrite_speedup_slice_not_leaderboard` |
| `LLM-R2` | official repo acquired, adapter-heavy bounded 10-case path | 10 | 9/10 | 9/10 | 9/10 | 9/10 | not_observed | 1 logical-plan-stage failure, 0 checker failures | 9 | 0.9592371433387649 | 1/6/2 | 1 | measured_for_correctness_gated_pg_only_witness_scale_slice | `bounded_10case_LLMR2_smoke_subset_not_leaderboard` | `bounded_pg_only_llmr2_speedup_slice_not_leaderboard` |

Coverage note:
- the source notes match the expected `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite` 10-case totals exactly
- `LLM-R2` is now on the same bounded denominator size as `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite`
- for `LLM-R2`, the checker-backed successful cases are classified as `clean_extracted_candidate`

## 2. Method-by-method Interpretation

### R-Bot / LLM4Rewrite
`R-Bot / LLM4Rewrite` currently provides the strongest bounded signal for nontrivial candidate generation among the integrated prior methods. On the bounded 10-case subset it produced `7/10` checker-consistent nontrivial candidates, which is materially different from a source-like fallback path. At the same time, the method carries both integration-path risk and correctness risk: two cases failed before candidate capture, and `PERF_0006` produced an executable candidate that failed semantic checking due to average/decimal drift. This is useful benchmark evidence precisely because it shows that executable-looking rewrites can still be semantically wrong. After correctness gating, its PG-only witness-scale speedup slice had eligible denominator `7`, `gm_speedup = 0.8804340264675553`, win/tie/loss `0/2/5`, and `regression_count@20 = 2`. The method generated nontrivial checker-consistent candidates, but none produced a win in the bounded witness-scale speedup slice.

### LearnedRewrite / embedded LLM4Rewrite
`LearnedRewrite / embedded LLM4Rewrite` is the most stable method on bounded generation and checker passage in the current 10-case subset: `10/10` generated, `10/10` executed, and `10/10` checker-consistent. But that stability is not the same thing as useful rewrite behavior. `8/10` outputs are explicitly source-like / no-op, leaving only `2/10` nontrivial checker-consistent cases. RewriteBench therefore treats the method as correctness-preserving on this bounded subset, while also making clear that correctness alone does not imply meaningful rewrite improvement. After correctness gating, only those `2` non-noop candidates entered primary PG-only speedup, and both regressed, giving `gm_speedup = 0.6295872209675301`, win/tie/loss `0/0/2`, and `regression_count@20 = 2`.

### LLM-R2
`LLM-R2` now has official-repo acquisition plus a bounded 10-case integrated path on the same denominator used for the other prior-method smoke subsets. Reaching that point required substantial adapter work: one-row fast path staging, CPU-only execution, schema-native contract alignment, deterministic output extraction cleanup, and a `v2` earliest balanced `SELECT/WITH` recovery path for nested-query cases. On this bounded denominator, `LLM-R2` generated checker-consistent clean extracted candidates on `9/10` cases. The remaining case, `PERF_0063`, failed at the logical-plan probe stage before candidate generation. This is useful checker-backed evidence on a shared denominator, but it is still bounded smoke evidence rather than full method coverage. After correctness gating, the PG-only witness-scale speedup slice had eligible denominator `9`, `gm_speedup = 0.9592371433387649`, win/tie/loss `1/6/2`, and `regression_count@20 = 1`. `LLM-R2` produced mostly ties, one win, and two losses; `gm_speedup` remained below `1`.

## 3. Cross-method Behavioral Contrast
| behavior | R-Bot | LearnedRewrite | LLM-R2 | RewriteBench value exposed |
| --- | --- | --- | --- | --- |
| nontrivial checker-consistent candidate | yes, `7/10` on the bounded 10-case subset | yes, but only `2/10` | yes, `9/10` clean extracted checker-consistent on the bounded 10-case subset | separates useful-looking rewrite success from mere execution |
| nontrivial checker-failed candidate | yes, `PERF_0006` | not observed in the current bounded subset | not observed in current bounded evidence | exposes semantic correctness risk even when SQL executes |
| source-like/no-op checker-consistent candidate | not observed in the current bounded subset | dominant behavior, `8/10` | not observed | prevents overclaiming no-op outputs as rewrite improvement |
| generation/path failure | yes, two bounded 10-case failures | not observed in the bounded 10-case subset | yes, one logical-plan-stage failure on `PERF_0063` before candidate generation | exposes integration and substrate fragility separately from semantic quality |
| adapter-heavy clean candidate recovery | no | no | yes, after one-row fast path, CPU-only, schema-native contract, deterministic extraction cleanup, and `v2` nested-query recovery | shows output extraction and substrate contract risk before checker-backed success |

This contrast is the main benchmark value of the current evidence:
- `R-Bot / LLM4Rewrite` exposes correctness risk
- `LearnedRewrite / embedded LLM4Rewrite` exposes no-op/source-like fallback behavior
- `LLM-R2` exposes adapter complexity, logical-plan fragility, and extraction risk before checker-backed success
- RewriteBench keeps these behaviors separate instead of collapsing them into a single “method works” label

## 4. Prior-method PG-only Speedup Slice

This section summarizes the completed correctness-gated PG-only speedup slice.

- speedup was correctness-gated
- only checker-consistent non-noop candidates were included
- `SQLSolver / VeriEQL` are excluded because they are support/verifier baselines
- this is PG-only
- this is witness-scale / sub-ms or near-sub-ms
- this is not final leaderboard
- this is not cross-engine transfer
- this is not production-scale performance evidence

| method | original_10case_denominator | eligible_speedup_denominator | valid_measured_count | gm_speedup | win/tie/loss | regression_count@20 | speedup_status |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `R-Bot / LLM4Rewrite` | `10` | `7` | `7` | `0.8804340264675553` | `0/2/5` | `2` | `measured_for_correctness_gated_pg_only_witness_scale_slice` |
| `LLM-R2` | `10` | `9` | `9` | `0.9592371433387649` | `1/6/2` | `1` | `measured_for_correctness_gated_pg_only_witness_scale_slice` |
| `LearnedRewrite / embedded LLM4Rewrite` | `10` | `2` | `2` | `0.6295872209675301` | `0/0/2` | `2` | `measured_for_correctness_gated_pg_only_witness_scale_slice` |

Interpretation:
- `R-Bot / LLM4Rewrite` generated nontrivial checker-consistent candidates, but none produced a win in the bounded witness-scale speedup slice.
- `LLM-R2` produced mostly ties, one win, and two losses; `gm_speedup` remains below `1`.
- `LearnedRewrite / embedded LLM4Rewrite` had only two non-noop candidates eligible for primary speedup, and both regressed.
- Overall: semantic consistency and nontrivial candidate generation do not guarantee even witness-scale speedup.

## 5. Metric Use
This summary uses the following metric families as bounded evidence:
- `candidate_generation_rate` as integration/smoke support evidence
- `executable_rate` as bounded prior-method smoke support
- `result_consistency_rate` as checker-backed validity evidence
- `source_like_or_noop_count` to avoid overclaiming checker-consistent no-op behavior
- `gm_speedup`, `win/tie/loss`, and `regression_count@20` for the correctness-gated PG-only witness-scale slice

These are also not applicable here:
- cross-engine metrics
- verifier/plan/attribution metrics

## 6. Paper-facing Wording
Safe wording:

“On a shared bounded 10-case prior-method smoke subset, R-Bot / LLM4Rewrite generated nontrivial checker-consistent candidates on 7/10 cases but also showed one semantic checker failure and two generation-path failures. LearnedRewrite generated checker-consistent candidates on 10/10 cases, but 8/10 were source-like/no-op outputs. LLM-R2 generated clean checker-consistent candidates on 9/10 cases after one-row fast-path, CPU-only, schema-contract, and output-extraction cleanup, with one logical-plan-stage failure. These results are not a leaderboard or speedup result; they show why RewriteBench reports candidate generation, execution, semantic consistency, no-op behavior, output extraction, and speedup eligibility separately.”

“After semantic gating, we additionally measured a PG-only witness-scale speedup slice for non-noop candidates. R-Bot / LLM4Rewrite had 0 wins over 7 eligible candidates, LLM-R2 had 1 win over 9 eligible candidates, and LearnedRewrite’s two eligible non-noop candidates both regressed. These measurements are not a final performance leaderboard or production-scale result; they show that checker consistency and nontrivial candidate generation do not guarantee even witness-scale runtime improvement.”

Forbidden wording:
- R-Bot beats LearnedRewrite
- LearnedRewrite beats R-Bot
- LLM-R2 beats either method
- full prior-method leaderboard
- full prior-method coverage
- production-scale speedup
- cross-engine transfer
- full benchmark speedup result
- final ranking

## 7. Recommended Next Step
`create baseline evidence matrix`

Reason:
- rewrite prior-method smoke + speedup slice is now summarized
- support/verifier summary also exists
- the next gap is cross-baseline visibility across rewrite, support, portability, and blocked methods

## 8. Non-Modification Note
No experiments were run for this note. No repo state changed except this note.
