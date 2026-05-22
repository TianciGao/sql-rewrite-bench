# RQ1 Failure Accounting Readme v1

## Inputs inspected

- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_summary_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_event_long_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv`

## Outputs created

- `hard_negative_guardrail_ledger_v1.csv`
- `hard_negative_guardrail_ledger_v1.md`
- `candidate_failure_accounting_v1.csv`
- `candidate_failure_accounting_v1.md`
- `rq1_failure_accounting_readme_v1.md`

## Aggregation rules

- Hard-negative per-row ledger uses `package_hard_negative_closure_event_long_v1.csv` as the canonical row source.
- Hard-negative summary counts are validated against `package_hard_negative_closure_summary_v1.csv` and `package_hard_negative_rejection_mode_audit_v1.csv`.
- Candidate route rows prefer `method_candidate_rejection_accounting_v1.csv` for exact/non-exact frontier accounting and `table7_failure_accounting_matrix_v3.csv` for failure buckets.
- `table3_same_engine_method_evidence_v3.csv` is used only where it supplies retained route-level planned/generated/executed/exact context.
- When a retained artifact exposes both successful-execution and broader ready-after-preflight notions, `executed` is normalized here to successful execution rather than not-preflight-blocked accounting.

## Bucket normalization rules

- Hard-negative `mismatch_rejected` -> `executable_semantic_mismatch`
- Hard-negative `negative_execution_failed_rejected` -> `execution_failure_rejection`
- Hard-negative `checker_failed` -> `checker_failure`
- Hard-negative blocked `missing_artifact` rows with `not_applicable_source_reference_engine` failure detail -> `not_applicable`
- Candidate-side buckets are copied from retained route-level artifacts; no new bucket is invented.

## Denominator rules

- Package hard-negative planned denominator remains `120`, with `111` tested and `9` blocked/not-applicable rows still visible.
- Candidate rows are not forced into the 120-row denominator when retained evidence is bounded or appendix-scoped.
- Mixed-scope appendix rows keep their retained denominator ids and explicit caution notes.
- The recovered LLM-R2 appendix row preserves the retained PG9 recovery-audit denominator while separately noting the PG6 exact recovered subset.

## Known limitations

- Some appendix prior methods retain only mixed-scope or summary-only failure frontiers.
- SQLGlot optimize keeps two checker-failed rows visible in notes/rejection accounting context, but the Table 15 schema here does not add a new checker_failed candidate bucket.
- LearnedRewrite retains bounded evidence but not a main-track denominator-compatible row-level frontier.

## Whether source-of-truth writeback is needed

- No. These are evidence-freeze aggregation artifacts only.
