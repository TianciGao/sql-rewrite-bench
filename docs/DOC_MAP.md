# Document Map

## 1. Role of this file

This file explains what each major project document is for, which files should be treated as the main maintained documents, which files are review records, and which files are candidates for archive.

Its purpose is to reduce document sprawl and make it clear:

- which file should be read first
- which file should be updated regularly
- which file is only a historical review record
- which file is likely outdated and should be archived rather than expanded further

---

## 2. Reading Order

Recommended reading order for normal project work:

1. `docs/PROJECT_PLAN.md`
2. `docs/POOL_MAPPING_RULES.md`
3. `benchmark_spec/common_core_extended_rules_v0.md`
4. `benchmark_spec/primary_metrics_v0.md`
5. `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
6. `docs/ANCHOR_CASE_SUMMARY.md`
7. `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
8. `benchmark_spec/decision_log.md`

Use the review documents only when a specific promotion / admission question needs to be checked.

---

## 3. Main Maintained Documents

These are the documents that should be actively maintained and kept aligned with the current project state.

| file | role | maintenance status |
|---|---|---|
| `docs/PROJECT_PLAN.md` | overall roadmap, scope, and current phase | main maintained |
| `docs/POOL_MAPPING_RULES.md` | formal pool assignment rules | main maintained |
| `docs/ANCHOR_CASE_SUMMARY.md` | anchor-case summary and pilot anchor interpretation | main maintained |
| `docs/EXTERNAL_DRAFT_CASE_STATUS.md` | cross-case status summary for external draft / candidate / admitted cases | main maintained |
| `benchmark_spec/decision_log.md` | project-level frozen decisions and decision trail | main maintained |
| `benchmark_spec/common_core_extended_rules_v0.md` | rules for `common-core` vs `extended` dataset line | main maintained |
| `benchmark_spec/primary_metrics_v0.md` | frozen primary metrics for current version | main maintained |
| `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md` | archetype-complete definition for future scalable case construction | main maintained |

---

## 4. Review Records

These files should usually be kept, but they are not everyday “mainline” files.
They exist mainly as explicit review records.

| file | role | maintenance status |
|---|---|---|
| `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md` | first promotion review for Batch 1 external draft cases | review record |
| `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md` | first explicit common-core admission check | review record |
| `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v0.md` | case-specific admission review for `PORT_0002` | review record |

Rule:
- keep these files
- do not keep expanding them unless a new review version is actually needed
- prefer creating `v1`, `v2`, etc. only when the decision context materially changes

---

## 5. Reference / Template Documents

These files are useful reference material, but they are not the primary place to understand current project state.

| file | role | maintenance status |
|---|---|---|
| `docs/INVENTORY_TEMPLATE.md` | filling rules for `inventory/source_registry.csv` | reference |
| `benchmark_spec/case_schema_v0.1.yaml` | older schema sketch / reference | likely outdated reference |

---

## 6. Operational Data Files (Not Narrative Docs)

These are important project files, but they are not “documentation” in the same sense as the markdown documents above.

| file | role |
|---|---|
| `inventory/source_registry.csv` | source-level registry |
| `inventory/source_inspection_phase3a_batch1.csv` | source inspection results |
| `inventory/seed_candidates_phase3a_batch1.csv` | seed-level tracking table |

These files should be read together with the main maintained docs, not instead of them.

---

## 7. Archive Candidates

These files should not be deleted casually, but they are good candidates for archive when the repository is cleaned up.

| file | reason |
|---|---|
| `benchmark_spec/benchmark_spec_v0.md` | historical boundary snapshot; no longer reflects the current repository stage |
| `benchmark_spec/case_schema_v0.1.yaml` | too small / too old compared with current real case manifests |

Archive policy:
- move to `docs/archive/` or another explicit archive location
- do not silently delete historical documents
- keep filenames stable enough that old references can still be understood

---

## 8. Simple Maintenance Rule

When deciding where new information should go, use the following rule:

### Add to an existing main maintained document when:
- the information changes the ongoing understanding of the project
- the information affects future routine work
- the information changes current project state

### Add a new review record only when:
- a promotion / admission / policy review is being made
- the project needs an explicit, frozen decision artifact
- the content is a one-time review rather than a daily-maintained summary

### Archive rather than expand when:
- the file describes an older project stage
- the file no longer matches the repository’s actual state
- the file has become historical rather than operational

---

## 9. Current Practical Interpretation

At the present stage:

- `PROJECT_PLAN.md` should remain the main roadmap file
- `EXTERNAL_DRAFT_CASE_STATUS.md` should remain the main external-case status file
- `decision_log.md` should remain the main decision history file
- review files should be kept as review records, not treated as everyday status files
- outdated early-stage files should gradually move to archive rather than continue accumulating partial edits

---

## 10. Bottom Line

This repository now has enough documents that document roles must be explicit.

The project should therefore operate with a small set of main maintained documents,
a smaller set of frozen review records,
and a clearly marked archive layer.

That is the only scalable way to keep the documentation usable as the benchmark grows.
