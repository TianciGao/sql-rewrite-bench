# Common-core v0 Replacement Preflight

## Executive Summary

This is a second read-only replacement preflight for Common-core v0. It checks only registry state, case-package presence, machine-readable artifact presence, and existing review/defer caveats.

Suitability counts: `strong_replacement=3`, `acceptable_with_manual_review=7`, `extended_preferred=10`, `defer=0`.

The PERF replacements are the cleanest because they are staged tri-engine cases with full machine-readable run artifacts and no current registry defer beyond later candidate review. CONS and PORT replacements are structurally ready but still explicitly sit in manual-review territory. Most LONGTAIL backups are artifact-complete and tri-engine closed, but the live registry still keeps them `not_assessed`, which makes them stronger as extended-preferred replacements than as common-core-ready swaps.

## Candidate Table

| case_id | pool | source_family | benchmark_line | admission_status | tri_engine | result_check | plan_check | caveat | suitability |
|---|---|---|---|---|---|---|---|---|---|
| `PERF_0062` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | TPC-DS tri-engine review marks formal skeleton complete; release-grade incomplete | `strong_replacement` |
| `PERF_0063` | `performance` | `TPC-DS` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | TPC-DS tri-engine review marks formal skeleton complete; release-grade incomplete | `strong_replacement` |
| `PERF_0010` | `performance` | `TPC-H` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | tri-engine review notes say Spark validation bundle remains partial at case-local layout hardening level | `strong_replacement` |
| `CONS_0024` | `consistency` | `Calcite` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | Calcite consistency review notes repaired after initial PG witness-discrimination issue; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `CONS_0032` | `consistency` | `VeriEQL` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | VeriEQL review notes compact correlated NOT IN null-sensitive case; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `CONS_0034` | `consistency` | `VeriEQL` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | VeriEQL review notes repaired after narrow Spark alias compatibility issue; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `PORT_0006` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | plan semantics not formally reviewed | portability review-prep only; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `PORT_0008` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | plan semantics not formally reviewed | portability review-prep only; appears in later PG-route/closure scratch snapshots | `acceptable_with_manual_review` |
| `PORT_0023` | `portability` | `PARROT` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | plan semantics not formally reviewed | portability review-prep only; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `LONGTAIL_0023` | `longtail` | `Stack Queries` | `staged ` | `staged_not_yet_admitted ` | `yes ` | yes | yes | known review/defer note | plan semantics not formally reviewed | normalization caveat: manual/hybrid Stack substrate | manual/hybrid Stack-substrate anchor; not direct SEDE source-text; plan semantics not formally reviewed | `acceptable_with_manual_review` |
| `LONGTAIL_0005` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0011` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0012` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete; repaired after MySQL-open state; registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0013` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete; repaired after MySQL-open state; registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0014` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0015` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0018` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete; repaired after MySQL-open state; registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0019` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0020` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete but registry still not_assessed | `extended_preferred` |
| `LONGTAIL_0021` | `longtail` | `SQLStorm` | `not_assessed ` | `not_assessed ` | `yes ` | yes | yes | registry not_assessed | known review/defer note | SQLStorm tri-engine review marks formal skeleton complete; repaired after earlier artifact-identity mismatch and MySQL-open state; registry still not_assessed | `extended_preferred` |

## Final Replacement Recommendations

- Final replacement for `PERF_0002`: `PERF_0062`. This is the strongest same-source-family TPC-DS replacement in the candidate set, with staged tri-engine closure and full machine-readable result/plan artifacts.
- Final replacement for `CONS_0001`: `CONS_0024`. This is the cleanest Calcite-based consistency replacement with staged tri-engine closure and explicit case-root governance artifacts, but it still needs manual review.
- Final replacement for `PORT_0002`: `PORT_0008`. This keeps the replacement in the same PARROT line, has tri-engine closure plus case-root result/plan artifacts, and has slightly better scratch-line visibility than the other two candidates. It still remains a manual-review portability draft rather than an admitted replacement.
- Fewer than four LONGTAIL replacements are ready at common-core replacement level. Only `LONGTAIL_0023` reaches `acceptable_with_manual_review` in this stricter pass.
- The remaining LONGTAIL candidates are better treated as `extended_preferred` because the live registry still marks them `not_assessed` even though tri-engine artifacts are present.

## Ordered Pool Recommendations

### PERF
- `PERF_0010`: `strong_replacement`; source `TPC-H`; rationale: staged tri-engine case with full machine-readable artifacts and no current registry defer beyond later candidate review
- `PERF_0062`: `strong_replacement`; source `TPC-DS`; rationale: staged tri-engine case with full machine-readable artifacts and no current registry defer beyond later candidate review
- `PERF_0063`: `strong_replacement`; source `TPC-DS`; rationale: staged tri-engine case with full machine-readable artifacts and no current registry defer beyond later candidate review

### CONS
- `CONS_0024`: `acceptable_with_manual_review`; source `Calcite`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory
- `CONS_0032`: `acceptable_with_manual_review`; source `VeriEQL`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory
- `CONS_0034`: `acceptable_with_manual_review`; source `VeriEQL`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory

### PORT
- `PORT_0006`: `acceptable_with_manual_review`; source `PARROT`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory
- `PORT_0008`: `acceptable_with_manual_review`; source `PARROT`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory
- `PORT_0023`: `acceptable_with_manual_review`; source `PARROT`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory

### LONGTAIL
- `LONGTAIL_0023`: `acceptable_with_manual_review`; source `Stack Queries`; rationale: tri-engine and artifact-complete, but registry/review notes still explicitly keep it in manual review / not formally reviewed territory
- `LONGTAIL_0005`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0011`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0012`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0013`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0014`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0015`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0018`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0019`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0020`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line
- `LONGTAIL_0021`: `extended_preferred`; source `SQLStorm`; rationale: artifact-complete and tri-engine closed, but live registry still leaves it not_assessed rather than a staged common-core review line

## Non-decision Statement

This preflight does not run databases, does not call any LLM/API, does not modify registry or SQL, and does not make final admission decisions.
