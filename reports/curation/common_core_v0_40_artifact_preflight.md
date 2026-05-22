# Common-core v0 40-case Artifact Preflight

## Executive Summary

This is a read-only artifact and metadata preflight for the proposed Common-core v0 40-case slate on branch `curation/common-core-v0-40`.

The scan found `13` cases complete for selection review, `20` requiring manual review, and `7` currently failing strict preflight readiness.

The strongest ready cluster is the tri-engine PERF line with machine-readable run artifacts. The main preflight blockers are older anchor/admitted packages that do not yet expose `result_check`/`plan_check` artifacts in the scanned layout and several longtail drafts that remain `not_assessed` in the live registry.

This preflight does not make final admission decisions.

## Pass / Review / Fail Counts

- Pass (`complete_for_selection_review`): `13`
- Review (`needs_manual_review`): `20`
- Fail (`artifact_gap` + `defer_recommended` + `registry_conflict`): `7`

## Per-pool Summary

| pool | count | pass | review | fail | source families |
|---|---:|---:|---:|---:|---|
| `performance` | `16` | `13` | `2` | `1` | JOB/IMDB=2, TPC-DS=7, TPC-H=7 |
| `consistency` | `9` | `0` | `8` | `1` | Calcite=6, VeriEQL=2, manual_seed=1 |
| `portability` | `9` | `0` | `8` | `1` | PARROT=9 |
| `longtail` | `6` | `0` | `2` | `4` | SQLStorm=3, Stack Queries=2, manual_seed=1 |

## Source-balance Summary

### By Pool
- `consistency`: `9`
- `longtail`: `6`
- `performance`: `16`
- `portability`: `9`

### By Source Family
- `Calcite`: `6`
- `JOB/IMDB`: `2`
- `PARROT`: `9`
- `SQLStorm`: `3`
- `Stack Queries`: `2`
- `TPC-DS`: `7`
- `TPC-H`: `7`
- `VeriEQL`: `2`
- `manual_seed`: `2`

### By Prior-experiment Participation
- `seed_common_core_9`: `9`
- `expanded_pg_evidence_46`: `15`
- `direct_llm_perf_34`: `6`
- `prior_method_pg10`: `9`
- `port_bounded_6`: `6`

### By Evidence Status
- `artifact_gap`: `4`
- `complete_for_selection_review`: `13`
- `defer_recommended`: `3`
- `needs_manual_review`: `20`

## Per-case Issue Table

| case_id | pool | source_family | benchmark_line | admission_status | tri_engine | artifact notes | prior evidence | evidence_status | risks | replacement |
|---|---|---|---|---|---|---|---|---|---|---|
| `PERF_0006` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_4|calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0007` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34 | `complete_for_selection_review` | - | - |
| `PERF_0008` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_4|calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0013` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0017` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0019` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34; prior_method_pg10; calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0024` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0002` | `performance` | `TPC-DS` | `common-core ` | `admitted ` | `yes ` | manifest, source, pos, neg | - | `artifact_gap` | missing result_check; package layout caveat; missing plan_check; admission/status conflict | PERF_0062, PERF_0063, PERF_0010 |
| `PERF_0033` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_4|calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0034` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34 | `complete_for_selection_review` | - | - |
| `PERF_0035` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34 | `complete_for_selection_review` | - | - |
| `PERF_0052` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34; prior_method_pg10; calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0054` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46; prior_method_pg10; calcite_hep_4|calcite_hep_10|llmr2_10case | `complete_for_selection_review` | - | - |
| `PERF_0056` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | expanded_pg_evidence_46; direct_llm_perf_34 | `complete_for_selection_review` | - | - |
| `PERF_0077` | `performance` | `JOB/IMDB` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `PERF_0082` | `performance` | `JOB/IMDB` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0001` | `consistency` | `manual_seed` | `pilot_anchor ` | `none_needed ` | `yes ` | manifest, source, pos, neg | - | `artifact_gap` | missing result_check; missing plan_check; admission/status conflict | CONS_0024, CONS_0032, CONS_0034 |
| `CONS_0005` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0007` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46 | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0009` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0010` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0011` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0012` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | seed_common_core_9; expanded_pg_evidence_46 | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0036` | `consistency` | `VeriEQL` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `CONS_0037` | `consistency` | `VeriEQL` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `PORT_0002` | `portability` | `PARROT` | `common-core ` | `admitted ` | `yes ` | manifest, source, pos, neg | - | `artifact_gap` | missing result_check; package layout caveat; missing plan_check; admission/status conflict | PORT_0006, PORT_0008, PORT_0023 |
| `PORT_0003` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `PORT_0005` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note | - |
| `PORT_0012` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |
| `PORT_0004` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note | - |
| `PORT_0013` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |
| `PORT_0022` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |
| `PORT_0024` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note | - |
| `PORT_0025` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | port_bounded_6; port_cross_engine_closed_6_claim_packet | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |
| `LONGTAIL_0001` | `longtail` | `manual_seed` | `pilot_anchor ` | `none_needed ` | `yes ` | manifest, source, pos, neg | - | `artifact_gap` | missing result_check; missing plan_check; admission/status conflict | LONGTAIL_0023, LONGTAIL_0005, LONGTAIL_0011 |
| `LONGTAIL_0003` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `defer_recommended` | known deferred or mismatch note | LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023 |
| `LONGTAIL_0004` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `defer_recommended` | known deferred or mismatch note | LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023 |
| `LONGTAIL_0016` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `defer_recommended` | known deferred or mismatch note | LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023 |
| `LONGTAIL_0022` | `longtail` | `Stack Queries` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |
| `LONGTAIL_0024` | `longtail` | `Stack Queries` | `staged ` | `staged_not_yet_admitted ` | `yes ` | manifest, source, pos, neg, result_check, plan_check | - | `needs_manual_review` | known deferred or mismatch note; case-specific normalization caveat | - |

## Cases Safe To Keep

- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0034`
- `PERF_0035`
- `PERF_0052`
- `PERF_0054`
- `PERF_0056`

