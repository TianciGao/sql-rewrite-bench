# Common-core v0.3 Candidate Slate

## Executive Summary

This document records a Common-core v0.3 40-case candidate slate assembled from the existing curation reports only. It is a selection-review input, not a final admission action, and it does not update registry facts.

The candidate slate preserves the target pool mix:

- `PERF`: `16`
- `CONS`: `9`
- `PORT`: `9`
- `LONGTAIL`: `6`

## Final 40-case Candidate Table

| case_id | pool | source_family | evidence_status | preflight_basis | human_review_required | proposed_common_core_role | replacement_history |
|---|---|---|---|---|---|---|---|
| `PERF_0006` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0007` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0008` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0013` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0017` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0019` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0024` | `performance` | `TPC-H` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0033` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0034` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0035` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0052` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0054` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0056` | `performance` | `TPC-DS` | `complete_for_selection_review` | `artifact_preflight:complete_for_selection_review` | `no` | `perf_core_candidate` | - |
| `PERF_0062` | `performance` | `TPC-DS` | `strong_replacement` | `replacement_preflight:strong_replacement` | `yes` | `perf_replacement_candidate` | `replaces PERF_0002` |
| `PERF_0077` | `performance` | `JOB/IMDB` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `perf_real_schema_bridge_candidate` | - |
| `PERF_0082` | `performance` | `JOB/IMDB` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `perf_real_schema_bridge_candidate` | - |
| `CONS_0005` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0007` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0009` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0010` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0011` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0012` | `consistency` | `Calcite` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0024` | `consistency` | `Calcite` | `acceptable_with_manual_review` | `replacement_preflight:acceptable_with_manual_review` | `yes` | `consistency_replacement_candidate` | `replaces CONS_0001` |
| `CONS_0036` | `consistency` | `VeriEQL` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `CONS_0037` | `consistency` | `VeriEQL` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `consistency_semantics_candidate` | - |
| `PORT_0003` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0004` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0005` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0008` | `portability` | `PARROT` | `acceptable_with_manual_review` | `replacement_preflight:acceptable_with_manual_review` | `yes` | `portability_replacement_candidate` | `replaces PORT_0002` |
| `PORT_0012` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0013` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0022` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0024` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `PORT_0025` | `portability` | `PARROT` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `portability_stress_candidate` | - |
| `LONGTAIL_0022` | `longtail` | `Stack Queries` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `longtail_stack_substrate_candidate` | - |
| `LONGTAIL_0023` | `longtail` | `Stack Queries` | `acceptable_with_manual_review` | `replacement_preflight:acceptable_with_manual_review` | `yes` | `longtail_stack_substrate_candidate` | `replaces LONGTAIL_0001` |
| `LONGTAIL_0024` | `longtail` | `Stack Queries` | `needs_manual_review` | `artifact_preflight:needs_manual_review` | `yes` | `longtail_stack_substrate_candidate` | - |
| `LONGTAIL_0011` | `longtail` | `SQLStorm` | `strong_longtail_review_candidate` | `longtail_review_prep:strong_longtail_review_candidate` | `yes` | `longtail_sqlstorm_diversity_candidate` | `replaces LONGTAIL_0003` |
| `LONGTAIL_0012` | `longtail` | `SQLStorm` | `strong_longtail_review_candidate` | `longtail_review_prep:strong_longtail_review_candidate` | `yes` | `longtail_sqlstorm_diversity_candidate` | `replaces LONGTAIL_0004` |
| `LONGTAIL_0013` | `longtail` | `SQLStorm` | `strong_longtail_review_candidate` | `longtail_review_prep:strong_longtail_review_candidate` | `yes` | `longtail_sqlstorm_diversity_candidate` | `replaces LONGTAIL_0016` |

## Per-pool Summary

| pool | count | dominant evidence mode | source families |
|---|---:|---|---|
| `performance` | `16` | `13` direct keepers, `1` strong replacement, `2` manual real-schema bridges | `TPC-H=7`, `TPC-DS=7`, `JOB/IMDB=2` |
| `consistency` | `9` | all `manual review` or `acceptable_with_manual_review` | `Calcite=7`, `VeriEQL=2` |
| `portability` | `9` | all `manual review` or `acceptable_with_manual_review` | `PARROT=9` |
| `longtail` | `6` | `3` Stack-substrate manual-review cases, `3` SQLStorm review-prep candidates | `Stack Queries=3`, `SQLStorm=3` |

