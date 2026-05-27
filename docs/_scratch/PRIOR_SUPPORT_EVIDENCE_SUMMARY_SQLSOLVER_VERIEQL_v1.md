# PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1

## 0. Purpose And Boundary
State:
- prior-support evidence summary only
- support/verifier evidence only
- not rewrite generation
- not speedup
- not leaderboard
- no new experiment

## 1. Current Support Coverage Snapshot
| support_tool | substrate_status | denominator | support_scope | positive_support | negative_support | unknown_or_unsupported | unexpected_verdict | verifier_support_rate | speedup_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SQLSolver` | `public repo acquired, tmp build complete, bounded support smoke executed` | `4 query pairs across CONS_0007 / CONS_0035` | `equivalence/refutation support smoke` | `1/2 expected positive pairs supported` | `2/2 expected negative pairs supported` | `0` | `1` | `3/4` | `not_run` | `bounded_sqlsolver_support_smoke_not_rewrite_not_leaderboard` |
| `VeriEQL` | `staged runtime path exists, support-canary and readiness evidence only` | `availability/readiness plus bounded 1-case canary on CONS_0035` | `support-canary / availability / constraint-sensitive verifier evidence` | `0/1 bounded positive canary support under empty constraints; constrained retry timed out` | `1/1 bounded negative canary refutation evidence` | `0 in executed canary; broader readiness still subset-limited` | `1 bounded positive canary caveat under empty-constraint policy` | `not_final_support_table` | `not_run` | `verieql_support_canary_availability_only_not_rewrite_not_leaderboard` |

## 2. SQLSolver Interpretation
SQLSolver is a verifier/support baseline, not a rewrite-generation line. The public upstream repo was acquired, its Apache 2.0 license was visible, a jar was built in `/tmp`, and the runner dry-run with the built jar passed before bounded support execution.

On the bounded `CONS_0007` / `CONS_0035` smoke, SQLSolver produced expected support on `3/4` pairs. `CONS_0007` was fully supported on both the positive and negative pair. `CONS_0035` negative was supported as a refuted-equivalence pair, while `CONS_0035` positive returned an unexpected `NEQ` verdict. This is verifier behavior evidence, not rewrite failure evidence and not speedup evidence.

## 3. VeriEQL Interpretation
In this project, a support-canary means a narrowly scoped verifier/support probe used to establish whether a staged verifier path can reach meaningful verdicts on a bounded case without claiming broad support coverage. VeriEQL is treated in that role rather than as a rewrite generator or speedup baseline.

The available evidence is mixed but concrete. Project decisions already treat VeriEQL as a consistency supplement source, and the readiness audit records it as a `support_only` verifier line with subset limitations and missing local wrapper/constraint-bridge policy. Later notes show a staged runtime path under `datasets/raw/verieql/staged/VeriEQL/`, a bounded `CONS_0035` module-mode canary that reached verdict stage, and a follow-up interpretation note explaining that the positive pair is constraint-sensitive rather than a clean proof failure. Under empty constraints, VeriEQL refuted both pairs on `CONS_0035`; with a bounded uniqueness bridge, the negative pair still refuted while the positive pair timed out instead of proving. That makes the current VeriEQL evidence support-canary / availability evidence with caveat, not a clean executed support-table denominator comparable to SQLSolver’s `4`-pair smoke.

What remains missing is broader runnable wrapper coverage, a stable constraint-bridge policy, and a finalized bounded support-table contract across multiple cases. For that reason, VeriEQL should still be described as runnable in a narrow canary sense but support-limited and not yet suitable for stronger coverage claims.

## 4. Shared Support Metrics
Use:
- `verifier_support_rate`
- `prove_count`
- `refute_count`
- `unknown_count`
- `timeout_count`
- `unsupported_count`
- `parser_or_translation_failure_count`
- `internal_error_count`
- `unexpected_verdict_count`

Explicitly out of scope:
- `candidate_generation_rate` for rewrite methods
- `gm_speedup`
- `regression_rate@20`
- `W/T/L`
- rewrite leaderboard rank

## 5. Relationship To Rewrite-method Evidence
SQLSolver and VeriEQL should live in prior-support evidence, separate from R-Bot / LearnedRewrite / LLM-R2 rewrite-method evidence.

They evaluate verifier/support coverage, not rewrite generation quality. They can support benchmark artifact trustworthiness and semantic-stress analysis, but they cannot be ranked against rewrite generators.

## 6. Paper-facing Wording
“Separate from rewrite-generation baselines, we evaluated support/verifier substrates. SQLSolver was acquired, built, and run on a bounded four-pair CONS support smoke, yielding expected support on 3/4 pairs and one unexpected verdict on a positive equivalence pair. VeriEQL remains treated as support-canary / availability evidence rather than a rewrite or speedup baseline. These results contribute to RewriteBench’s artifact-support story, not to the rewrite-method leaderboard.”

## 7. Recommended Next Step
- `add this support evidence to paper/RQ narrative`

## 8. Non-Modification Note
Confirm no experiments were run and no repo state changed except this note.
