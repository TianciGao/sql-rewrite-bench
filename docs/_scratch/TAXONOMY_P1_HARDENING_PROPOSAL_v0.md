# TAXONOMY_P1_HARDENING_PROPOSAL_v0

## 1. Status

This is a scratch P1 taxonomy hardening proposal for the current RQ4 sliced cases.

It is a proposal only, not taxonomy writeback.

## 2. Governance Basis

The current source-of-truth hierarchy remains:

- `taxonomy/*.yaml`
  - vocabulary and definition layer
- `manifest.yaml` tags
  - stable case-level annotation layer
- `taxonomy_trial_v0.x.yaml`
  - draft / review / hardening layer
- `inventory/case_registry.csv`
  - live status and governance facts only

P0 governance is already closed for `PERF_0033` and `PERF_0054` through bounded manifest writeback.

P1 should therefore focus on cases where draft slicing is already possible, but the draft taxonomy layer is still placeholder or provisional.

## 3. P1 Scope

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PORT_0004`

## 4. Per-Case Proposal Table

| case_id | current trial status | current manifest tag adequacy | metadata gaps | proposed action | claim risk after action |
|---|---|---|---|---|---|
| `PERF_0006` | `placeholder_or_empty` | adequate for current draft slicing | `taxonomy_trial_placeholder_or_empty` | `taxonomy_trial_normalization_needed` | low |
| `PERF_0008` | `placeholder_or_empty` | adequate for current draft slicing | `taxonomy_trial_placeholder_or_empty` | `taxonomy_trial_normalization_needed` | low |
| `PERF_0013` | `placeholder_or_empty` | adequate for current draft slicing | `taxonomy_trial_placeholder_or_empty` | `taxonomy_trial_normalization_needed` | low |
| `PERF_0017` | `placeholder_or_empty` | adequate for current draft slicing | `taxonomy_trial_placeholder_or_empty` | `taxonomy_trial_normalization_needed` | low |
| `PERF_0024` | `placeholder_or_empty` | adequate for current draft slicing | `taxonomy_trial_placeholder_or_empty` | `taxonomy_trial_normalization_needed` | low |
| `PORT_0004` | `provisional` | adequate for current draft slicing | `taxonomy_trial_provisional` | `keep_provisional_pending_review` | medium |

Interpretation:

- none of the current P1 cases require immediate stable manifest tag writeback to support the current draft slicer
- the five TPC-H PERF cases mainly need `taxonomy_trial` normalization because the manifest tag layer is already populated
- `PORT_0004` should remain reviewer-gated because its trial file is narrower and more tentative than the manifest tag layer

## 5. Detailed Case Notes

### 5.1 `PERF_0006`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/manifest.yaml)
- [taxonomy_trial_v0.2.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/taxonomy_trial_v0.2.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[date_time_function, expression_complexity]`
- `rewrite_opportunity_tags=[predicate_pushdown, materialization_strategy]`
- `portability_tags=[datetime_semantics_gap, type_semantics_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags=[scan, aggregate, sort]`

Proposal:

- no manifest writeback needed now
- replace placeholder `taxonomy_trial_v0.2.yaml` with a normalized review draft aligned to current manifest tags

Evidence notes:

- `l_shipdate <= date '1998-08-27'` supports `date_time_function` only because the current vocabulary and manifest already classify explicit date literal/date-type usage here
- aggregation-heavy scan / aggregate / sort shape is already reflected in current plan tags
- portability concerns are already represented in manifest suspected tags

Caveats:

- if reviewers want a stricter interpretation of `date_time_function`, they should resolve that vocabulary decision consistently across the TPC-H date-filtered PERF cases rather than case-by-case

