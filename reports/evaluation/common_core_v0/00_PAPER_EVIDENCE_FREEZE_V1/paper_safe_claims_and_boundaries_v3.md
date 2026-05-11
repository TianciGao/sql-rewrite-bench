# Paper Safe Claims and Boundaries v3

## Can Claim

- Common-core v0 仍然是固定的 `16/9/9/6 = 40`，Track A same-engine 扩展仍然是 `120` 行。
- 结果仍然是一个 **denominator-aware evidence ledger**，**not a final ranked leaderboard**。
- `correctness-gated performance` 仍然是核心口径，计时只看 `exact timed subsets`。
- SQLGlot 现在可以安全地用 route-separated 口径写入主表：
  - `sqlglot_transpile_same_dialect_noop`: exact72 / timed72
  - `sqlglot_optimize_same_dialect`: revised exact63 / timed63
- `bounded prior-method evidence` 仍然只放在 Table 11。
- Table 5 / Table 9 / Table 10 仍然是 `support-layer evidence` 或 `selected case-study observability`，不是主排名表。

## Partial / Bounded

- SQLGlot combined 240 仍然只是 appendix diagnostic aggregate。
- SQLGlot optimize 的旧 aggregate 65 已经不再作为 paper-safe 主 timing denominator；现在用 revised exact63。
- 两个 optimize checker_failed 行仍然保留在 backfill packet 中，但不进入 timing denominator。

## Cannot Claim

- final ranked leaderboard
- global method winner
- SQLGlot combined as a main route
- full plan attribution
- full PORT9
- SpeedupTransferRate
- CONS9 verifier completion

## Writing Guidance

- 结果段落里可以直接引用 Table 3 v3 和 Table 6 v4 的 SQLGlot rows。
- 但必须明确写出 `route-separated`，并注明 optimize 使用的是 revised `63` exact rows。
