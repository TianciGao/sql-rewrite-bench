# External Draft Case Status

## 1. Document Role

This document records the current status of the **external draft cases** that were derived from Batch 1 external sources during Phase 3A.

Its purpose is to provide a compact and stable summary of:

- which external source each draft case came from
- what level of validation has already been completed
- which draft cases are currently closer to `common-core`
- which draft cases should remain `not_yet_admitted`
- what the most valuable next step is for each case

This document is not a replacement for per-case manifests or taxonomy files.  
Instead, it acts as a **cross-case consolidation layer** for the current external draft set.

Related files:

- `docs/PROJECT_PLAN.md`
- `docs/ANCHOR_CASE_SUMMARY.md`
- `docs/POOL_MAPPING_RULES.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`
- `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`
- `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v0.md`
- `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v1.md`
- `inventory/seed_candidates_phase3a_batch1.csv`

---

## 2. Scope

This file covers the current external draft cases derived from the first-wave inspected sources:

- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

These cases are important because they are the first cases in the repository that demonstrate:

> **external source → seed candidate → draft case package**

rather than only anchor-style hand-constructed cases.

At the current stage, these cases are no longer all at the same maturity level.

---

## 3. Current Consolidation Principle

At the current phase, the four external draft cases fall into two groups:

### Group A: admitted external common-core cases
- `PERF_0002`
- `PORT_0002`

### Group B: staged draft cases
- `LONGTAIL_0002`
- `CONS_0002`

This split is intentional.

The project should not treat all external draft cases as equally mature.

Instead, it should distinguish between:

- cases already strong enough to be admitted
- cases already useful, but still better treated as staged drafts

---

## 4. External Draft Case Status Table

| case_id | primary_pool | source | current maturity | current dataset-line interpretation | strongest validated evidence | main missing piece | recommended next step | promotion direction |
|---|---|---|---|---|---|---|---|---|
| `PERF_0002` | performance | TPC-DS `query53.tpl` | tri-engine source + positive/negative validated draft | **admitted external common-core** | source and positive rewrite are equivalent on PostgreSQL, MySQL, and Spark; negative rewrite changes the result on all three engines; plan artifacts are collected across all three engines | no immediate technical gap for admission; remaining work is release-level stabilization only | treat as the admitted reference external common-core case | already admitted |
| `LONGTAIL_0002` | longtail | SQLStorm StackOverflow `12033.sql` | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | MySQL/Spark not yet validated; cross-engine stability not yet established | keep as staged longtail draft; do not rush common-core promotion | remain `not_yet_admitted` |
| `CONS_0002` | consistency | Calcite `new-decorr.iq` commission candidate | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | broader engine validation not yet completed; current evidence is still PG-only | keep as staged consistency draft; next step is broader validation or checker/report consolidation | remain `not_yet_admitted` |
| `PORT_0002` | portability | PARROT BIRD `pg_res.json[0]` | PG source + MySQL positive/negative + Spark positive/negative validated portability draft | **admitted external common-core** | PostgreSQL source returns `1.5`; MySQL positive returns `1.5`; MySQL negative returns `1`; Spark positive returns `1.5`; Spark negative returns `1.0`; plan artifacts are collected for the validated source/rewrite sides | no immediate technical gap for admission; remaining work is release-level stabilization only | treat as the admitted external portability reference case | already admitted |

---

## 5. Per-Case Interpretation

### 5.1 `PERF_0002`

**Why it matters**

`PERF_0002` is the first external performance-oriented case that has been pushed beyond source inspection into:

- materialized source SQL
- minimal generated dataset
- PostgreSQL execution
- MySQL execution
- Spark execution
- source-level plan collection
- validated positive rewrite
- validated negative rewrite

**Current reading**

This case is now the strongest external performance case in the repository and has already passed the current admission threshold.

**Current status**

`PERF_0002` is now treated as:

> **the first admitted external common-core case**

**Immediate next step**

Do not deepen it technically before needed.  
Use it as the admitted external reference case in later benchmark discussions.

---

### 5.2 `LONGTAIL_0002`

**Why it matters**

`LONGTAIL_0002` is the first external longtail draft case derived from SQLStorm and demonstrates that the repository can absorb:

- realistic query style
- CTE structure
- outer-join-bearing structure
- positive/negative rewrite behavior on a witness dataset

