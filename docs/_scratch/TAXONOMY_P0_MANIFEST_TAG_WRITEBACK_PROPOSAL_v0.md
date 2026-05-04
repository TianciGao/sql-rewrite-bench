# TAXONOMY_P0_MANIFEST_TAG_WRITEBACK_PROPOSAL_v0

## 1. Status

This is a scratch manifest tag writeback proposal for the current P0 cases only.

It is not applied metadata.

## 2. Governance Basis

The current governance basis is:

- `taxonomy/*.yaml`
  - defines the allowed vocabulary and tag meaning
- `manifest.yaml` tags
  - intended stable case-level annotation layer
- `taxonomy_trial_v0.x.yaml`
  - draft / review / hardening layer used before stable case metadata is updated
- `inventory/case_registry.csv`
  - tracks live status and governance facts
  - is not the full taxonomy payload store

This proposal exists because the P0 trial tags are now usable for current slicing, but they have not yet been promoted into stable manifest-level case annotation.

## 3. Scope

- `PERF_0033`
- `PERF_0054`

## 4. PERF_0033 Proposal

### 4.1 Current Evidence Inspected

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/manifest.yaml)
- [taxonomy_trial_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0033/taxonomy_trial_v0.3.yaml)
- [sql_feature_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/sql_feature_taxonomy_v0.3.yaml)
- [rewrite_opportunity_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml)
- [portability_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/portability_taxonomy_v0.3.yaml)
- [plan_operator_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/plan_operator_taxonomy_v0.3.yaml)
- [workload_realism_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/workload_realism_taxonomy_v0.3.yaml)

### 4.2 Current Manifest Tag Status

Current manifest status:

- `sql_feature.primary=[]`
- `sql_feature.secondary=[]`
- `rewrite_opportunity.primary=[predicate_pushdown]`
- `rewrite_opportunity.secondary=[join_reorder]`
- `plan_operator.present=[scan, join, aggregate, sort, limit]`
- `workload_realism.source_inherited=[classic_analytical_baseline]`
- `portability.confirmed=[]`
- `portability.suspected=[]`

Interpretation:

- rewrite, plan, and workload realism tags are already close to the reviewed P0 outcome
- portability is still missing the reviewed `limit_fetch_gap`
- SQL feature is already represented as explicit empty in the manifest’s current nested schema

### 4.3 Current `taxonomy_trial_v0.3` Status

Current trial status:

- `status=p0_taxonomy_hardened_draft`
- `sql_feature_tags=[]`
- `rewrite_opportunity_tags=[predicate_pushdown, join_reorder]`
- `portability_tags=[limit_fetch_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags.observed_in_postgres=[scan, join, aggregate, sort, limit]`

### 4.4 Proposed Stable Manifest Tags Block

Proposal only:

```yaml
tags:
  sql_feature:
    primary: []
    secondary: []
  rewrite_opportunity:
    primary:
      - predicate_pushdown
    secondary:
      - join_reorder
  plan_operator:
    present:
      - scan
      - join
      - aggregate
      - sort
      - limit
    delta_relevant: []
  workload_realism:
    source_inherited:
      - classic_analytical_baseline
    case_specific: []
  portability:
    confirmed:
      - limit_fetch_gap
    suspected: []
```

### 4.5 Evidence Notes

- explicit-empty `sql_feature_tags`
  - evidence source:
    - `source.sql` structure reviewed during P0 hardening
    - current `taxonomy_trial_v0.3.yaml`
    - current manifest nested `sql_feature` block already encodes an empty reviewed state
  - note:
    - keep this as explicit empty, not missing
- `predicate_pushdown`
  - evidence source:
    - manifest and P0 trial alignment
    - selective predicates on manager and calendar filters
- `join_reorder`
  - evidence source:
    - manifest and P0 trial alignment
    - multi-relation analytical join shape
- `limit_fetch_gap`
  - evidence source:
    - source comments note normalization from `TOP 100` to `LIMIT 100`
    - portability taxonomy explicitly treats row-limiting syntax/semantics as `limit_fetch_gap`
- `classic_analytical_baseline`
  - evidence source:
    - TPC-DS origin and current manifest inherited workload realism tag
- `scan`, `join`, `aggregate`, `sort`, `limit`
  - evidence source:
    - current manifest plan operator block
    - existing PG plan evidence already summarized in manifest / trial review

### 4.6 Caveats

- do not add `date_time_function`
  - the query uses calendar dimension columns, not explicit date/time functions
- plan operator tags remain acceptable only if reviewer agrees that existing PG plan evidence is sufficient for stable manifest tagging
- proposal should be written only after confirming manifest tag schema expectations for explicit-empty SQL-feature representation

### 4.7 Writeback Readiness

- recommended status: ready after bounded review

## 5. PERF_0054 Proposal

### 5.1 Current Evidence Inspected

