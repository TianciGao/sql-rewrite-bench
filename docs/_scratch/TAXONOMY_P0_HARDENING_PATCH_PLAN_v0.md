# TAXONOMY_P0_HARDENING_PATCH_PLAN_v0

## 1. Status

This is a tracked scratch patch plan for RQ4 taxonomy metadata hardening on the current P0 cases only:

- `PERF_0033`
- `PERF_0054`

This is only a patch plan.

It is not taxonomy writeback, not registry writeback, and not a case modification.

## 2. Why This Plan Exists

The current RQ4 hardening plan identifies `PERF_0033` and `PERF_0054` as the clearest P0 blockers for final feature-level slicing quality.

Both cases currently have:

- missing `taxonomy_trial*.yaml`
- empty / missing `sql_feature_tags`
- empty / missing `portability_tags`

Both cases already have enough local evidence to define a bounded patch proposal without touching `cases/`, `taxonomy/`, or registry files.

## 3. Patch Target Convention

If later applied, the proposed case-local target filename for both cases should be:

- `cases/PERF/PERF_0033/taxonomy_trial_v0.3.yaml`
- `cases/PERF/PERF_0054/taxonomy_trial_v0.3.yaml`

This document does not create those files.

## 4. Proposed Patch: PERF_0033

### 4.1 Case Summary

- `case_id`: `PERF_0033`
- `pool`: `performance`
- `source_family`: `TPC-DS`
- `source basis`: `query55.tpl`, PostgreSQL-normalized from TPC-DS ANSI materialization

### 4.2 Proposed Tag Payload

- `taxonomy_trial target filename`:
  - `cases/PERF/PERF_0033/taxonomy_trial_v0.3.yaml`
- `sql_feature_tags`:
  - proposed primary: none
  - proposed secondary: none
- `rewrite_opportunity_tags`:
  - primary:
    - `predicate_pushdown`
  - secondary:
    - `join_reorder`
- `portability_tags`:
  - confirmed:
    - `limit_fetch_gap`
- `workload_realism_tags`:
  - `classic_analytical_baseline`
- `plan_operator_tags`:
  - `scan`
  - `join`
  - `aggregate`
  - `sort`
  - `limit`

### 4.3 Evidence Sources

- `sql_feature_tags`:
  - evidence source:
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/source.sql)
    - [sql_feature_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/sql_feature_taxonomy_v0.3.yaml)
  - rationale:
    - the query is a flat join + aggregate + order + limit pattern
    - no `cte`, `recursive_cte`, `correlated_subquery`, `subquery_in_from`, `outer_join`, `non_equi_join`, `window_function`, `set_operation`, `grouping_sets`, or `deep_nesting` evidence is present
    - `limit 100` is not strong evidence for `large_limit`
  - consequence:
    - the patch should explicitly record an intentionally empty SQL-feature assignment rather than leaving the category unspecified

- `rewrite_opportunity_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/source.sql)
    - [rewrite_opportunity_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml)
  - rationale:
    - selective predicates on `i_manager_id`, `d_moy`, and `d_year` support `predicate_pushdown`
    - multi-relation join shape supports `join_reorder`

- `portability_tags`:
  - evidence source:
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/source.sql)
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
    - [portability_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/portability_taxonomy_v0.3.yaml)
  - rationale:
    - source comments explicitly note PostgreSQL normalization from `TOP 100` to `LIMIT 100`
    - that is direct evidence for `limit_fetch_gap`
    - no stronger evidence was found for `datetime_semantics_gap`, `type_semantics_gap`, or `engine_specific_syntax_gap`

- `workload_realism_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
  - rationale:
    - inherited TPC-DS analytical benchmark structure matches `classic_analytical_baseline`

