# Table 4 Hard-Negative Finalization Recommendation V1

This is a diagnosis memo from retained artifacts only. No DB, checker, timing, generation, verifier, or EXPLAIN run was performed in this step.

## Assessment

1. **Is Table 4A substantively strong as a main-paper table?**

Yes, with one explicit caveat. The tested hard-negative packet is substantively strong because all `111` tested rows are rejected as **executable semantic mismatches**, not as execution failures or checker crashes. The caveat is coverage: `9/120` planned rows remain explicit `PORT` source-reference-engine `not_applicable` cells.

2. **Are most negative rejections semantic mismatches or execution failures?**

They are entirely semantic mismatches in the retained tested packet:

- `mismatch_rejected = 111`
- `negative_execution_failed_rejected = 0`
- `checker_failed = 0`
- `source_execution_failed = 0`
- `false_accept = 0`

3. **Which pool best demonstrates semantic negative value?**

All tested pools tie at `1.0000` executable mismatch negative rate. If one pool must be highlighted, `PERF` or `CONS` is cleaner than `PORT` because they have no blocked rows.

4. **Which engine has the most execution-failure negatives?**

None. Every engine has `0` execution-failure negatives on the tested frontier. `mysql` has the largest blocked not-applicable slice, but that is a coverage issue, not an execution-failure issue.

5. **Should Table 4A be promoted to the main paper as-is?**

Yes, but only if the final table explicitly separates:

- planned negatives
- tested negatives
- blocked / not-applicable negatives
- mismatch-based rejections
- false accepts

The main-paper value is strong precisely because the tested packet is semantic, not crash-driven.

6. **Should we revise or repair any negative rewrites before final paper freeze?**

No repair is currently required for the tested rows. The retained evidence does not show weak negatives, execution-failure negatives, or false accepts among runnable rows. The remaining action is documentation discipline: keep the `9` blocked `PORT` rows visible as `not_applicable`, not as hidden failures or silently omitted rows.

7. **What exact columns should the final Table 4A use?**

Recommended final main-paper columns:

- `scope`
- `planned_negative_rows`
- `tested_negative_rows`
- `blocked_not_applicable_rows`
- `mismatch_rejected`
- `negative_execution_failed_rejected`
- `false_accept`
- `NegativeRejectionRate`
- `FalseAcceptRate`
- `executable_mismatch_negative_rate`

If space is tight, the most important retained semantic signal is:

- `tested_negative_rows`
- `mismatch_rejected`
- `false_accept`
- `blocked_not_applicable_rows`
- `executable_mismatch_negative_rate`

8. **What should remain appendix-only?**

- full row-level event log
- per-row blocked `PORT` identifiers
- any very detailed by-engine breakdown if table space is limited

The by-pool and by-engine summaries are useful, but they can move to appendix if the main table needs to stay compact.

9. **What must not be overclaimed?**

- Do not claim `120/120` hard-negative closure; the safe statement is `111/111 tested negatives rejected`, with `9` explicit not-applicable blocked rows.
- Do not imply this packet audits accepted generated candidates for false accept.
- Do not relabel package hard-negative closure as method-level hard-negative rejection.
- Do not use this table to support a final leaderboard or global winner claim.

## Bottom Line

结论很明确：当前 package hard-negative packet **不是弱证据**。它的强点在于，保留下来的 `111` 个 tested negatives 全部是“能跑、checker 也能判、而且结果确实不等价”的语义负例。最终 Table 4A 应该突出这一点，而不是只写一个不透明的 `111/111 rejected`。