- [manifest.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/manifest.yaml)
- [taxonomy_trial_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0054/taxonomy_trial_v0.3.yaml)
- [sql_feature_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/sql_feature_taxonomy_v0.3.yaml)
- [rewrite_opportunity_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml)
- [portability_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/portability_taxonomy_v0.3.yaml)
- [plan_operator_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/plan_operator_taxonomy_v0.3.yaml)
- [workload_realism_taxonomy_v0.3.yaml](/home/tianci_gao/code/sql-rewrite-bench/taxonomy/workload_realism_taxonomy_v0.3.yaml)

### 5.2 Current Manifest Tag Status

Current manifest status:

- `sql_feature.primary=[]`
- `sql_feature.secondary=[]`
- `rewrite_opportunity.primary=[join_reorder]`
- `rewrite_opportunity.secondary=[predicate_pushdown]`
- `plan_operator.present=[scan, join, aggregate, sort, limit]`
- `workload_realism.source_inherited=[classic_analytical_baseline]`
- `portability.confirmed=[]`
- `portability.suspected=[]`

Interpretation:

- rewrite, plan, and workload realism tags are already aligned with the reviewed P0 trial
- portability is still missing the reviewed `limit_fetch_gap`
- SQL feature is already represented as explicit empty in the manifest’s current nested schema

### 5.3 Current `taxonomy_trial_v0.3` Status

Current trial status:

- `status=p0_taxonomy_hardened_draft`
- `sql_feature_tags=[]`
- `rewrite_opportunity_tags=[join_reorder, predicate_pushdown]`
- `portability_tags=[limit_fetch_gap]`
- `workload_realism_tags=[classic_analytical_baseline]`
- `plan_operator_tags.observed_in_postgres=[scan, join, aggregate, sort, limit]`

### 5.4 Proposed Stable Manifest Tags Block

Proposal only:

```yaml
tags:
  sql_feature:
    primary: []
    secondary: []
  rewrite_opportunity:
    primary:
      - join_reorder
    secondary:
      - predicate_pushdown
  plan_operator:
    present:
      - scan
      - join
      - aggregate
      - sort
      - limit
    delta_relevant: []
  workload_realism:
    source_inherited:
      - classic_analytical_baseline
    case_specific: []
  portability:
    confirmed:
      - limit_fetch_gap
    suspected: []
```

### 5.5 Evidence Notes

- explicit-empty `sql_feature_tags`
  - evidence source:
    - current trial file
    - current manifest nested empty block
    - SQL review determined no high-signal SQL feature tag should be forced here
- `join_reorder`
  - evidence source:
    - current manifest and current trial agree
    - multi-table analytical join structure
- `predicate_pushdown`
  - evidence source:
    - current manifest and current trial agree
    - selective manufacturer and month filters support pushdown opportunity
- `limit_fetch_gap`
  - evidence source:
    - source comments note normalization from `TOP 100` to `LIMIT 100`
- `classic_analytical_baseline`
  - evidence source:
    - TPC-DS origin and current manifest inherited workload realism tag
- `scan`, `join`, `aggregate`, `sort`, `limit`
  - evidence source:
    - current manifest plan operator block
    - existing PG plan evidence summarized in current metadata

### 5.6 Caveats

- do not add `date_time_function`
  - `d_year` and `d_moy` are calendar dimension columns, not explicit date/time functions
- this proposal should not be read as registry admission, common-core admission, or formal review completion
- stable writeback should happen only after bounded review confirms that manifest nested tag schema remains the intended stable representation

### 5.7 Writeback Readiness

- recommended status: ready after bounded review

## 6. Proposed Writeback Format

Generic proposed manifest insertion format, shown for schema alignment only:

```yaml
tags:
  sql_feature:
    primary: []
    secondary: []
  rewrite_opportunity:
    primary:
      - <primary_rewrite_tag>
    secondary:
      - <secondary_rewrite_tag>
  plan_operator:
    present:
      - <operator_tag>
    delta_relevant: []
  workload_realism:
    source_inherited:
      - <source_level_or_inherited_realism_tag>
    case_specific: []
  portability:
    confirmed:
      - <confirmed_portability_tag>
    suspected: []
```

This block is proposal only.

It must not be treated as already applied metadata.

## 7. Reviewer Checklist Before Applying

- confirm manifest tag schema still expects nested `tags` blocks for:
  - `sql_feature`
  - `rewrite_opportunity`
  - `plan_operator`
  - `workload_realism`
  - `portability`
- confirm explicit-empty SQL-feature representation should remain:
  - `primary: []`
  - `secondary: []`
- confirm `date_time_function` should remain absent for both cases
- confirm `plan_operator` tags are acceptable from existing PG plan evidence
- confirm no registry writeback is required for this bounded manifest-only update

## 8. Recommended Next Action

- after review, apply a bounded manifest tag writeback patch for `PERF_0033` and `PERF_0054` only

## 9. Claim Boundaries

- no manifest changes
- no taxonomy writeback
- no registry writeback
- no formal review update
- no final RQ4 claim

## 10. Verification / Non-Modification Note

- only this proposal was created
- no case files were modified
- no taxonomy vocabulary files were modified
- no registry files were modified
- no SQL or database workload was run
- no model or LLM call was made
- no SQLGlot execution or generation was run
- no checker was run
- taxonomy calibration notes were untouched