- `plan_operator_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
  - rationale:
    - existing plan evidence is already summarized in manifest tags and `plan_checked: true`
    - the patch can reuse that case-local plan operator set without re-reading or recomputing plan artifacts

### 4.4 Confidence and Reviewer Notes

- `confidence level`: medium-high
- reviewer notes / caveats:
  - the strongest positive addition is `limit_fetch_gap`
  - the SQL-feature proposal is mostly a deliberate explicit-empty classification, not a positive tag expansion
  - if later reviewers want a stricter policy against empty SQL-feature payloads, they should first clarify whether “flat analytical aggregate/join/order/limit” needs a dedicated tag family in taxonomy, rather than improvising one here

## 5. Proposed Patch: PERF_0054

### 5.1 Case Summary

- `case_id`: `PERF_0054`
- `pool`: `performance`
- `source_family`: `TPC-DS`
- `source basis`: `query3.tpl`, PostgreSQL-normalized from TPC-DS ANSI materialization

### 5.2 Proposed Tag Payload

- `taxonomy_trial target filename`:
  - `cases/PERF/PERF_0054/taxonomy_trial_v0.3.yaml`
- `sql_feature_tags`:
  - proposed primary: none
  - proposed secondary: none
- `rewrite_opportunity_tags`:
  - primary:
    - `join_reorder`
  - secondary:
    - `predicate_pushdown`
- `portability_tags`:
  - confirmed:
    - `limit_fetch_gap`
- `workload_realism_tags`:
  - `classic_analytical_baseline`
- `plan_operator_tags`:
  - `scan`
  - `join`
  - `aggregate`
  - `sort`
  - `limit`

### 5.3 Evidence Sources

- `sql_feature_tags`:
  - evidence source:
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/source.sql)
    - [sql_feature_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/sql_feature_taxonomy_v0.3.yaml)
  - rationale:
    - the query remains a flat analytical join + group + order + limit shape
    - no direct evidence appears for the named SQL feature tags in v0.3
    - `d_year` and `d_moy` are date-dimension columns, not date/time functions

- `rewrite_opportunity_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/source.sql)
    - [rewrite_opportunity_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml)
  - rationale:
    - multi-table analytical join structure supports `join_reorder`
    - selective filters on `i_manufact_id` and `d_moy` support `predicate_pushdown`

- `portability_tags`:
  - evidence source:
    - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/source.sql)
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)
    - [portability_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/portability_taxonomy_v0.3.yaml)
  - rationale:
    - source comments explicitly note normalization from `TOP 100` to `LIMIT 100`
    - that is direct evidence for `limit_fetch_gap`
    - no additional portability tag is strongly supported by the visible SQL text alone

- `workload_realism_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)
  - rationale:
    - inherited TPC-DS workload profile supports `classic_analytical_baseline`

- `plan_operator_tags`:
  - evidence source:
    - [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)
  - rationale:
    - manifest already records `scan`, `join`, `aggregate`, `sort`, and `limit`

### 5.4 Confidence and Reviewer Notes

- `confidence level`: medium-high
- reviewer notes / caveats:
  - as with `PERF_0033`, the main hardening value is making the empty SQL-feature decision explicit and filling the portability gap with a defensible tag
  - do not over-tag `date_time_function`; the query references calendar dimension columns, but does not call a date/time function

## 6. Cross-Case Reviewer Guidance

- prefer explicit empty `sql_feature_tags` over silent omission if no taxonomy v0.3 SQL feature clearly applies
- keep `rewrite_opportunity_tags` aligned with current manifest intent unless later plan-attribution work proves otherwise
- use `limit_fetch_gap` only because the source comments explicitly document `TOP` to `LIMIT` normalization
- do not infer broader portability tags without direct SQL or provenance evidence

## 7. Proposed Minimal Patch Shape

If later converted into an actual bounded patch, each case-local `taxonomy_trial_v0.3.yaml` should minimally include:

- case identity
- provenance / status marker that it is a trial taxonomy file
- explicit `sql_feature_tags`
- `rewrite_opportunity_tags`
- `portability_tags`
- `workload_realism_tags`
- `plan_operator_tags`
- short reviewer notes citing source SQL, manifest tags, and taxonomy definitions

## 8. Claim Boundaries

- this is not a patch application
- this does not create any `taxonomy_trial*.yaml`
- this does not modify `cases/`
- this does not modify `taxonomy/`
- this does not modify registry
- this does not finalize RQ4 rates

## 9. Verification / Non-Modification Note

- only this patch plan was created
- no SQL or database workload was run
- no model or LLM call was made
- no SQLGlot execution or generation was run
- no checker was run
- no case files were changed
- no taxonomy files were changed
- no registry files were changed
- taxonomy calibration notes were untouched
