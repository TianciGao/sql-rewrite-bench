# First Pilot Results

## File role
This file records the **first paper-facing pre-pilot results slice** for the current SQL rewrite benchmark repository.

It is intended to summarize the currently stabilized evidence and provide a first results block for paper drafting.
It does **not** claim full pilot-scale completion.

---

## 1. Current interpretation

The repository now supports a controlled first evaluation slice.
At the current stage:

- total tracked cases: **12**
- first-slice cases: **8**
- stable anchors: **4**
- admitted external common-core cases: **2**
- tri-engine validated staged drafts: **2**

The current first-slice cases are:

**PERF_0001, PERF_0002, LONGTAIL_0001, CONS_0001, CONS_0003, CONS_0004, PORT_0001, PORT_0002**

This should be interpreted as a **pre-pilot stable reporting slice**, not as a claim of full benchmark completion.

---

## 2. Table 1 — Case maturity summary

| summary_group | count | case_ids | include_in_first_slice | notes |
| --- | --- | --- | --- | --- |
| stable_pilot_anchor | 4 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | yes | four stable anchors across all four pools |
| admitted_external_common_core | 2 | PERF_0002;PORT_0002 | yes | current admitted external common-core cases |
| staged_tri_engine_validated_draft | 2 | CONS_0003;CONS_0004 | yes | tri-engine validated but still not_yet_admitted |
| staged_partial_engine_closure_draft | 4 | PERF_0003;PERF_0004;LONGTAIL_0002;CONS_0002 | no | engine closure still incomplete or line intentionally kept partial |
| total_repository_cases | 12 | PERF_0001;PERF_0002;PERF_0003;PERF_0004;LONGTAIL_0001;LONGTAIL_0002;CONS_0001;CONS_0002;CONS_0003;CONS_0004;PORT_0001;PORT_0002 | n/a | current tracked case universe |
| first_slice_total | 8 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001;PERF_0002;PORT_0002;CONS_0003;CONS_0004 | yes | current pre-pilot evaluation slice |

### Interpretation
The current repository already exhibits a non-flat maturity structure:
- four stable pilot anchors,
- admitted external common-core cases,
- and staged drafts with different closure levels.

This supports the benchmark’s structural maturity argument even before full pilot-scale expansion.

---

## 3. Table 2 — Case-level maturity matrix

| case_id | pool | source_family | current_maturity | validated_engines | admitted_or_staged | include_in_first_slice | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | smoke/pipeline anchor |
| PERF_0002 | performance | TPC-DS | admitted_external_common_core | postgres;mysql;spark | admitted | yes | current strongest external performance case |
| PERF_0003 | performance | JOB | pg_only_staged_performance_draft | postgres | staged | no | JOB line currently frozen as partial realized supplement |
| PERF_0004 | performance | JOB | pg_validated_staged_performance_draft | postgres | staged | no | JOB line currently frozen as partial realized supplement |
| LONGTAIL_0001 | longtail | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | structure-rich longtail anchor |
| LONGTAIL_0002 | longtail | SQLStorm | pg_validated_staged_longtail_draft | postgres | staged | no | engine closure still missing |
| CONS_0001 | consistency | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | correctness anchor |
| CONS_0002 | consistency | Calcite | pg_validated_staged_consistency_draft | postgres | staged | no | broader engine validation still missing |
| CONS_0003 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes | tri-engine validated but still not_yet_admitted |
| CONS_0004 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes | tri-engine validated but still not_yet_admitted |
| PORT_0001 | portability | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | clean portability anchor |
| PORT_0002 | portability | PARROT | admitted_external_common_core | postgres;mysql;spark | admitted | yes | current strongest external portability case |

### Interpretation
The current first-slice inclusion boundary is intentionally conservative.
Only cases with sufficiently stable maturity and engine evidence are included.

---

## 4. Table 3 — Source-to-case materialization map

