# Status

This note records the narrow Batch 2B CONS backfill for:

- `CONS_0024`
- `CONS_0031`
- `CONS_0034`

The backfill is limited to `validation/checker.yaml` and `taxonomy_trial_v0.3.yaml` creation plus read-only YAML validation and preflight rerun. No SQL, checker, or database execution was performed.

# Files Created

- `cases/CONS/CONS_0024/validation/checker.yaml`
- `cases/CONS/CONS_0031/validation/checker.yaml`
- `cases/CONS/CONS_0034/validation/checker.yaml`
- `cases/CONS/CONS_0024/taxonomy_trial_v0.3.yaml`
- `cases/CONS/CONS_0031/taxonomy_trial_v0.3.yaml`
- `cases/CONS/CONS_0034/taxonomy_trial_v0.3.yaml`

# Checker Backfill

All three checker configs now:

- define `source.sql` vs `rewrite_pos_01.sql` as expected equal
- define `source.sql` vs `rewrite_neg_01.sql` as expected not equal
- point to existing PostgreSQL TSV outputs under `runs/pg/`
- cite existing `runs/result_check.json` and `runs/pg/result_check.json` as witness-backed validation evidence

Boundary:

- witness-backed checker config only
- not admission
- not promotion
- not formal review

# Taxonomy Draft Backfill

All three taxonomy drafts now:

- use `status: batch2b_taxonomy_draft`
- use `candidate_primary_pool: consistency`
- use `dataset_line_candidate: consistency-extension-candidate`
- derive tags conservatively from existing manifest tags, SQL text, and PostgreSQL plan artifacts

Per case:

- `CONS_0024`
  - SQL features: `correlated_subquery`, `outer_join`
  - rewrite opportunity: `subquery_decorrelation`
  - plan operators: `scan`, `join`, `aggregate`, `subquery`
- `CONS_0031`
  - SQL features: `correlated_subquery`
  - rewrite opportunity: `subquery_decorrelation`
  - plan operators: `scan`, `project`, `subquery`
- `CONS_0034`
  - SQL features: `outer_join`, `expression_complexity`
  - rewrite opportunities: `aggregation_rewrite`, `expression_simplification`
  - workload realism: `complex_expression_density`
  - plan operators: `scan`, `join`, `aggregate`

# Batch 2B Preflight Effect

Validation performed:

- YAML syntax validated for all six new YAML files
- `python -m scripts.cli formal-batch2b-cons-backfill-preflight`
- `python -m json.tool reports/formal_expansion/batch2b_cons_backfill_preflight_v0.json >/dev/null`

Observed status movement:

- `CONS_0024`: `minor_backfill_needed` -> `ready_for_batch2b_execution`
- `CONS_0031`: `minor_backfill_needed` -> `ready_for_batch2b_execution`
- `CONS_0034`: `minor_backfill_needed` -> `ready_for_batch2b_execution`

Current preflight result:

- `ready_count=3`
- `minor_backfill_count=0`
- `recommended_batch2b_execution_cases=[CONS_0024, CONS_0031, CONS_0034]`

# Boundaries

- no SQL execution
- no checker execution
- no registry update
- no `docs/EXECUTION_STATUS.md` update
- no formal review update
