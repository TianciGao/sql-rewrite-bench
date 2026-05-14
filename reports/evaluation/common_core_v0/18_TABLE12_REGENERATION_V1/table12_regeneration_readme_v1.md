# Table 12 Regeneration README V1

## Inputs Read
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv`
- `reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv`
- `reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv`
- `reports/evaluation/common_core_v0/17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_cell_provenance_v1.csv`
- `reports/evaluation/common_core_v0/17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_formula_source_map_v1.csv`
- `reports/evaluation/common_core_v0/17_TABLE12_ULTIMATE_PROVENANCE_V1/table12_provenance_summary_v1.md`
- `reports/evaluation/common_core_v0/16_STATIC_RECOMPUTE_AUDIT_V1/static_recompute_results_v1.csv`
- `reports/evaluation/common_core_v0/16_STATIC_RECOMPUTE_AUDIT_V1/static_recompute_summary_v1.md`

## Outputs Written
- `reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.csv`
- `reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md`
- `reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_diff_v1.csv`
- `reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_readme_v1.md`

## Exact Command
`python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check`

## Formulas / Column Logic
`planned`, `executed`, and `exact` are copied from retained route evidence or candidate failure semantics. `generated_or_ready` preserves route-specific wording and does not conflate ready/preflight state with executed. `timed`, `gm_speedup`, and `regression_rate_20pct` are copied from retained timing slices. GM speedup is defined by the retained audits as `exp(mean(log(speedup_ratio)))`, and Regression@20 as `count(speedup_ratio < 0.8) / timing_denominator`.

## What This Script Does Not Do
It does not run databases, LLM/model calls, verifier experiments, PORT9 experiments, EXPLAIN, timing collection, benchmark case generation, or retained source artifact regeneration.

## Known Limitations
This is a Table 12 render entrypoint only. It does not regenerate `table3_same_engine_method_evidence_v3.csv`, `candidate_failure_accounting_v1.csv`, or `speedup_slice_summary_v1.csv`.

## Source-Of-Truth Writeback Judgment
No source-of-truth writeback is needed. This script hardens reproducible rendering without changing retained values, denominators, taxonomy, case facts, protocol, or paper claims.
