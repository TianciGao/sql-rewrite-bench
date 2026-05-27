# Common-core v0 Paper Results Readme V8

This version refreshes the paper index and claim layer after `Table 5 v5` and the `Table 10A / Table 10B` split.

- `Table 5 v5` remains a route-level observability coverage matrix.
- `Table 10A` is the selected PG plan-attribution case-study surface.
- `Table 10B` remains separate failure-side diagnostic evidence anchored by `CONS_0024 / pg / Direct LLM / mismatch`.
- The reviewed PG attribution packet retains `24/24` plan parse success.
- `21/24` rows are `buffer_or_runtime_delta_without_operator_change`.
- Attribution confidence is `22/24 low` and `2/24 medium`.

This does not create denominator-wide causal attribution. It strengthens selected-case observability only.

中文说明：v8 的关键不是新实验，而是把索引和 claim layer 对齐到 `Table 5 v5` 与 `Table 10A / 10B`。`10A` 是 selected PG attribution，`10B` 是 failure-side diagnostic。`24/24` 计划解析成功、`21/24` 仅表现为 buffer/runtime delta、`22/24` 低置信度、`2/24` 中等置信度，这些都是 packet-level facts，但都不能升级成 full-denominator causal attribution。
