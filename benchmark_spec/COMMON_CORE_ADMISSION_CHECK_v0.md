# Common-Core Admission Check v0

## 1. Document Role

This document defines the first explicit admission check for promoting an external draft case
from provisional candidate status into an admitted `common-core` case.

Its role is narrower than:

- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`

Those documents summarize maturity and promotion direction.

This document answers a stricter question:

> Is the case now strong enough to be treated as an admitted external common-core case?

---

## 2. Scope

This first admission check reviews the current four Batch 1 external draft cases:

- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

However, this review is expected to produce at most a very small number of admissions.

---

## 3. Admission Principle

Admission into `common-core` should remain conservative.

A case should not be admitted merely because:

- it is interesting
- one engine succeeded
- a draft case package exists

Instead, admission should require that the case already behaves like a stable benchmark unit.

---

## 4. Minimum Admission Criteria

A case should satisfy all of the following to pass this check.

### 4.1 Provenance completeness
The derivation path from external source to repository case package must be explicit.

### 4.2 Case-package completeness
The case must include at least:

- frozen `source.sql`
- positive and negative rewrite files
- manifest
- taxonomy trial
- provenance files
- data profile

### 4.3 Multi-engine execution evidence
The case should demonstrate stable execution on the intended `common-core` engine set.

For this first admission check, the strongest possible case is tri-engine evidence.

### 4.4 Rewrite behavior evidence
The case must show:

- source == positive
- source != negative

with concrete execution evidence, not only by argument.

### 4.5 Plan observability
Plan artifacts must be present for the validated engines.

### 4.6 Pool-level representativeness
The case must already capture the core benchmark value of its pool in a reusable way.

---

## 5. Current Admission Check Table

| case_id | current maturity | admission check result | rationale |
|---|---|---|---|
| `PERF_0002` | tri-engine source + positive/negative validated draft | **PASS** | provenance complete; source/positive/negative all exist; PostgreSQL/MySQL/Spark all validate source/positive/negative behavior; plans collected across all three engines; case is already benchmark-shaped |
| `LONGTAIL_0002` | PG-validated draft with positive/negative pair | **NOT YET** | high-value draft, but current evidence is still PG-only and not yet strong enough for common-core admission |
| `CONS_0002` | PG-validated draft with positive/negative pair | **NOT YET** | semantic evidence is strong, but current evidence is still PG-only and should remain staged |
| `PORT_0002` | PG source + MySQL positive/negative validated portability draft | **NOT YET** | strong portability draft, but still lacks broader closure and should remain a candidate rather than a fully admitted common-core case |

---

## 6. Current Admission Decision

The current decision of this first admission check is:

### Admit as external common-core case
- `PERF_0002`

### Do not admit yet
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

---

## 7. Why `PERF_0002` Passes

`PERF_0002` now satisfies the current minimum admission criteria because it has:

- explicit provenance from TPC-DS `query53.tpl`
- frozen source SQL
- positive rewrite
- negative rewrite
- minimal reusable dataset
- PostgreSQL validation
- MySQL validation
- Spark validation
- source/positive equivalence
- source/negative divergence
- plan artifacts across validated engines

This makes it the first external case in the repository that is strong enough to behave as an admitted benchmark unit rather than merely as a staged draft.

---

## 8. Why the Other Three Do Not Yet Pass

### `LONGTAIL_0002`
It is already valuable, but its evidence is still too concentrated on PostgreSQL witness validation.

### `CONS_0002`
Its semantic structure is excellent, but it remains a staged consistency draft rather than an admitted common-core case.

### `PORT_0002`
It is already a strong portability candidate, but it is still better treated as a `common-core candidate` rather than an admitted common-core case.

---

## 9. Implementation Consequence

This admission check implies the following metadata consequence:

- `PERF_0002` should move from `common-core_candidate` to `common-core`
- `PORT_0002` should remain `common-core_candidate`
- `LONGTAIL_0002` should remain `not_yet_admitted`
- `CONS_0002` should remain `not_yet_admitted`

This file itself is the explicit project-level basis for that change.

---

## 10. Update Rule

This file should be updated whenever:

- another external draft case reaches admission-level evidence
- an admitted common-core case is deferred or downgraded
- the project changes its admission threshold
- a later admission review supersedes this version

Related updates should also be reflected in:

- case-local `manifest.yaml`
- case-local `taxonomy_trial_v0.2.yaml`
- `benchmark_spec/decision_log.md`
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`

---

## 11. Current Bottom Line

At the current stage, the project is ready to take its first explicit admission step.

That step is:

> Admit `PERF_0002` as the first external common-core case.

The other external draft cases remain important, but they should continue to be treated as candidates or staged drafts rather than admitted common-core cases.
