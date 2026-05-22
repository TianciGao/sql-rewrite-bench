# Common-core v0 Paper Results Readme v2

## What This Package Is

这是 Common-core v0 的 paper-facing freeze-folder 结果入口。
它把主表、附表、claim 边界、以及 remaining gaps 放在一个可先读的结构里。

## What It Is Not

- 它不是 final ranked leaderboard。
- 它不是 global method winner 公告。
- 它不是 full PORT9 结果包。
- 它不是 full plan attribution 结果包。
- 它不是 verifier-complete CONS9 结果包。

## Reading Order

1. `paper_results_table_index_v2.csv` / `.md`
2. `paper_safe_claims_and_boundaries_v2.md`
3. `paper_claim_matrix_v2.csv` / `.md`
4. `table3_same_engine_method_evidence_v2.csv` / `.md`
5. `table4_correctness_guardrail_evidence_v1.csv` / `.md`
6. `table6_performance_on_exact_timed_rows_v3.csv` / `.md`
7. `table7_failure_accounting_matrix_v2.csv` / `.md`
8. `table10_plan_observability_case_study_v2.csv` / `.md`
9. `table11_bounded_pilot_evidence_reuse_v2.csv` / `.md`
10. `paper_remaining_experiment_gaps_v2.csv` / `.md`

## Table 1–11 Map

- Table 1: denominator contract
- Table 2: protocol/design surface
- Table 3: same-engine denominator-aware method evidence
- Table 4: correctness and guardrail evidence
- Table 5: support-layer observability readiness
- Table 6: exact timed subset performance
- Table 7: failure accounting and failure frontier
- Table 8: Track C portability / translation only
- Table 9: verifier support only
- Table 10: selected case-study observability only
- Table 11: appendix bounded / pilot evidence reuse

## Current Result Highlights

- Direct LLM 原始 same-engine baseline 保留 `94/120` exact rows。
- Direct LLM + Execute-and-Repair-1 把 exact rows 提升到 `96/120`，但它是 separately versioned feedback-aware route。
- Calcite HEP 保留 `93/120` fail-closed correctness ledger，并且现在有 `93` exact-row correctness-gated timing。
- case-level failure export 现在支持具体 failure row，因此 Table 10 v2 的 failure exemplar 已经具体化。

## Claim Boundaries

- Track A / Track B / Track C 必须分开读。
- Table 8 是 portability-only，不是 same-engine rewrite performance。
- Table 9 是 support-layer evidence，不是 rewrite generator 比较表。
- Table 10 是 selected-case qualitative surface，不是 denominator-complete observability。
- Do not compare rows without denominator/scope labels.

## Remaining Gaps

- SQLGlot full per-case timing export
- method-specific plan extraction for Table 10 selected cases
- node alignment
- attribution mapping
- full PORT9 or frozen selected PORT subset
- SpeedupTransferRate
- CONS9 verifier support
- method-level hard negative rejection for non-control rows

## Reproduction / Review Note

本目录只整合保留工件，不会替代原始 run packet。
写论文时应先看 claim matrix，再看具体表格，再回到 run-level artifact 做 spot check。

## Do Not Compare Rows Without Denominator / Scope Labels

同一个数字如果 denominator、engine scope、route scope、timing scope 不同，就不能直接横向比较。
特别是：

- `Direct LLM` 与 `Direct LLM + Execute-and-Repair-1` 不是同一协议行
- `Calcite HEP` 的 `93` exact-row timing 不是 full `120` timing
- `R-Bot`、`LLM-R2`、`LearnedRewrite` 仍是 appendix / bounded evidence
