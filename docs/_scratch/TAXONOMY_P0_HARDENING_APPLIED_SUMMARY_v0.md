# TAXONOMY_P0_HARDENING_APPLIED_SUMMARY_v0

## 1. Status

P0 hardening was applied only for:

- `PERF_0033`
- `PERF_0054`

The bounded case-local taxonomy trial files were created, the `formal-experiment-taxonomy-slicing` parser was fixed for `taxonomy_trial_v0.3.yaml`, and the existing taxonomy slicing command was rerun.

## 2. Files Created

- `cases/PERF/PERF_0033/taxonomy_trial_v0.3.yaml`
- `cases/PERF/PERF_0054/taxonomy_trial_v0.3.yaml`
- `docs/_scratch/TAXONOMY_P0_HARDENING_APPLIED_SUMMARY_v0.md`

## 3. Patch Basis

Patch basis:

- [TAXONOMY_P0_HARDENING_PATCH_PLAN_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/TAXONOMY_P0_HARDENING_PATCH_PLAN_v0.md)
- [TAXONOMY_METADATA_HARDENING_PLAN_FOR_RQ4_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/TAXONOMY_METADATA_HARDENING_PLAN_FOR_RQ4_v0.md)

Patch boundaries:

- no registry writeback
- no taxonomy vocabulary change
- no formal review update
- no other case was modified

## 4. PERF_0033 Tags Applied

- `trial_version="0.3"`
- `status=p0_taxonomy_hardened_draft`
- `candidate_primary_pool=performance`
- `dataset_line_candidate=common-core`
- `sql_feature_tags=[]`
- `rewrite_opportunity_tags`:
  - `predicate_pushdown`
  - `join_reorder`
- `portability_tags`:
  - `limit_fetch_gap`
- `workload_realism_tags`:
  - `classic_analytical_baseline`
- `plan_operator_tags.observed_in_postgres`:
  - `scan`
  - `join`
  - `aggregate`
  - `sort`
  - `limit`

Evidence boundary recorded in the file:

- `source.sql` and `manifest.yaml` were inspected
- existing PostgreSQL plan artifacts were used only as supporting evidence for provisional plan operator tags
- `date_time_function` was intentionally not tagged
- this is not registry writeback and not formal admission

## 5. PERF_0054 Tags Applied

- `trial_version="0.3"`
- `status=p0_taxonomy_hardened_draft`
- `candidate_primary_pool=performance`
- `dataset_line_candidate=common-core`
- `sql_feature_tags=[]`
- `rewrite_opportunity_tags`:
  - `join_reorder`
  - `predicate_pushdown`
- `portability_tags`:
  - `limit_fetch_gap`
- `workload_realism_tags`:
  - `classic_analytical_baseline`
- `plan_operator_tags.observed_in_postgres`:
  - `scan`
  - `join`
  - `aggregate`
  - `sort`
  - `limit`

Evidence boundary recorded in the file:

- `source.sql` and `manifest.yaml` were inspected
- existing PostgreSQL plan artifacts were used only as supporting evidence for provisional plan operator tags
- `date_time_function` was intentionally not tagged
- this is not registry writeback and not formal admission

## 6. Taxonomy Slicing Verification Result

The existing taxonomy slicing command reran successfully and rewrote:

- `reports/formal_common_core/taxonomy_slicing_v0.json`

Observed counts from the corrected report:

- `cases_with_taxonomy_tags_count=12`
- `cases_missing_taxonomy_tags_count=0`
- `sql_feature_gap_count=0`
- `portability_tag_gap_count=1`
- `workload_realism_gap_count=2`
- `taxonomy_trial_missing_count=4`
- `taxonomy_trial_placeholder_or_empty_count=5`
- `taxonomy_trial_provisional_count=1`

Bucket-level verification from the new report:

- `by_sql_feature_tag.untagged.case_count=2`
- `by_sql_feature_tag.untagged.cases=[PERF_0033, PERF_0054]`
- `by_portability_tag.untagged.case_count=1`
- `by_portability_tag.untagged.cases=[CONS_0007]`
- `by_portability_tag.limit_fetch_gap.cases=[PERF_0033, PERF_0054, CONS_0012]`

Interpretation:

- the two new files reduced `taxonomy_trial_missing_count` from the prior 6-case state to 4
- the parser fix now classifies `PERF_0033` and `PERF_0054` as `taxonomy_trial_status=usable_for_current_slicing`
- both cases now carry `metadata_missing_flags=[]`
- both cases remain in the SQL-feature `untagged` bucket because `sql_feature_tags=[]` is an explicit empty assignment, not a missing tag gap
- both cases no longer remain in the portability `untagged` bucket because `limit_fetch_gap` is now parsed correctly from the v0.3 top-level field

## 7. Remaining Metadata Gaps / Caveats

- P0 hardening was applied only to `PERF_0033` and `PERF_0054`
- the current slicer still reports both P0 cases in the SQL-feature `untagged` bucket, but this now reflects explicit-empty / no-feature classification rather than a missing-tag gap
- the current slicer no longer reports either P0 case in the portability `untagged` bucket
- `CONS_0007` and `CONS_0012` still remain P2 hardening items
- `PORT_0004` remains provisional
- placeholder P1 taxonomy trials still exist
- this is not final taxonomy closure for RQ4

## 8. Claim Boundaries

- P0 hardening applied only for `PERF_0033` and `PERF_0054`
- no registry writeback
- no taxonomy vocabulary change
- no formal review update
- not final taxonomy closure
- remaining P1 and P2 taxonomy hardening still exists

## 9. Recommended Next Action

- review P1 placeholder/provisional taxonomy trials before treating RQ4 feature-level rates as final
