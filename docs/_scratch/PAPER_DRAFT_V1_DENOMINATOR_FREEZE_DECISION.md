# PAPER_DRAFT_V1_DENOMINATOR_FREEZE_DECISION

## 1. Status

This is a paper-draft-v1 denominator freeze decision.

It is not a final benchmark freeze.

## 2. Decision

The current expanded evidence packet is frozen for paper results draft v1.

This means:

- the current expanded evidence packet is the fixed denominator for the next paper-draft-v1 writing pass
- the final benchmark denominator remains open
- registry state remains unchanged
- admission and common-core promotion state remain unchanged
- formal review state remains unchanged

## 3. Frozen Paper-Draft-v1 Evidence Packet

Current frozen paper-draft-v1 packet:

- common-core seed: `9`
- Batch 2A PERF: `19`
- Batch 2B CONS: `3`
- Batch 3A PERF: `11`
- Batch 3B PERF: `4`
- expanded common-core evidence total: `46`
- seed PORT: `3`
- Batch 2C PORT: `3`
- PORT PostgreSQL-side evidence total: `6`

This freeze therefore covers:

- `46` common-core evidence cases
- `6` PostgreSQL-side PORT evidence cases

## 4. Final PORT Feasibility Note

The final PORT expansion feasibility preflight found no quick-add candidates.

- `PORT_0003`:
  - `needs_pg_witness_backfill`
- `PORT_0006`:
  - `needs_pg_witness_backfill`
- `PORT_0016`:
  - `too_slow_for_current_cycle`

Accordingly, the paper-draft-v1 freeze keeps the current `6`-case PostgreSQL-side PORT packet unchanged rather than widening it with a last-minute partial add.

## 5. What This Enables

This freeze enables the following immediately:

- start or continue drafting the paper results section against a stable v1 packet
- use [PAPER_RESULTS_TABLES_DRAFT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_RESULTS_TABLES_DRAFT_v0.md) as the working table source
- use the expanded common-core and expanded PORT closeouts as the supporting evidence packet
- preserve denominator, route, portability, and paper-draft governance caveats explicitly in the paper text

## 6. What This Does Not Claim

- not final benchmark denominator
- not final leaderboard
- not registry writeback
- not admission
- not common-core promotion
- not full PORT closure
- not full cross-engine matrix
- not final taxonomy writeback
- not formal review update

## 7. Allowed Future Expansion

Batch 3 or later expansion may happen later if time permits.

If that happens:

- later evidence must be appended as later evidence
- it must not be silently mixed into paper-draft-v1 tables
- paper-draft-v1 tables should remain reproducible against the current closeout and freeze documents

## 8. Recommended Next Action

- draft the paper results section from [PAPER_RESULTS_TABLES_DRAFT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PAPER_RESULTS_TABLES_DRAFT_v0.md)

## 9. Verification / Non-Modification Note

- only this decision note was created
- no SQL / database / model / SQLGlot / checker execution
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched
