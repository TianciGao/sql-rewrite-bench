# PRIOR_METHOD_EVIDENCE_SUMMARY_RBOT_LEARNEDREWRITE_LLMR2_v1

## 0. Purpose And Boundary
This note is a prior-method evidence summary only. It is not leaderboard evidence, not full prior-method coverage, runs no new experiment, does not compute speedup, and does not perform registry writeback.

## 1. Current Coverage Snapshot
| method | substrate_status | denominator | candidate_generation | candidate_execution | checker_consistency | nontrivial_checker_consistent | source_like_or_noop | failures | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-Bot / LLM4Rewrite` | integrated bounded external path | 10 | 8/10 | 8/10 | 7/10 | 7/10 | 0/10 | 1 checker failure + 2 generation/path failures | not_run | `bounded_10case_prior_method_smoke_subset_not_leaderboard` |
| `LearnedRewrite / embedded LLM4Rewrite` | integrated embedded path | 10 | 10/10 | 10/10 | 10/10 | 2/10 | 8/10 | 0 checker failures, but mostly no-op/source-like behavior | not_run | `bounded_10case_prior_method_smoke_subset_not_leaderboard` |
| `LLM-R2` | official repo acquired, adapter-heavy one-case path | 1 | 1/1 | 1/1 | 1/1 | 1/1 | not_observed | many adapter/runtime blockers resolved before success | not_run | `bounded_1_case_LLMR2_checker_smoke_not_speedup_not_leaderboard` |

Coverage note:
- the source notes match the expected `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite` 10-case totals exactly
- `LLM-R2` is intentionally not placed on the same denominator; current evidence is bounded to `PERF_0006` only
- for `LLM-R2`, the checker-backed candidate is classified as `clean_extracted_candidate`

## 2. Method-by-method Interpretation

### R-Bot / LLM4Rewrite
`R-Bot / LLM4Rewrite` currently provides the strongest bounded signal for nontrivial candidate generation among the integrated prior methods. On the bounded 10-case subset it produced `7/10` checker-consistent nontrivial candidates, which is materially different from a source-like fallback path. At the same time, the method carries both integration-path risk and correctness risk: two cases failed before candidate capture, and `PERF_0006` produced an executable candidate that failed semantic checking due to average/decimal drift. This is useful benchmark evidence precisely because it shows that executable-looking rewrites can still be semantically wrong. No speedup was run.

### LearnedRewrite / embedded LLM4Rewrite
`LearnedRewrite / embedded LLM4Rewrite` is the most stable method on bounded generation and checker passage in the current 10-case subset: `10/10` generated, `10/10` executed, and `10/10` checker-consistent. But that stability is not the same thing as useful rewrite behavior. `8/10` outputs are explicitly source-like / no-op, leaving only `2/10` nontrivial checker-consistent cases. RewriteBench therefore treats the method as correctness-preserving on this bounded subset, while also making clear that correctness alone does not imply meaningful rewrite improvement. No speedup was run.

### LLM-R2
`LLM-R2` now has official-repo acquisition plus a bounded 1-case integrated path on `PERF_0006`. Reaching that point required substantial adapter work: one-row fast path staging, CPU-only execution, schema-native contract alignment, and output SQL extraction cleanup before checker handoff. After that bounded cleanup, a clean extracted candidate passed the PostgreSQL checker on `PERF_0006`. This is useful checker-backed evidence, but it is still only `1/1` coverage and should not be compared directly against the 10-case denominators used for `R-Bot / LLM4Rewrite` and `LearnedRewrite / embedded LLM4Rewrite`. No speedup was run.

## 3. Cross-method Behavioral Contrast
| behavior | R-Bot | LearnedRewrite | LLM-R2 | RewriteBench value exposed |
| --- | --- | --- | --- | --- |
| nontrivial checker-consistent candidate | yes, `7/10` on the bounded 10-case subset | yes, but only `2/10` | yes, `1/1` on bounded `PERF_0006` evidence | separates useful-looking rewrite success from mere execution |
| nontrivial checker-failed candidate | yes, `PERF_0006` | not observed in the current bounded subset | not observed in current bounded evidence | exposes semantic correctness risk even when SQL executes |
| source-like/no-op checker-consistent candidate | not observed in the current bounded subset | dominant behavior, `8/10` | not observed | prevents overclaiming no-op outputs as rewrite improvement |
| generation/path failure | yes, two bounded 10-case failures | not observed in the bounded 10-case subset | yes, multiple bounded adapter/runtime blockers before the final successful path | exposes integration and substrate fragility separately from semantic quality |
| adapter-heavy clean candidate recovery | no | no | yes, after one-row fast path, CPU-only, schema-native contract, and extraction cleanup | shows output extraction and substrate contract risk before checker-backed success |

This contrast is the main benchmark value of the current evidence:
- `R-Bot / LLM4Rewrite` exposes correctness risk
- `LearnedRewrite / embedded LLM4Rewrite` exposes no-op/source-like fallback behavior
- `LLM-R2` exposes adapter complexity and extraction risk before checker-backed success
- RewriteBench keeps these behaviors separate instead of collapsing them into a single “method works” label

## 4. Metric Use
This summary uses the following metric families as bounded evidence:
- `candidate_generation_rate` as integration/smoke support evidence
- `executable_rate` as bounded prior-method smoke support
- `result_consistency_rate` as checker-backed validity evidence
- `source_like_or_noop_count` to avoid overclaiming checker-consistent no-op behavior

This summary does not compute:
- `gm_speedup`
- `regression_rate@20`

These are also not applicable here:
- cross-engine metrics
- verifier/plan/attribution metrics

## 5. Paper-facing Wording
Safe wording:

“On a bounded 10-case prior-method smoke subset, R-Bot / LLM4Rewrite generated nontrivial checker-consistent candidates on 7/10 cases but also showed one semantic checker failure and two generation-path failures. LearnedRewrite generated checker-consistent candidates on 10/10 cases, but 8/10 were source-like/no-op outputs. LLM-R2 was additionally integrated to a bounded one-case checker-backed smoke after one-row fast-path, schema-contract, CPU-only, and output-extraction cleanup. These results are not a leaderboard; they show why RewriteBench reports candidate generation, execution, semantic consistency, no-op behavior, and speedup eligibility separately.”

Forbidden wording:
- R-Bot beats LearnedRewrite
- LearnedRewrite beats R-Bot
- LLM-R2 beats either method
- full prior-method leaderboard
- full prior-method coverage
- speedup result
- final ranking

## 6. Recommended Next Step
`stop and use this as bounded prior-method evidence`

Reason:
- the current project phase is consolidation rather than broad prior-method expansion
- the existing evidence already captures the important behavioral split across the three methods
- `LLM-R2` now has a real bounded checker-backed anchor without yet justifying broader denominator expansion
- any speedup work should happen only for checker-consistent non-noop candidates and only after explicit approval

## 7. Non-Modification Note
No experiments were run for this note. No repo state changed except this note.
