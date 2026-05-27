# PAPER_DRAFT_V0_DENOMINATOR_FREEZE_DECISION

## 1. Status

This is a paper-draft-v0 denominator freeze decision.

It is not a final benchmark freeze.

## 2. Decision

The current expanded evidence packet is frozen for paper results draft v0.

This means:

- the current expanded evidence packet is the fixed denominator for the next paper-draft-v0 results writing pass
- the final benchmark denominator remains open
- registry state remains unchanged
- admission and common-core promotion state remain unchanged

## 3. Frozen Paper-Draft-v0 Evidence Packet

Current frozen paper-draft-v0 packet:

- common-core seed: `9`
- Batch 2A PERF: `19`
- Batch 2B CONS: `3`
- expanded common-core evidence total: `31`
- seed PORT: `3`
- Batch 2C PORT: `3`
- PORT PostgreSQL-side evidence total: `6`

This freeze therefore covers:

- `31` common-core evidence cases
- `6` PostgreSQL-side PORT evidence cases

## 4. What This Enables

This freeze enables the following immediately:

- start drafting the paper results section
- use [PAPER_RESULTS_TABLES_DRAFT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_RESULTS_TABLES_DRAFT_v0.md) as the table source
- use the expanded common-core and expanded PORT closeouts as the supporting evidence packet
- preserve denominator, route, and portability caveats explicitly in the paper text

## 5. What This Does Not Claim

- not final benchmark denominator
- not final leaderboard
- not registry writeback
- not admission
- not full PORT closure
- not full cross-engine matrix
- not final taxonomy writeback

## 6. Allowed Future Expansion

Batch 3 expansion may happen later if time permits.

If that happens:

- Batch 3 evidence must be appended as later evidence
- it must not be silently mixed into paper-draft-v0 tables
- paper-draft-v0 tables should remain reproducible against the current closeout docs

## 7. Recommended Next Action

- draft the paper results section from [PAPER_RESULTS_TABLES_DRAFT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_RESULTS_TABLES_DRAFT_v0.md)

## 8. Verification / Non-Modification Note

- only this decision note was created
- no SQL / database / model / SQLGlot / checker execution
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched
