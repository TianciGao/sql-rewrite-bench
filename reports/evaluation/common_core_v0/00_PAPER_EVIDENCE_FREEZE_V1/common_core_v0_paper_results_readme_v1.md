**What This Package Is**

This folder is the paper-facing freeze package for Common-core v0. It is organized as a denominator-aware evidence ledger that separates same-engine rewrite evidence, support-layer evidence, portability evidence, bounded prior-method evidence, and selected case-study observability.

**What It Is Not**

- It is not a final ranked leaderboard.
- It is not a global winner declaration.
- It is not full PORT9 closure.
- It is not CONS9 verifier completion.
- It is not denominator-complete plan attribution.

**Reading Order**

1. `paper_table_contract_v1.csv` and `table1_common_core_composition_v1.csv`
2. `paper_results_table_index_v1.csv`
3. `paper_claim_matrix_v1.csv`
4. Table 3 and Table 4
5. Table 6 and Table 7
6. Table 5, Table 8, Table 9, Table 10
7. Table 11
8. `paper_remaining_experiment_gaps_v1.csv`

**Table 1–11 Map**

- Table 1: accepted denominator split
- Table 2: protocol/design surface
- Table 3: Track A same-engine denominator-aware method evidence
- Table 4: correctness and guardrail evidence
- Table 5: observability / plan artifact support
- Table 6: performance on exact timed subsets
- Table 7: failure accounting matrix
- Table 8: Track C portability / translation
- Table 9: verifier support
- Table 10: selected case-study observability
- Table 11: appendix bounded / pilot evidence reuse

**Current Result Highlights**

- The accepted Common-core v0 denominator is 40 cases: 16 PERF, 9 CONS, 9 PORT, 6 LONGTAIL.
- Track A same-engine evidence is organized on a 120-row expansion where appropriate.
- Direct LLM currently has the strongest retained Track A same-engine route evidence, but this is not a winner claim.
- Hard-negative controls support a tested-denominator guardrail view.
- Timing is correctness-gated and reported only on exact timed subsets.
- Track C is bounded PORT6 evidence, not full PORT9.

**Claim Boundaries**

- Track A, Track B, and Track C must remain separate.
- Support-layer evidence must not be read as rewrite ranking evidence.
- Table 8 is portability-only.
- Table 9 is verifier support only.
- Table 10 is selected case-study only.
- Do not compare rows without denominator/scope labels.

**Remaining Gaps**

- Method-level negative rejection for non-control rows
- SQLGlot full per-case timing export
- Full PORT9 or explicitly frozen selected PORT subset
- SpeedupTransferRate
- CONS9 verifier support
- Method-specific plan extraction, node alignment, attribution, and case-level failure exemplar

**Reproduction / Review Note**

This package is built from retained artifacts only. It is intended for paper review and synthesis, not as a trigger to rerun DB engines, timing jobs, translation jobs, plan extraction, LLM generation, or verifier tools.

**Do Not Compare Rows Without Denominator / Scope Labels**

Every table in this folder is scope-labeled on purpose. Do not compare rows across Track A, Track B, Track C, appendix-only packets, PG-only bounded packets, or exact timed subsets unless the denominator and claim boundary are aligned.
