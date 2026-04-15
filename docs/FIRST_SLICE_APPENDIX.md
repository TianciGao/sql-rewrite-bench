# First Slice Appendix

## File role
This appendix summarizes the current **first-slice pre-pilot case subset** and its immediate exclusions.

It is intended to provide:
- a compact appendix-ready maturity summary,
- a clear included / excluded case boundary,
- and a stable reference block for early paper drafting.

This appendix does **not** claim full pilot completion.

---

## 1. Appendix summary table

| summary_group | count | case_ids | include_in_first_slice | notes |
| --- | --- | --- | --- | --- |
| stable_pilot_anchor | 4 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | yes | four stable anchors across all four pools |
| admitted_external_common_core | 2 | PERF_0002;PORT_0002 | yes | current admitted external common-core cases |
| staged_tri_engine_validated_draft | 2 | CONS_0003;CONS_0004 | yes | tri-engine validated but still not_yet_admitted |
| staged_partial_engine_closure_draft | 4 | PERF_0003;PERF_0004;LONGTAIL_0002;CONS_0002 | no | engine closure still incomplete or line intentionally kept partial |
| total_repository_cases | 12 | PERF_0001;PERF_0002;PERF_0003;PERF_0004;LONGTAIL_0001;LONGTAIL_0002;CONS_0001;CONS_0002;CONS_0003;CONS_0004;PORT_0001;PORT_0002 | n/a | current tracked case universe |
| first_slice_total | 8 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001;PERF_0002;PORT_0002;CONS_0003;CONS_0004 | yes | current pre-pilot evaluation slice |

---

## 2. Included first-slice cases

| case_id | pool | source_family | included_in_first_slice | reason_for_inclusion_or_exclusion | current_gap_if_excluded | notes |
| --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | manual_seed | yes | stable_anchor | n/a | smoke/pipeline anchor |
| LONGTAIL_0001 | longtail | manual_seed | yes | stable_anchor | n/a | structure-rich longtail anchor |
| CONS_0001 | consistency | manual_seed | yes | stable_anchor | n/a | correctness anchor |
| PORT_0001 | portability | manual_seed | yes | stable_anchor | n/a | clean portability anchor |
| PERF_0002 | performance | TPC-DS | yes | admitted_external_case | n/a | current strongest external performance case |
| PORT_0002 | portability | PARROT | yes | admitted_external_case | n/a | current strongest external portability case |
| CONS_0003 | consistency | VeriEQL | yes | tri_engine_consistency_draft | n/a | tri-engine validated but still staged |
| CONS_0004 | consistency | VeriEQL | yes | tri_engine_consistency_draft | n/a | tri-engine validated but still staged |

### Interpretation
These cases are included because they form the most stable currently available slice across:
- all four pools,
- stable anchors,
- admitted external cases,
- and tri-engine validated staged consistency drafts.

---

## 3. Excluded first-slice cases

| case_id | pool | source_family | included_in_first_slice | reason_for_inclusion_or_exclusion | current_gap_if_excluded | notes |
| --- | --- | --- | --- | --- | --- | --- |
| LONGTAIL_0002 | longtail | SQLStorm | no | engine_closure_missing | MySQL_and_Spark_closure_missing | valuable longtail case but not yet stable enough for first slice |
| CONS_0002 | consistency | Calcite | no | engine_closure_missing | broader_engine_validation_missing | still PG-only staged consistency draft |
| PERF_0003 | performance | JOB | no | partial_realized_supplement | MySQL_and_Spark_closure_missing | JOB line intentionally frozen as partial realized supplement |
| PERF_0004 | performance | JOB | no | partial_realized_supplement | MySQL_and_Spark_closure_missing | JOB line intentionally frozen as partial realized supplement |

### Interpretation
These cases are currently excluded not because they are unimportant, but because:
- engine closure remains incomplete,
- or the line is intentionally kept partial in the current phase.

---

## 4. Engine-validation appendix table

| case_id | pool | postgres_validated | mysql_validated | spark_validated | result_artifacts_present | plan_artifacts_present | current_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | yes | yes | yes | yes | yes | anchor |
| PERF_0002 | performance | yes | yes | yes | yes | yes | admitted |
| LONGTAIL_0001 | longtail | yes | yes | yes | yes | yes | anchor |
| CONS_0001 | consistency | yes | yes | yes | yes | yes | anchor |
| CONS_0003 | consistency | yes | yes | yes | yes | yes | staged |
| CONS_0004 | consistency | yes | yes | yes | yes | yes | staged |
| PORT_0001 | portability | yes | yes | yes | yes | yes | anchor |
| PORT_0002 | portability | yes | yes | yes | yes | yes | admitted |

### Interpretation
The first slice is intentionally restricted to cases with sufficiently stable engine evidence and artifact completeness.

---

## 5. Source-to-case appendix table

| source_family | current_source_status | materialized_cases | current_line_interpretation | first_slice_usage |
| --- | --- | --- | --- | --- |
| manual_seed | active | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | internal anchor source family | yes |
| TPC-H | staged_partial_inspection | none | target source without realized current case | no |
| TPC-DS | staged_and_inspected | PERF_0002 | strongest current external performance line | yes |
| SQLStorm | staged_and_inspected | LONGTAIL_0002 | primary longtail source but case line still staged | no |
| Stack | dumps_only_realism_substrate | none | realism substrate only | no |
| Calcite | staged_and_inspected | CONS_0002 | base consistency seed line | no |
| VeriEQL | accepted_and_materialized | CONS_0003;CONS_0004 | strongest current consistency supplement line | yes |
| PARROT | staged_and_inspected | PORT_0002 | strongest current external portability line | yes |
| JOB | partial_realized_frozen | PERF_0003;PERF_0004 | partial realized supplement only | no |
| DSB | unresolved_not_started | none | still unresolved at source-decision layer | no |
| SQLEquiQuest | not_selected | none | not active in current branch | no |

### Interpretation
This table highlights that the benchmark is already organized through source-family roles rather than simple flat query accumulation.

---

## 6. Case-maturity appendix table

| case_id | pool | source_family | current_maturity | validated_engines | admitted_or_staged | include_in_first_slice |
| --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes |
| PERF_0002 | performance | TPC-DS | admitted_external_common_core | postgres;mysql;spark | admitted | yes |
| PERF_0003 | performance | JOB | pg_only_staged_performance_draft | postgres | staged | no |
| PERF_0004 | performance | JOB | pg_validated_staged_performance_draft | postgres | staged | no |
| LONGTAIL_0001 | longtail | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes |
| LONGTAIL_0002 | longtail | SQLStorm | pg_validated_staged_longtail_draft | postgres | staged | no |
| CONS_0001 | consistency | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes |
| CONS_0002 | consistency | Calcite | pg_validated_staged_consistency_draft | postgres | staged | no |
| CONS_0003 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes |
| CONS_0004 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes |
| PORT_0001 | portability | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes |
| PORT_0002 | portability | PARROT | admitted_external_common_core | postgres;mysql;spark | admitted | yes |

### Interpretation
The appendix maturity table makes the repository boundary explicit:
- some cases are already stable enough for early reporting,
- while others remain intentionally staged.

---

## 7. Recommended current use

This appendix is most useful for:
- early appendix drafting,
- evaluation-section support,
- and explicit explanation of first-slice inclusion boundaries.

It should not be used to imply:
- full pilot-scale readiness,
- complete source-universe closure,
- or broad baseline-comparison readiness.
