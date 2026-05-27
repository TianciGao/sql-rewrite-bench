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
- LLM-R2 now also has a separate paper-facing bounded PG-only reconciliation
  packet:
  [llm_r2_pg9_bounded_evidence_reconciliation_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.md).
  The fixed interpretation is bounded PostgreSQL-supported Common-core evidence
  on 9 PG rows:
  `9/9` generation attempts, `9/9` generated SQL files, `3/9` generated SQL
  executions with `3/9` exact matches, and `6/9` explicit
  `execution_failed` rows due to malformed generated SQL. This is not PG40,
  not tri-engine `120`, not timing evidence, and not leaderboard-comparable.
- LLM-R2 now also has a separate recovered-extraction route scaffold:
  [llm_r2_recovered_extraction_route_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_recovered_extraction_route_plan_v1.md).
  The fixed interpretation is still that the frozen PG9 packet remains the
  canonical original-route bounded evidence. Any future recovered-extraction
  output must be emitted as a separate route and must not overwrite or
  reinterpret the original-route packet.
- LLM-R2 now also has a non-dry-run execute-mode implementation for that
  separate recovered route:
  [llm_r2_recovered_extraction_execute_mode_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_recovered_extraction_execute_mode_plan_v1.md).
  The fixed interpretation remains generation-only recovered-route engineering.
  It does not itself authorize PostgreSQL execution, checker, timing, or any
  paper-table promotion.
- LLM-R2 now also has a separate recovered-extraction PG6 bounded evidence
  review packet:
  [llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.md).
  The fixed interpretation is separate route-scoped bounded PostgreSQL
  evidence on 6 rows:
  `6/6` generated rows, `6/6` PostgreSQL source executions, `6/6` PostgreSQL
  generated executions, and `6/6` exact matches. This is not original-route
  PG9 evidence, not recovered PG9 evidence, not PG40 evidence, not tri-engine
  `120` evidence, not timing evidence, and not leaderboard-comparable.
- A narrow recovered-route PG3 rerun was then attempted for `PERF_0006`,
  `PERF_0013`, and `PERF_0024`.
  The fixed interpretation is:
  `3/3` recovered-route generation successes, `3/3` recovered SQL retention
  results, and `3/3` static inspection passes, but `0/3` generated PostgreSQL
  executions completed because all three generated executions failed with a
  duplicated `SELECT` syntax pattern. Therefore recovered PG9 appendix
  evidence was not achieved, and recovered-route PG6 remains the current
  separate recovered-route bounded appendix packet.
- LLM-R2 should therefore be treated as bounded appendix-only evidence for
  paper-facing purposes:
  original-route PG9 remains bounded original-route evidence, recovered-route
  PG6 remains bounded recovered-route evidence, and the recovered-route PG3
  rerun is a failed appendix extension rather than a successful recovered PG9
  packet.
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
