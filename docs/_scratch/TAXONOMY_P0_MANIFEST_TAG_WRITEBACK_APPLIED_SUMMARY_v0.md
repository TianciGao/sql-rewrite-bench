# TAXONOMY_P0_MANIFEST_TAG_WRITEBACK_APPLIED_SUMMARY_v0

## 1. Status

This note records the bounded P0 manifest-only taxonomy tag writeback for `PERF_0033` and `PERF_0054`.

It is not registry writeback, taxonomy vocabulary change, formal review update, or final RQ4 closure.

## 2. Files Modified

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)

## 3. Governance Basis

- `taxonomy/*.yaml` remains the vocabulary layer
- `manifest.yaml` tags remain the stable case-level annotation layer
- `taxonomy_trial_v0.x.yaml` remains draft / review / hardening only
- `inventory/case_registry.csv` remains governance/status tracking rather than full taxonomy payload storage

## 4. PERF_0033 Manifest Tags Applied

- `sql_feature.primary=[]`
- `sql_feature.secondary=[]`
- `rewrite_opportunity.primary=[predicate_pushdown]`
- `rewrite_opportunity.secondary=[join_reorder]`
- `portability.confirmed=[limit_fetch_gap]`
- `portability.suspected=[]`
- `workload_realism.source_inherited=[classic_analytical_baseline]`
- `plan_operator.present=[scan, join, aggregate, sort, limit]`

Notes:

- explicit-empty SQL feature lists were preserved as reviewed no-feature decisions
- `date_time_function` was intentionally not added
- calendar dimension columns are not date/time functions

## 5. PERF_0054 Manifest Tags Applied

- `sql_feature.primary=[]`
- `sql_feature.secondary=[]`
- `rewrite_opportunity.primary=[join_reorder]`
- `rewrite_opportunity.secondary=[predicate_pushdown]`
- `portability.confirmed=[limit_fetch_gap]`
- `portability.suspected=[]`
- `workload_realism.source_inherited=[classic_analytical_baseline]`
- `plan_operator.present=[scan, join, aggregate, sort, limit]`

Notes:

- explicit-empty SQL feature lists were preserved as reviewed no-feature decisions
- `date_time_function` was intentionally not added
- calendar dimension columns are not date/time functions

## 6. Taxonomy Slicing Verification

After manifest writeback and rerunning taxonomy slicing:

- `PERF_0033` and `PERF_0054` remain usable for current slicing
- both remain explicit-empty SQL-feature cases rather than missing-tag cases
- both remain portability-tagged via `limit_fetch_gap`

Observed report counts:

- `sql_feature_gap_count=0`
- `portability_tag_gap_count=1`
- `workload_realism_gap_count=2`
- `taxonomy_trial_missing_count=4`
- `taxonomy_trial_placeholder_or_empty_count=5`
- `taxonomy_trial_provisional_count=1`

## 7. Remaining Metadata Caveats

- remaining metadata caveats outside this bounded P0 patch still exist
- P1 placeholder / provisional taxonomy-trial cases still require review
- P2 follow-up hardening still remains for later governance work

## 8. Claim Boundaries

- no registry writeback
- no taxonomy vocabulary change
- no formal review update
- not final RQ4 closure

## 9. Recommended Next Action

- review P1 placeholder / provisional taxonomy trials before treating RQ4 feature-level rates as final