| source_family | source_role | current_source_status | materialized_cases | active_pool_alignment | current_line_interpretation | first_slice_usage | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| manual_seed | internal_seed_family | active | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | performance;longtail;consistency;portability | internal anchor source family | yes | not a formal fifth pool |
| TPC-H | performance_base | staged_partial_inspection | none | performance | target source without realized current case | no | resource present but not yet materialized into active case line |
| TPC-DS | performance_base | staged_and_inspected | PERF_0002 | performance | strongest current external performance line | yes | admitted external common-core case exists |
| SQLStorm | longtail_base | staged_and_inspected | LONGTAIL_0002 | longtail | primary longtail source but case line still staged | no | current first-slice exclusion due to engine closure gap |
| Stack | longtail_realism_substrate | dumps_only_realism_substrate | none | longtail | realism substrate only | no | not a direct SQL query corpus in current version |
| Calcite | consistency_base | staged_and_inspected | CONS_0002 | consistency | base consistency seed line | no | current case still PG-only staged draft |
| VeriEQL | consistency_supplement | accepted_and_materialized | CONS_0003;CONS_0004 | consistency | strongest current consistency supplement line | yes | both staged drafts now have tri-engine closure |
| PARROT | portability_base | staged_and_inspected | PORT_0002 | portability | strongest current external portability line | yes | admitted external common-core case exists |
| JOB | performance_supplement | partial_realized_frozen | PERF_0003;PERF_0004 | performance | partial realized supplement only | no | do not deepen further in current phase |
| DSB | performance_realism_candidate | unresolved_not_started | none | performance | still unresolved at source-decision layer | no | no acquisition or inspection started |
| SQLEquiQuest | alternative_consistency_candidate | not_selected | none | consistency | not active in current branch | no | VeriEQL is the selected supplement source |

### Interpretation
The benchmark is not being built as a flat SQL union.
Instead, different source families currently play different roles:
- anchors,
- admitted external case lines,
- staged draft lines,
- realism substrate lines,
- and unresolved target-only lines.

---

## 5. Table 4 — Engine-validation summary

| case_id | pool | current_maturity | postgres_validated | mysql_validated | spark_validated | result_artifacts_present | plan_artifacts_present | current_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | smoke/pipeline anchor |
| PERF_0002 | performance | admitted_external_common_core | yes | yes | yes | yes | yes | admitted | current strongest external performance case |
| LONGTAIL_0001 | longtail | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | structure-rich longtail anchor |
| CONS_0001 | consistency | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | correctness anchor |
| CONS_0003 | consistency | tri_engine_validated_staged_consistency_draft | yes | yes | yes | yes | yes | staged | tri-engine validated but still not_yet_admitted |
| CONS_0004 | consistency | tri_engine_validated_staged_consistency_draft | yes | yes | yes | yes | yes | staged | tri-engine validated but still not_yet_admitted |
| PORT_0001 | portability | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | clean portability anchor |
| PORT_0002 | portability | admitted_external_common_core | yes | yes | yes | yes | yes | admitted | current strongest external portability case |

### Interpretation
The first slice is intentionally restricted to cases with strong enough engine evidence.
In particular, the current first slice already includes:
- tri-engine anchors,
- admitted external tri-engine cases,
- and tri-engine validated staged consistency drafts.

This gives the repository meaningful early support for correctness-aware and cross-engine evaluation.

---

## 6. Current strongest takeaways

At the current repository stage, the strongest paper-facing takeaways are:

1. The benchmark already has a meaningful **four-pool structure**.
2. The repository already separates **anchor / admitted / staged** lines.
3. A stable **tri-engine evidence slice** already exists.
4. The consistency line already contains **tri-engine validated staged drafts**, showing that correctness is a first-class benchmark dimension.

---

## 7. Current non-claims

The current results should **not** be interpreted as evidence of:

- full pilot-scale completion,
- full source-universe closure,
- large-scale baseline comparison,
- broad workload curation completion,
- or benchmark expansion readiness.

These remain later-phase goals.

---

## 8. Immediate next step

The next step after this results snapshot should be to use these tables as the basis for:

- the first evaluation subsection draft,
- the first benchmark-characterization subsection,
- and the first appendix-style maturity summary block.

Only after that should the team decide whether to prioritize:
- selected source activation,
- controlled benchmark expansion,
- or baseline-comparison preparation.