### 5.2 `PERF_0008`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/manifest.yaml)
- [taxonomy_trial_v0.2.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/taxonomy_trial_v0.2.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[date_time_function, subquery_in_from]`
- `rewrite_opportunity_tags=[predicate_pushdown, materialization_strategy]`
- `portability_tags=[datetime_semantics_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags=[scan, join, aggregate, sort, limit]`

Proposal:

- no manifest writeback needed now
- replace placeholder `taxonomy_trial_v0.2.yaml` with a normalized review draft aligned to current manifest tags

Evidence notes:

- date predicates and limiting behavior are already represented by current manifest-derived tags
- join / aggregate / sort / limit operator evidence is already present in current plan metadata

Caveats:

- do not promote `limit` into a SQL-feature tag solely because the query uses `LIMIT 10`; current evidence only supports it as plan/operator and portability-adjacent structure

### 5.3 `PERF_0013`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0013/manifest.yaml)
- [taxonomy_trial_v0.2.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0013/taxonomy_trial_v0.2.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0013/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[date_time_function]`
- `rewrite_opportunity_tags=[predicate_pushdown, join_reorder]`
- `portability_tags=[datetime_semantics_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags=[scan, join, aggregate, sort]`

Proposal:

- no manifest writeback needed now
- replace placeholder `taxonomy_trial_v0.2.yaml` with a normalized review draft aligned to current manifest tags

Evidence notes:

- explicit interval arithmetic and date-bound filtering support the current date/time classification
- multi-join analytical structure supports the current rewrite and operator tags

Caveats:

- if later reviewers want to split date-literal usage from function-like temporal semantics, that should be a vocabulary-level review rather than a one-off manifest rewrite

### 5.4 `PERF_0017`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0017/manifest.yaml)
- [taxonomy_trial_v0.2.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0017/taxonomy_trial_v0.2.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0017/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[date_time_function]`
- `rewrite_opportunity_tags=[predicate_pushdown, join_reorder]`
- `portability_tags=[datetime_semantics_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags=[scan, join, aggregate, sort, limit]`

Proposal:

- no manifest writeback needed now
- replace placeholder `taxonomy_trial_v0.2.yaml` with a normalized review draft aligned to current manifest tags

Evidence notes:

- month-window date filtering supports the current temporal classification
- join / aggregate / sort / limit structure is already encoded in manifest tags and plan summaries

Caveats:

- keep `date_time_function` only because the current stable manifest layer already uses that label consistently across similar temporal-filter TPC-H cases

### 5.5 `PERF_0024`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0024/manifest.yaml)
- [taxonomy_trial_v0.2.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0024/taxonomy_trial_v0.2.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0024/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[correlated_subquery, date_time_function]`
- `rewrite_opportunity_tags=[subquery_decorrelation, predicate_pushdown]`
- `portability_tags=[datetime_semantics_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags=[scan, join, aggregate, sort, materialize]`

Proposal:

- no manifest writeback needed now
- replace placeholder `taxonomy_trial_v0.2.yaml` with a normalized review draft aligned to current manifest tags

Evidence notes:

- nested `IN` plus correlated aggregate subquery supports `correlated_subquery`
- date range predicate using interval arithmetic supports the current temporal tag
- `subquery_decorrelation` is the central rewrite opportunity

Caveats:

- do not dilute this case by flattening it into a generic date-filter case; the correlated subquery signal is the stronger differentiator

### 5.6 `PORT_0004`

Evidence inspected:

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0004/manifest.yaml)
- [taxonomy_trial_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0004/taxonomy_trial_v0.3.yaml)
- [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0004/source.sql)
- `reports/formal_common_core/taxonomy_slicing_v0.json`

Current slicer tags:

- `sql_feature_tags=[date_time_function, expression_complexity]`
- `rewrite_opportunity_tags=[dialect_adaptation, function_normalization, expression_simplification]`
- `portability_tags=[identifier_quoting, datetime_semantics_gap, type_semantics_gap]`
- `workload_realism_tags=[realistic_query_style, complex_expression_density]`
- `plan_operator_tags=[scan, filter, aggregate]`

Proposal:

- keep provisional pending review
- no manifest writeback needed now
- later normalize the trial file only after reviewer confirms whether it should match the richer manifest tags or intentionally remain narrower

Evidence notes:

- `DATE_FORMAT(CAST(... AS DATETIME), '%Y')` is a real date/time function case
- quoting, type coercion, and datetime semantics are central portability issues here
- current manifest tags are already richer than the provisional trial file

Caveats:

- this is a portability-governance case, not a performance-speedup case
- trial normalization should not erase the reviewer-facing distinction between confirmed portability signals and still-reviewable portability interpretation

## 6. P1 Grouping

### Apply Manifest Writeback Proposal Next

- none

Reason:

- current stable manifest tag layers for all six P1 cases are already adequate for current draft slicing

### Normalize `taxonomy_trial` Only

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`

Reason:

- each case has a placeholder `taxonomy_trial_v0.2.yaml`
- current slicer tags already come from the manifest layer
- the hardening need is draft-layer normalization, not another manifest writeback

### No Action Needed

- none

Reason:

- all six P1 cases still carry either placeholder or provisional trial-state risk

### Keep Provisional Pending Reviewer Decision

- `PORT_0004`

Reason:

- the manifest layer is already useful
- the trial file is narrower and explicitly draft-only
- reviewer intent should be clarified before normalizing it into a stronger draft or mirroring the manifest layer

## 7. Recommended Next Action

- create a bounded manifest-writeback proposal only for P1 cases that require stable manifest tag updates

## 8. Claim Boundaries

- no manifest changes
- no taxonomy writeback
- no registry writeback
- no formal review update
- no final RQ4 claim

## 9. Verification / Non-Modification Note

- only this proposal was created
- no case files were modified
- no taxonomy files were modified
- no registry files were modified
- no SQL or database workload was run
- no model or LLM call was made
- no SQLGlot execution or generation was run
- no checker was run
- taxonomy calibration notes were untouched
