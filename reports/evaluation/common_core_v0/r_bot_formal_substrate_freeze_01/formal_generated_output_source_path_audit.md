# Formal Generated-Output Source Path Audit

## Scope

This audit addresses the single generated-output source-path blocker carried in `formal_gate_status_v6`:

- `generated_source_missing:calcite:/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`

It does not modify generated outputs.

## Direct Answer

Root cause classification: `path bug / stale template assumption`

It is **not** a pure missing-file situation.
It is **not** evidence that no Calcite generated outputs exist in the repository.

## Evidence

### Missing path referenced by current checker templates

The current human-run checker scaffolds point the Calcite family at:

- `reports/evaluation/common_core_v0/runs/calcite_same_engine_generation_01/generated`

That exact path is missing.

This stale path appears in:

- [run_manual_r_bot_formal_generated_output_exclusion_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_generated_output_exclusion_check.py)
- [run_manual_r_bot_formal_contamination_hash_check.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/run_manual_r_bot_formal_contamination_hash_check.py)
- [formal_corpus_manifest_draft.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_corpus_manifest_draft.csv)
- [formal_contamination_attestation_template.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_contamination_attestation_template.csv)

### Actual Calcite generated-output tree present in repo

The repository does contain a Calcite generated tree at:

- `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`

Observed facts:

- root exists
- discovered `.sql` files under that root: `33`
- route recorded in [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/run_results.json): `calcite_hep_pg_rewrite`
- generated file naming pattern:
  - `generated/<case_id>/pg/calcite_hep_pg_rewrite.sql`

## Interpretation

The current blocker comes from a stale assumption that the Calcite family should look like:

- run id: `calcite_same_engine_generation_01`
- file name: `calcite_same_engine_rewrite.sql`

But the visible retained artifacts actually use:

- run id: `calcite_hep_pg40_generation_01`
- route/file name: `calcite_hep_pg_rewrite.sql`
- engine scope: `pg`

So the blocker is best described as:

- `path bug in checker/template inputs`
- plus `family naming mismatch between placeholder formal template and actual retained Calcite run`

## Proposed Correction

Do not change generated outputs.

Instead, correct the future exclusion input contract so that the Calcite family points at the actual retained family root:

- root:
  - `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated`
- path template:
  - `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/generated/<case_id>/pg/calcite_hep_pg_rewrite.sql`

If the formal policy intends to exclude only actual discovered generated artifacts rather than a hypothetical same-engine Calcite family, the checker should enumerate the real PG40 retained tree.

If the formal policy instead requires a future tri-engine Calcite same-engine family that does not yet exist, then the current blocker should be renamed from `generated_source_missing` to a more honest policy-side blocker such as:

- `generated_family_not_materialized_for_formal_scope:calcite_same_engine`

## Recommended Handling In The Gate Draft

For current governance, the safest interpretation is:

1. clear that the old Calcite blocker is a stale path/template issue
2. do not claim Calcite exclusion fully passed yet
3. require the next human-run exclusion rerun to target the actual retained Calcite generated tree or an explicitly frozen alternative family definition

## Bottom Line

Missing Calcite path root cause: `stale checker/template path`

Actual repo state:

- Calcite generated outputs are present
- they live under `calcite_hep_pg40_generation_01/generated`
- they use `calcite_hep_pg_rewrite.sql`

Therefore the single Calcite blocker should be treated as a correction-to-audit-input issue, not as proof that the repository lacks Calcite generated outputs.