## Source-balance Summary

- `TPC-H`: `7`
- `TPC-DS`: `7`
- `JOB/IMDB`: `2`
- `Calcite`: `7`
- `VeriEQL`: `2`
- `PARROT`: `9`
- `Stack Queries`: `3`
- `SQLStorm`: `3`

Source-balance interpretation:

- The performance line stays evenly split between template families (`TPC-H` and `TPC-DS`) with a narrow `JOB/IMDB` real-schema bridge supplement.
- The consistency line remains Calcite-led with a smaller VeriEQL supplement.
- The portability line stays entirely inside the current PARROT route family.
- The longtail line is now balanced between Stack-substrate manual or hybrid anchors and direct SQLStorm query-text cases.

## Prior-experiment Participation Summary

- `seed_common_core_9`: `9`
- `expanded_pg_evidence_46`: `15`
- `direct_llm_perf_34`: `6`
- `prior_method_pg10` or `llmr2_10case`-aligned PERF packet: `9`
- `consistency_tri_engine_review_packet`: `9`
- `portability_tri_engine_review_prep_packet`: `9`
- `port_bounded_6`: `6`
- `longtail_tri_engine_review_packet`: `6`
- `longtail_sqlstorm_review_prep`: `3`

Interpretation:

- The performance line remains the most experiment-backed part of the slate.
- The consistency and portability lines are mostly review-prep and tri-engine packet backed, rather than already-finalized common-core lines.
- The SQLStorm longtail additions are supported by the focused longtail review-prep, not by a final registry-aligned common-core review.

## Caveats By Pool

### PERF

- `PERF_0062` is a replacement candidate, not a final admitted substitution.
- `PERF_0077` and `PERF_0082` are `JOB/IMDB` real-schema bridge cases and require explicit human approval.

### CONS

- All nine consistency cases remain below final admission.
- `CONS_0024` is the best replacement for `CONS_0001`, but it still carries human-review and plan-semantics caveats.

### PORT

- All nine portability cases remain stress-route review candidates rather than finalized common-core admissions.
- `PORT_0012`, `PORT_0013`, `PORT_0022`, and `PORT_0025` carry normalization caveats and require human approval.

### LONGTAIL

- `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` are manual or hybrid Stack-substrate cases, not direct SEDE query-text cases.
- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` remain `registry not_assessed` and therefore still require human review and possible registry alignment before any final freeze.

## Cases Replaced From The First-pass Slate

| first-pass case | v0.3 candidate slate case | basis |
|---|---|---|
| `PERF_0002` | `PERF_0062` | strongest TPC-DS replacement from replacement preflight |
| `CONS_0001` | `CONS_0024` | strongest Calcite replacement from replacement preflight |
| `PORT_0002` | `PORT_0008` | strongest PARROT replacement from replacement preflight |
| `LONGTAIL_0001` | `LONGTAIL_0023` | Stack-substrate replacement carried forward from replacement preflight |
| `LONGTAIL_0003` | `LONGTAIL_0011` | SQLStorm review-prep recommendation |
| `LONGTAIL_0004` | `LONGTAIL_0012` | SQLStorm review-prep recommendation |
| `LONGTAIL_0016` | `LONGTAIL_0013` | SQLStorm review-prep recommendation |

## Remaining Manual Review Questions

- Are `PERF_0077` and `PERF_0082` acceptable as `JOB/IMDB` real-schema bridges inside a Common-core v0.3 candidate slate?
- Does `CONS_0024` sufficiently replace the anchor-style `CONS_0001` for a candidate-slate phase, or should a VeriEQL case be preferred instead?
- Which PARROT stress cases with normalization caveats should be explicitly approved for a human-reviewed portability packet?
- Can `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` be treated as review-ready despite `registry not_assessed`, or should a narrow registry/status alignment happen before final freeze?

## Boundary

This candidate slate is a curation output only. It does not make final admission decisions, and it does not update registry facts in `inventory/case_registry.csv`.
