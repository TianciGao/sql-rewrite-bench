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

At the current phase, the four external draft cases no longer have the same maturity.

They now fall into two broad groups:

### Group A: promotion candidates
These are the external drafts that are now close enough to support a `common-core` promotion discussion.

- `PERF_0002`
- `PORT_0002`

### Group B: staged draft cases
These are already valuable draft cases, but should remain staged rather than be promoted prematurely.

- `LONGTAIL_0002`
- `CONS_0002`

This split is intentional.

The project should not promote all external draft cases uniformly.  
Instead, it should distinguish between:

- cases that are already strong enough for promotion review
- cases that are already useful, but are still better treated as staged draft cases

---

## 4. External Draft Case Status Table

| case_id | primary_pool | source | current maturity | current dataset-line interpretation | strongest validated evidence | main missing piece | recommended next step | promotion direction |
|---|---|---|---|---|---|---|---|---|
| `PERF_0002` | performance | TPC-DS `query53.tpl` | tri-engine source + positive/negative validated draft | provisional `common-core candidate` | source and positive rewrite are equivalent on PostgreSQL, MySQL, and Spark; negative rewrite changes results on all three engines; plans collected across all three engines | formal promotion decision still pending; release-level stabilization still needed | use as the primary candidate in the next `common-core` promotion review | strongest current promotion candidate |
| `LONGTAIL_0002` | longtail | SQLStorm StackOverflow `12033.sql` | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | MySQL/Spark not yet validated; cross-engine stability not yet established | keep as staged longtail draft; do not rush common-core promotion | remain `not_yet_admitted` |
| `CONS_0002` | consistency | Calcite `new-decorr.iq` commission candidate | PG-validated draft with positive/negative pair | remain `not_yet_admitted` for now | source and positive rewrite agree on PostgreSQL; negative rewrite changes result on PostgreSQL witness dataset | broader engine validation not yet completed; current evidence is still PG-only | keep as staged consistency draft; next step is broader validation or checker/report consolidation | remain `not_yet_admitted` |
| `PORT_0002` | portability | PARROT BIRD `pg_res.json[0]` | PG source + MySQL positive/negative validated portability draft | provisional `common-core candidate` | PostgreSQL source query returns `1.5`; MySQL positive rewrite also returns `1.5`; MySQL negative rewrite returns `1`; PG/MySQL plans collected | formal promotion decision still pending; broader engine coverage still absent | use as the second candidate in the next promotion review, after `PERF_0002` | second strongest promotion candidate |

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
- validated positive rewrite
- validated negative rewrite

**Current reading**

This is currently the strongest external draft in the repository.

**Why it is not yet fully admitted**

It still lacks:

- a formal promotion decision
- release-level stabilization
- a final judgment on whether the current draft evidence is sufficient for admission

**Immediate next step**

Do not add more technical expansion first.  
Use this case as the primary candidate in the next `common-core` promotion review.

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

`PORT_0002` is the first external portability draft case that now demonstrates the core portability story with both a positive and a negative rewrite:

- a PostgreSQL-style source expression
- a MySQL-style positive rewrite that preserves the result
- a MySQL-style negative rewrite that changes the result on the witness dataset

**Current reading**

This case is now close to a meaningful portability promotion discussion.

**Why it is not yet admitted**

It still lacks:

- a formal promotion decision
- broader engine coverage
- a final decision on whether the current two-engine portability evidence is sufficient for admission

**Immediate next step**

Use this case as the second promotion-review candidate, after `PERF_0002`.

---

## 6. Current Priority Order

At the current phase, the recommended priority order is:

### Priority 1
`PERF_0002`

Reason:
- strongest current external draft
- already validated on PostgreSQL, MySQL, and Spark
- already has validated positive and negative rewrites
- should now move into promotion review rather than further technical deepening

### Priority 2
`PORT_0002`

Reason:
- already demonstrates the core portability story
- now has both positive and negative rewrite evidence
- should enter promotion review after `PERF_0002`

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

- `PERF_0002` should be treated as the strongest external draft for near-term `common-core` promotion review
- `PORT_0002` should be treated as the second external draft to enter that same review path
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

- `PERF_0002` has become a tri-engine source + rewrite validated external performance draft and is now the strongest current promotion-review candidate
- `PORT_0002` has become a PG/MySQL portability draft with validated positive and negative rewrites and is now the second promotion-review candidate
- `LONGTAIL_0002` and `CONS_0002` are already high-value staged drafts and should remain staged rather than be promoted prematurely

The next phase is therefore not “collect more source data first,” but rather:

- selectively review the strongest external drafts for promotion
- keep weaker-but-valuable drafts staged
- promote only when the missing admission evidence is actually judged sufficient