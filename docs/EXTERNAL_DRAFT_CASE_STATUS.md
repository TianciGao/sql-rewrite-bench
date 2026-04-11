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

At the current stage, these cases are still treated as **draft external cases**, not final release-level benchmark cases.

---

## 3. Current Consolidation Principle

At the current phase, all four external draft cases remain in:

- `dataset_line_candidate: not_yet_admitted`
  or
- provisional `common-core`-leaning status only

This is intentional.

The project should not promote external draft cases into the formal admitted set merely because one technical step has succeeded.

Promotion should occur only after the next missing evidence is added in a controlled way.

---

## 4. External Draft Case Status Table

| case_id | primary_pool | source | current maturity | current dataset-line interpretation | strongest validated evidence | main missing piece | recommended next step | promotion direction |
|---|---|---|---|---|---|---|---|---|
| `PERF_0002` | performance | TPC-DS `query53.tpl` | tri-engine source-validated draft | strongest current `common-core` promotion candidate among the external drafts | source SQL runs on PostgreSQL, MySQL, and Spark with value-normalized agreement; source plans collected | no positive/negative rewrites yet | define conservative positive and hard negative rewrites | move toward `common-core candidate` |
| `LONGTAIL_0002` | longtail | SQLStorm StackOverflow `12033.sql` | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | MySQL/Spark not yet validated; cross-engine stability not yet established | keep as staged longtail draft; do not rush common-core promotion | remain `not_yet_admitted` |
| `CONS_0002` | consistency | Calcite `new-decorr.iq` commission candidate | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | broader engine validation not yet completed; current evidence is still PG-only | keep as staged consistency draft; next step is broader validation or checker/report consolidation | remain `not_yet_admitted` |
| `PORT_0002` | portability | PARROT BIRD `pg_res.json[0]` | PG/MySQL-validated portability draft | close to `common-core`, but not yet admitted | PostgreSQL source query and MySQL positive rewrite both return `1.5` on the witness dataset; PG/MySQL plans collected | no negative rewrite yet; Spark not yet validated | define one portability-oriented negative rewrite | move toward `common-core candidate` |

---

## 5. Per-Case Interpretation

### 5.1 `PERF_0002`

**Why it matters**

`PERF_0002` is the first external performance-oriented draft case that has been pushed beyond source inspection into:

- materialized source SQL
- minimal generated dataset
- PostgreSQL execution
- MySQL execution
- Spark execution
- source-level plan collection

**Current reading**

This case is now the strongest current candidate for eventual `common-core` promotion among the external drafts.

**Why it is not yet admitted**

It still lacks:

- positive rewrite
- negative rewrite

**Immediate next step**

Define conservative positive and hard negative rewrites before deciding whether to promote the case further.

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

rather than in immediate common-core cross-engine admission.

**Immediate next step**

Keep it staged. Do not force common-core promotion yet.

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

`PORT_0002` is the first external portability draft case that already demonstrates the core portability story:

- a PostgreSQL-style source expression
- a MySQL-style positive rewrite
- matching results on a controlled witness dataset

**Current reading**

This case is already close to a compelling portability benchmark unit.

**Why it is not yet admitted**

It still lacks:

- a portability-oriented negative rewrite
- broader engine coverage
- a more complete cross-engine closure story

**Immediate next step**

Define a negative portability rewrite before considering further promotion.

---

## 6. Current Priority Order

At the current phase, the recommended priority order is:

### Priority 1
`PERF_0002`

Reason:
- already validated on PostgreSQL, MySQL, and Spark
- strongest current external draft for `common-core` promotion
- now needs rewrite variants rather than more source-only validation

### Priority 2
`PORT_0002`

Reason:
- already demonstrates the core portability story
- needs a negative rewrite to become a stronger portability case

### Priority 3
`CONS_0002`

Reason:
- already has a strong source/positive/negative witness setup
- should remain staged until broader validation is added

### Priority 4
`LONGTAIL_0002`

Reason:
- already valuable as a longtail structural draft
- should remain staged rather than be pushed prematurely toward common-core

---

## 7. Current Decision

The project should **not** immediately promote all four external draft cases into the formal admitted set.

Instead, the current decision is:

- `PERF_0002` should be treated as the strongest external draft for near-term `common-core` promotion
- `PORT_0002` should be treated as the second external draft closest to `common-core`
- `LONGTAIL_0002` and `CONS_0002` should continue to be treated as **high-value staged draft cases**
- all four should remain tracked explicitly as **external draft cases**, not silently merged into the admitted benchmark population

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

- `PERF_0002` has become a tri-engine source-validated external performance draft and is the strongest current `common-core` promotion candidate
- `PORT_0002` is the next closest case to a `common-core` promotion path
- `LONGTAIL_0002` and `CONS_0002` are already high-value staged drafts and should remain staged rather than be promoted prematurely

The next phase is therefore not “collect more source data first,” but rather:

- selectively deepen the strongest external drafts
- keep weaker-but-valuable drafts staged
- promote only when the missing validation evidence is actually present