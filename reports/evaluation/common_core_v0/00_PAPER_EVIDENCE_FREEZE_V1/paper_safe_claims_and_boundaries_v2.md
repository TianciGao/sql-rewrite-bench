# Paper Safe Claims And Boundaries v2

## 可安全主张 / Can Claim

- 本套 freeze folder 是一个 **denominator-aware evidence ledger**，不是 **final ranked leaderboard**。
- Common-core v0 的 paper denominator 固定为 `16/9/9/6 = 40`，Track A same-engine 扩展为 `120` 行。
- `Direct LLM` 原始 same-engine baseline 保留 `94/120` exact rows。
- `Direct LLM + Execute-and-Repair-1` 在 21 个 repair-ready rows 上进行一次反馈修复，最终把 exact rows 从 `94/120` 提升到 `96/120`。
- `Calcite HEP` 保留 `93/120` fail-closed correctness ledger，并且现在有 `93` exact-row correctness-gated timing。
- 所有性能数字都必须按 **correctness-gated performance** 理解，只能在 **exact timed subsets** 上报告。
- case-level failure export 现在支持具体 failure row，因此 Table 10 v2 的 failure exemplar 已经从占位符升级为 `CONS_0024 / pg / direct_llm / direct_llm_same_engine_rewrite / mismatch`。

## 部分 / 有边界 / Partial Or Bounded

- `Direct LLM + Execute-and-Repair-1` 是反馈增强路由，使用同一模型家族，但它是 separately versioned route，不替代原始 Direct LLM。
- `Calcite HEP` 的 timing claim 只覆盖 `93` exact-row correctness-gated timing，不是 full `120` timing。
- `SQLGlot` 仍然必须 route-separated：`sqlglot_optimize_same_dialect` 与 `sqlglot_transpile_same_dialect_noop` 不能合并成一个方法赢家叙事。
- `R-Bot`、`LLM-R2`、`LearnedRewrite` 仍属于 **bounded prior-method evidence**，应留在 Table 11 appendix 范围内。
- Table 10 v2 只能支持 **selected case-study observability**。failure exemplar 已经具体化，但 method-specific plan extraction、node alignment、attribution 仍未补齐。
- Table 5 / Table 9 仍然是 **support-layer evidence**，不是 rewrite method ranking metrics。

## 不能主张 / Cannot Claim

- 不能主张 **final ranked leaderboard**。
- 不能主张 global method winner。
- 不能主张 `Calcite HEP` full `120` timing。
- 不能主张 full plan attribution、full node alignment、或 denominator-complete attribution coverage。
- 不能主张 full `PORT9`。
- 不能主张 `SpeedupTransferRate`。
- 不能主张 `CONS9` verifier completion。
- 不能把 hard-negative control 结果写成 non-control method-level negative rejection。

## 论文引用建议 / How To Cite The Tables

- Table 3：用于 same-engine denominator-aware correctness + timing coverage 总览。
- Table 4：用于 correctness / controls / hard-negative boundary。
- Table 6：用于 exact timed subsets 上的 GM speedup、median、Regression@20、best/worst。
- Table 7：用于 failure frontier 与 case-level failure accounting。
- Table 10 v2：只用于 selected-case qualitative observability narrative，不用于 full observability claim。
- Table 11：用于 appendix bounded evidence，不能回流成主表赢家叙事。

## 推荐结果段落写法 / Recommended Results Wording

可采用如下安全表达：

`On the fixed Common-core v0 denominator, Direct LLM retains 94/120 exact rows, while Direct LLM + Execute-and-Repair-1 recovers 2 additional exact rows to 96/120 on the retained 21-row repair-ready frontier. Calcite HEP retains a 93/120 fail-closed correctness ledger and now has a 93 exact-row correctness-gated timing packet. These rows should be read as denominator-aware evidence, not a final ranked leaderboard.`

同时避免如下误写：

- `Method X wins overall.`
- `Calcite HEP has full 120 timing.`
- `Table 10 proves full observability.`
- `Track C proves SpeedupTransferRate.`
