# Decision Notes

## Fixed interpretation

- The current directory is a denominator-aware evidence ledger, not a final
  ranked leaderboard.
- Direct LLM, SQLGlot optimize, and SQLGlot no-op have retained `120` evidence.
- Calcite HEP has `93/120` correctness evidence but not full `120` timing.
- R-Bot must not be described as `not attempted on 120`; it has a formal `120`
  generation attempt and a PG15 execution/timing subset.
- LearnedRewrite and LLM-R2 do not yet have `120` evidence; their Stage-1
  scaffolds show dependency blockers.
- SQLSolver and VeriEQL are support/verifier, not rewrite methods for the
  current rerun campaign.
- SQLGlot cross-dialect and LLM Translate are portability routes, not Track A
  same-engine rerun rows.
- No failed, unsupported, no-op, or mismatch rows may be silently dropped from
  denominator accounting.

## Why this freeze folder exists

The Common-core v0 evidence now spans:

- paper-facing result cards
- proposed rows
- synthesis files
- bounded appendices
- rerun-governance drafts
- Stage-1 preflight scaffolds

This folder exists to keep those materials readable as one fixed governance
entrypoint without moving or rewriting the original artifacts.

## MISSING_NOT_INDEXED note

- `docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.csv` was requested in prior
  audits but does not exist, so it is not indexed as a retained artifact here.
