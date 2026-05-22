**First-read summary**

This freeze folder is a denominator-aware evidence ledger for Common-core v0, not a final ranked leaderboard. The package separates Track A same-engine rewrite evidence, Track B support-layer evidence, and Track C portability evidence so that correctness, timing, observability, and verifier support are not silently mixed.

**Strong claims supported now**

- The paper denominator is frozen at 40 Common-core v0 cases with a 16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL split.
- Track A same-engine evidence is reported on a 120-row expansion where appropriate, with correctness-gated performance.
- Timing claims are restricted to exact timed subsets.
- Hard-negative controls provide an explicit tested-denominator guardrail view.
- Bounded prior-method evidence is retained and clearly separated from the main same-engine table.

**Partial / bounded claims**

- Direct LLM currently has the strongest retained Track A same-engine route evidence, but that remains a route-scoped statement rather than a winner claim.
- SQLGlot route evidence is retained, but SQLGlot optimize and SQLGlot same-dialect transpile/no-op must remain route-separated.
- Track C currently supports bounded PORT6 portability evidence, not full PORT9.
- Support-layer evidence exists for SQLSolver and VeriEQL, but only as smoke/canary scope rather than denominator-complete verifier coverage.
- Selected case-study observability exists as a qualitative bridge only, not as denominator-complete observability coverage.

**Unsupported claims that must not appear in abstract or conclusion**

- Do not claim this package is a final ranked leaderboard.
- Do not claim a global winner.
- Do not claim full PORT9 completion.
- Do not claim SpeedupTransferRate.
- Do not claim CONS9 verifier completion.
- Do not claim full plan-node attribution, denominator-complete NodeAlignmentCoverage, or denominator-complete AttributionCoverage.

**How to cite the tables in the paper**

- Cite Table 1 for the accepted denominator and Table 3 for denominator-aware same-engine route evidence.
- Cite Table 4 before Table 6 whenever discussing performance, because correctness-gated performance is the governing rule.
- Cite Table 5 and Table 10 only as support-layer evidence and selected case-study observability, not as rewrite ranking evidence.
- Cite Table 8 only for portability / translation evidence and keep it separate from same-engine rewrite discussion.
- Cite Table 9 only for verifier support and never as a speed baseline.
- Cite Table 11 whenever bounded prior-method evidence is mentioned.

**Recommended wording for results section**

Use wording like: "We report a denominator-aware evidence ledger rather than a final ranked leaderboard. For Track A, correctness-gated performance is summarized on exact timed subsets. Prior-method and route-bounded packets are retained as bounded prior-method evidence. Observability and verifier analyses remain support-layer evidence, with selected case-study observability replacing any claim of denominator-complete plan attribution."
