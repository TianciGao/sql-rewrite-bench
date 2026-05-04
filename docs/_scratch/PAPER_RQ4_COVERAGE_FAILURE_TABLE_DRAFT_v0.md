# PAPER_RQ4_COVERAGE_FAILURE_TABLE_DRAFT_v0

## 1. Status

This is a paper-facing RQ4 coverage / failure table draft based on current metadata and slicing outputs.

It is a draft table packet only.

It is not final RQ4.

## 2. Scope

- total cases currently sliced: `12`
- common-core cases: `9`
- PORT snapshot cases: `3`
- metadata exists for all `12` currently sliced cases
- tag quality varies across manifest tags, missing taxonomy trial files, placeholder trial files, and provisional trial files

## 3. Table 1: Coverage By Pool And Source Family

### 3.1 Coverage By Pool

| slice | count | interpretation |
|---|---:|---|
| common-core performance | `7` | current analytical speedup denominator and main performance evidence line |
| common-core consistency | `2` | semantic / consistency line; included in correctness and observability, excluded from first-pass `GM_Speedup` |
| PORT snapshot | `3` | bounded portability route status packet, separate from common-core |

### 3.2 Coverage By Source Family

| slice | count | interpretation |
|---|---:|---|
| `TPC-H` | `5` | strongest current analytical source-family block in the common-core packet |
| `TPC-DS` | `2` | smaller analytical performance subline |
| `Calcite` | `2` | consistency / subquery semantics subline |
| `PARROT` | `3` | current bounded portability source-family block |

## 4. Table 2: SQL Feature And Rewrite-Opportunity Buckets

### 4.1 SQL Feature Tags

| sql feature tag | count | interpretation note |
|---|---:|---|
| `date_time_function` | `8` | strongest cross-packet feature family; appears in both common-core and PORT evidence |
| `correlated_subquery` | `3` | concentrated in consistency and decorrelation-relevant cases |
| `expression_complexity` | `3` | appears in analytical and portability slices |
| `subquery_in_from` | `2` | smaller structural subquery slice |
| `untagged` | `2` | current metadata gap; do not over-interpret feature coverage rates |

### 4.2 Rewrite Opportunity Tags

| rewrite opportunity tag | count | interpretation note |
|---|---:|---|
| `predicate_pushdown` | `7` | dominant current common-core rewrite family |
| `join_reorder` | `4` | present across multiple analytical performance cases |
| `dialect_adaptation` | `3` | core current portability rewrite family |
| `function_normalization` | `3` | recurring portability-oriented rewrite theme |
| `materialization_strategy` | `3` | visible in both performance and consistency slices |
| `subquery_decorrelation` | `3` | concentrated in consistency / correlated-subquery cases |
| `expression_simplification` | `2` | smaller expression cleanup slice |
| `order_limit_simplification` | `1` | narrow current slice, not broad coverage |

## 5. Table 3: Claim Eligibility By Denominator Role

| claim eligibility | count | interpretation |
|---|---:|---|
| `main_table_correctness` | `9` | full common-core correctness line is closed |
| `plan_observability` | `9` | full common-core plan parse / pair-readiness line is closed |
| `main_table_perf_speedup` | `7` | current correctness-gated speedup packet is PERF-only |
| `not_yet_claimable` | `2` | `CONS_0007` and `CONS_0012` remain outside first-pass `GM_Speedup` |
| `port_snapshot` | `2` | clean current PORT snapshot cases: `PORT_0004`, `PORT_0022` |
| `failure_case_study` | `1` | `PORT_0012` is an explicit holdout failure-analysis case |

## 6. Table 4: Failure / Blocker Buckets

### 6.1 Common-Core Blocker / Evidence Buckets

| bucket | count | interpretation |
|---|---:|---|
| `generated_method_checker_backed_consistency_closed` | `9` | full common-core generated-method consistency is closed |
| `operator_delta_observed_not_attribution` | `9` | structural plan observations exist, but attribution is still absent |
| `attribution_not_computed` | `9` | common-core attribution remains a separate future layer |
| `registry_admission_not_claimed` | `9` | current packet is evidence only, not admission |
| `perf_only_speedup_completed` | `7` | current speedup evidence is closed for PERF denominator only |
| `speedup_policy_frozen` | `7` | PERF runtime / speedup policy is frozen for the current packet |
| `cons_excluded_from_gm_speedup` | `2` | current runtime packet excludes the two consistency cases |

### 6.2 PORT Failure Buckets

| bucket | count | interpretation |
|---|---:|---|
| `full_port_closure_not_claimed` | `3` | the current PORT line is still bounded, not closed |
| `registry_admission_not_claimed` | `3` | PORT evidence remains non-admission evidence |
| `port_invalid_datetime_format` | `1` | concrete execution-layer failure on `PORT_0012` |
| `quoted_identifier_vs_string_literal_confusion` | `1` | central failure mechanism for `PORT_0012` |
| `datetime_timestamp_formatting` | `1` | date/time formatting is part of the failure chain |
| `dialect_normalization_failure` | `1` | normalization / translation layer still unstable on holdout |
| `portability_translation_failure` | `1` | current holdout exemplifies translation failure risk |
| `port_holdout_failure_analysis` | `1` | `PORT_0012` remains an intentional failure-study case |

Interpretation for `PORT_0012`:

- it is the anchor portability failure-analysis case in the current packet
- it illustrates dialect normalization and datetime handling failure rather than generic infra failure

## 7. Table 5: Metadata / Taxonomy Caveats

| caveat | count | interpretation |
|---|---:|---|
| `sql_feature_gap_count` | `2` | some cases still lack complete SQL feature assignment |
| `portability_tag_gap_count` | `3` | portability-theme coverage is incomplete outside the strongest tagged cases |
| `workload_realism_gap_count` | `2` | realism slicing is currently partial |
| `taxonomy_trial_missing_count` | `6` | many cases depend on manifest tags without a trial file |
| `taxonomy_trial_placeholder_or_empty_count` | `5` | several trial files are scaffolds, not usable evidence |
| `taxonomy_trial_provisional_count` | `1` | at least one case has explicit provisional trial tags |

Important caveat:

- missing and provisional tags are reported, not repaired
- feature-level rates are only as complete as current metadata
- taxonomy slicing is not final taxonomy writeback

## 8. RQ4 Interpretation Draft

The current benchmark slice spans performance, consistency, and bounded portability evidence across `12` currently aggregated cases. Date/time-oriented SQL and predicate-driven rewrite families are prominent in the present packet, while correlated-subquery and decorrelation structure anchor the smaller consistency line. The failure / blocker slicing now exposes both evidence closure and remaining blockers: common-core generated-method consistency and plan observability are closed on the current denominator, PERF-only correctness-gated speedup is closed for the current runtime packet, and `PORT_0012` provides a concrete dialect-normalization and datetime failure study. Final feature-level claims still require metadata hardening because several taxonomy trial files remain missing, placeholder, or provisional.

## 9. What Cannot Yet Be Claimed

- final RQ4 coverage map
- final taxonomy coverage percentages
- registry-backed taxonomy writeback
- full PORT closure
- attribution-based failure explanation
- final leaderboard

## 10. Recommended Next Action

- harden taxonomy metadata for cases with missing / placeholder / provisional taxonomy_trial files before treating RQ4 feature-level rates as final

## 11. Verification / Non-Modification Note

- only this table draft was created
- no SQL / database / model / SQLGlot / checker execution occurred
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- no taxonomy writeback occurred
- taxonomy calibration notes were untouched