## Cases Requiring Manual Review

- `PERF_0077`
- `PERF_0082`
- `CONS_0005`
- `CONS_0007`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0036`
- `CONS_0037`
- `PORT_0003`
- `PORT_0005`
- `PORT_0012`
- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`
- `LONGTAIL_0022`
- `LONGTAIL_0024`

## Cases Recommended For Replacement

- `PERF_0002`: `artifact_gap`; suggested backups `PERF_0062, PERF_0063, PERF_0010`
- `CONS_0001`: `artifact_gap`; suggested backups `CONS_0024, CONS_0032, CONS_0034`
- `PORT_0002`: `artifact_gap`; suggested backups `PORT_0006, PORT_0008, PORT_0023`
- `LONGTAIL_0001`: `artifact_gap`; suggested backups `LONGTAIL_0023, LONGTAIL_0005, LONGTAIL_0011`
- `LONGTAIL_0003`: `defer_recommended`; suggested backups `LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023`
- `LONGTAIL_0004`: `defer_recommended`; suggested backups `LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023`
- `LONGTAIL_0016`: `defer_recommended`; suggested backups `LONGTAIL_0005, LONGTAIL_0011, LONGTAIL_0023`

## Backup Candidate Recommendations

### performance
- `PERF_0010`: `complete_for_selection_review`; source `TPC-H`; tri-engine `yes`; next gap `后续如需推进，再决定是否推进 common-core candidate`
- `PERF_0062`: `complete_for_selection_review`; source `TPC-DS`; tri-engine `yes`; next gap `后续如需推进，再决定是否推进 common-core candidate`
- `PERF_0063`: `complete_for_selection_review`; source `TPC-DS`; tri-engine `yes`; next gap `后续如需推进，再决定是否推进 common-core candidate`
- `PERF_0080`: `defer_recommended`; source `JOB/IMDB`; tri-engine `yes`; next gap `human review package quality；decide whether to keep JOB-derived case and whether to advance toward formal review`

### consistency
- `CONS_0024`: `needs_manual_review`; source `Calcite`; tri-engine `yes`; next gap `human review package quality；decide whether to keep Calcite-derived consistency case and whether to advance toward formal review`
- `CONS_0032`: `needs_manual_review`; source `VeriEQL`; tri-engine `yes`; next gap `human review package quality；decide whether to keep VeriEQL-derived consistency case and whether to advance toward formal review`
- `CONS_0034`: `needs_manual_review`; source `VeriEQL`; tri-engine `yes`; next gap `human review package quality；decide whether to keep VeriEQL-derived consistency case and whether to advance toward formal review`

### portability
- `PORT_0006`: `needs_manual_review`; source `PARROT`; tri-engine `yes`; next gap `human review；portability review-prep packet；later admission decision；plan semantics not formally reviewed`
- `PORT_0008`: `needs_manual_review`; source `PARROT`; tri-engine `yes`; next gap `human review；portability review-prep packet / later formal review；later admission decision；plan semantics not formally reviewed`
- `PORT_0023`: `needs_manual_review`; source `PARROT`; tri-engine `yes`; next gap `human review；portability review-prep packet / later formal review；later admission decision；plan semantics not formally reviewed`

### longtail
- `LONGTAIL_0023`: `needs_manual_review`; source `Stack Queries`; tri-engine `yes`; next gap `human review package quality；prepare longtail review-prep wording；plan semantics not formally reviewed；later admission decision`
- `LONGTAIL_0005`: `defer_recommended`; source `SQLStorm`; tri-engine `yes`; next gap `human review package quality；decide whether to keep SQLStorm-derived longtail case and whether to advance toward formal review`
- `LONGTAIL_0011`: `defer_recommended`; source `SQLStorm`; tri-engine `yes`; next gap `human review package quality；decide whether to keep SQLStorm-derived longtail case and whether to advance toward formal review`

## Non-decision Statement

This preflight is limited to registry facts, package presence, artifact presence, and prior-evidence metadata. It does not run databases, does not modify cases or registries, and does not make final admission or replacement decisions.