**Current reading**

This case is already valuable as a longtail structural draft, even without broader engine closure.

**Why it should remain `not_yet_admitted`**

Its current value lies in:

- structure coverage
- rewrite sensitivity
- longtail realism

rather than in immediate cross-engine common-core admission.

**Immediate next step**

Keep it staged. Do not force promotion yet.

---

### 5.3 `CONS_0002`

**Why it matters**

`CONS_0002` is the first external consistency draft case that clearly demonstrates:

- a semantic source query
- a semantically equivalent positive rewrite
- a semantically incorrect negative rewrite
- a small witness dataset that exposes the difference

**Current reading**

This is currently the most complete **consistency-shaped** external draft case.

**Why it should remain `not_yet_admitted`**

Although its internal logic is strong, current validation is still PostgreSQL-only.

**Immediate next step**

Keep it staged. Its next value comes from broader validation or improved checker/report integration, not from premature admission.

---

### 5.4 `PORT_0002`

**Why it matters**

`PORT_0002` is the first external portability draft case that now demonstrates the portability story with:

- a PostgreSQL-style source expression
- a MySQL-style positive rewrite preserving the result
- a MySQL-style negative rewrite changing the result
- a Spark-style positive rewrite preserving the result
- a Spark-style negative rewrite changing the result

**Current reading**

This case is now strong enough to be treated as an admitted external common-core portability case.

**Current status**

`PORT_0002` is now treated as:

> **the second admitted external common-core case**

**Immediate next step**

Do not deepen it technically before needed.  
Use it as the admitted external portability reference case in later benchmark discussions.

---

## 6. Current Priority Order

At the current phase, the recommended priority order is:

### Priority 1
`CONS_0002`

Reason:
- already has a strong source/positive/negative witness setup
- is now the strongest remaining staged draft that may later deserve broader validation or checker/report consolidation

### Priority 2
`LONGTAIL_0002`

Reason:
- already valuable as a longtail structural draft
- should remain staged, but is the next staged archetype to revisit if the project wants to deepen non-admitted archetypes

### Priority 3
`PERF_0002`

Reason:
- already admitted
- no immediate technical deepening is required

### Priority 4
`PORT_0002`

Reason:
- already admitted
- no immediate technical deepening is required

---

## 7. Current Decision

The current project-level decision is:

### Admitted external common-core cases
- `PERF_0002`
- `PORT_0002`

### Staged draft cases
- `LONGTAIL_0002`
- `CONS_0002`

This means the project now explicitly distinguishes between:

- admitted external common-core cases
- staged draft cases

---

## 8. Why This Document Exists

Without a cross-case consolidation layer, the project risks drifting into one of two errors:

### Error A
Treating every external draft case as equally mature.

### Error B
Promoting cases prematurely based on one successful run.

This document prevents both errors by forcing the project to distinguish:

- source-level success
- draft case success
- pool-level usefulness
- admission readiness

---

## 9. Update Rule

This file should be updated whenever any of the following happens:

- an external draft case gains a new validated engine
- an external draft case gains positive and/or negative rewrites
- an external draft case changes its current dataset-line interpretation
- an external draft case is promoted closer to `common-core`
- an external draft case is formally admitted or explicitly deferred

Related updates should also be reflected in:

- the case-local `manifest.yaml`
- the case-local `taxonomy_trial_v0.2.yaml`
- `inventory/seed_candidates_phase3a_batch1.csv`
- `docs/ANCHOR_CASE_SUMMARY.md` when applicable
- `benchmark_spec/decision_log.md` when a project-level promotion decision is made

---

## 10. Current Bottom Line

At the present stage, the project has successfully demonstrated that all four formal pools can accept **external-source-derived draft cases**.

That is already a meaningful construction milestone.

However, the four external draft cases are no longer equally mature:

- `PERF_0002` has become the first admitted external common-core case
- `PORT_0002` has become the second admitted external common-core case
- `LONGTAIL_0002` and `CONS_0002` are already high-value staged drafts and should remain staged rather than be promoted prematurely

The next phase is therefore not “collect more source data first,” but rather:

- use the admitted cases as reference points
- keep staged drafts stable
- revisit staged cases only when broader validation or stronger methodological need justifies it