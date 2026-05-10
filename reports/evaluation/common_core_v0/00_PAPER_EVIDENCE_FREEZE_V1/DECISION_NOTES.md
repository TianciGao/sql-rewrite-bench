# Decision Notes

## Fixed interpretation

- The current directory is a denominator-aware evidence ledger, not a final
  ranked leaderboard.
- Direct LLM, SQLGlot optimize, and SQLGlot no-op have retained `120` evidence.
- Calcite HEP has `93/120` correctness evidence but not full `120` timing.
- R-Bot must not be described as `not attempted on 120`; it has a formal `120`
  generation attempt and a PG15 execution/timing subset.
- Previous preflight-only wording for R-Bot is now superseded and caveated by
  the reconciliation packet:
  [r_bot_common_core_120_evidence_reconciliation_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.md).
  The fixed interpretation is mixed-scope retained evidence:
  formal `120` generation attempt, PG40 generation expansion, PG15 execution
  and timing subset, and explicit MySQL/Spark canary failure.
- LearnedRewrite and LLM-R2 do not yet have `120` evidence; their Stage-1
  scaffolds show dependency blockers.
- SQLSolver and VeriEQL are support/verifier, not rewrite methods for the
  current rerun campaign.
- SQLGlot cross-dialect and LLM Translate are portability routes, not Track A
  same-engine rerun rows.
- No failed, unsupported, no-op, or mismatch rows may be silently dropped from
  denominator accounting.

## Human recovery-priority decision

- `date = 2026-05-10`
- approved recovery priority:
  1. `llm_r2`
  2. `r_bot`
  3. `learnedrewrite`
- `llm_r2` is the highest-priority recovery candidate.
- `r_bot` is held as final mixed-scope evidence for now and should not be
  pursued immediately as a full `120` rerun target.
- `learnedrewrite` is deferred unless adapter, checkpoint, and inference
  artifacts are provided.

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
