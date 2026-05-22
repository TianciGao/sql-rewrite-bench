# Common-core v0 Paper Results README v3

这是一次 **SQLGlot-only** 的 paper-facing refresh，基于保留的 checker backfill 和 route-separated per-case timing packet。

## What This Package Is

- 一个面向论文写作的 retained-artifact synthesis
- 一个 denominator-aware evidence ledger
- 一个把 SQLGlot 从 aggregate-only timing 更新到 route-separated per-case timing 的版本

## What It Is Not

- 不是 final ranked leaderboard
- 不是新的 SQLGlot generation run
- 不是新的 checker/timing execution in this refresh step
- 不是 `sqlglot_combined_same_engine_240` 升级为主方法行

## Reading Order

1. `table3_same_engine_method_evidence_v3.csv`
2. `table6_performance_on_exact_timed_rows_v4.csv`
3. `table7_failure_accounting_matrix_v3.csv`
4. `table11_bounded_pilot_evidence_reuse_v3.csv`
5. `paper_claim_matrix_v3.csv`
6. `paper_safe_claims_and_boundaries_v3.md`
7. `paper_remaining_experiment_gaps_v3.csv`

## Current SQLGlot Highlights

- no-op route: exact72 / timed72 / GM speedup `1.000145903000493`
- optimize route: revised exact63 / timed63 / GM speedup `0.9907164888740984`
- optimize route no longer uses the old aggregate 65 as the paper-safe timing denominator
- the two optimize checker_failed rows remain visible and excluded from timing

## Claim Boundaries

- Do not compare rows without denominator and scope labels.
- Keep SQLGlot route-separated.
- Keep `sqlglot_combined_same_engine_240` in appendix-only discussion.

## Remaining Gaps

- node alignment / attribution
- PORT9 or frozen selected PORT subset
- SpeedupTransferRate
- CONS9 verifier support
- method-level hard-negative rejection outside controls
