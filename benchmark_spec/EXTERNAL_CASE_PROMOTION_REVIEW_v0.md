# External Case Promotion Review v0

## 1. Document Role

This document records the first formal **promotion review** for the current Batch 1 external draft cases.

Its purpose is to answer a narrower question than `docs/EXTERNAL_DRAFT_CASE_STATUS.md`:

> Given the current evidence, should an external draft case remain `not_yet_admitted`, be promoted to `common-core candidate`, or be considered for later formal admission?

This document does **not** replace:

- per-case `manifest.yaml`
- per-case `taxonomy_trial_v0.2.yaml`
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`

Instead, it provides a project-level review layer for promotion decisions.

---

## 2. Scope

This review covers the current four external draft cases derived from Batch 1 external sources:

- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

These four cases are reviewed because they are the first repository cases that successfully demonstrate:

> **external source → seed candidate → draft case package**

with real case-local evidence.

---

## 3. Review Principle

This review uses a conservative promotion principle.

An external draft case should **not** be promoted merely because it is interesting or because one run succeeded.

Instead, promotion depends on whether the case now has enough evidence to support a stronger project-level status.

For this review, the relevant statuses are:

- `not_yet_admitted`
- `common-core candidate`
- later, possibly formal admission

This review intentionally does **not** directly admit any external case into the final admitted set.

---

## 4. Review Criteria

The following criteria are used in this review:

### 4.1 Provenance completeness
The source, seed, and derivation path should be clearly recorded.

### 4.2 Case-package completeness
The case should have at least:

- frozen `source.sql`
- usable manifest
- usable taxonomy trial
- relevant provenance files

### 4.3 Execution evidence
The case should have concrete execution evidence on one or more benchmark engines.

### 4.4 Plan evidence
The case should have plan artifacts for the validated engine(s).

### 4.5 Pool-specific usefulness
The case should already demonstrate the core value of its target pool:

- performance: stable analytical cross-engine source behavior
- longtail: structural coverage and rewrite sensitivity
- consistency: positive/negative semantic distinction
- portability: cross-dialect source/target behavior

### 4.6 Promotion readiness
Promotion is justified only if the case has enough evidence to support a stronger status than ordinary staging.

---

## 5. Promotion Review Table

| case_id | primary_pool | current maturity | current strongest evidence | review judgment | why not fully admitted yet | next action |
|---|---|---|---|---|---|---|
| `PERF_0002` | performance | tri-engine source + positive/negative validated draft | PostgreSQL, MySQL, and Spark all agree on source/positive equivalence and source/negative non-equivalence | **promote to `common-core candidate`** | formal admission decision still pending; release-level stabilization still needed | use as the primary candidate in the next common-core promotion discussion |
| `LONGTAIL_0002` | longtail | PG-validated draft with positive/negative pair | PostgreSQL witness dataset clearly distinguishes positive vs negative behavior | **keep `not_yet_admitted`** | longtail value is already high, but cross-engine closure is still weak | keep staged; do not rush promotion |
| `CONS_0002` | consistency | PG-validated draft with positive/negative pair | PostgreSQL witness dataset clearly proves source/positive equivalence and source/negative divergence | **keep `not_yet_admitted`** | semantic evidence is strong, but current validation is still PG-only | keep staged; revisit after broader validation or checker/report strengthening |
| `PORT_0002` | portability | PG source + MySQL positive/negative validated portability draft | PG source returns `1.5`, MySQL positive returns `1.5`, MySQL negative returns `1` | **promote to `common-core candidate`** | Spark is still missing; full cross-engine closure is incomplete | use as the second candidate in the next common-core promotion discussion |

---

## 6. Per-Case Review Notes

### 6.1 `PERF_0002`

**Current state**

`PERF_0002` has become the strongest external draft case in the repository.

It now includes:

- materialized source provenance
- minimal generated data subset
- PostgreSQL execution
- MySQL execution
- Spark execution
- source plan artifacts
- validated positive rewrite
- validated negative rewrite

**Promotion judgment**

This case is strong enough to move beyond ordinary staging.

**Decision**

Promote from ordinary external draft handling into:

> `common-core candidate`

but do **not** yet mark it as formally admitted.

---

### 6.2 `LONGTAIL_0002`

**Current state**

`LONGTAIL_0002` already demonstrates the key value of a longtail case:

- realistic query style
- CTE structure
- outer-join sensitivity
- positive/negative distinction on a witness dataset

**Promotion judgment**

Its structural value is already clear, but that does not yet justify promotion toward common-core.

**Decision**

Keep as:

> `not_yet_admitted`

and continue to treat it as a staged longtail draft.

---

### 6.3 `CONS_0002`

**Current state**

`CONS_0002` is already a strong consistency-shaped draft case because it clearly demonstrates:

- semantic source query
- equivalent positive rewrite
- non-equivalent negative rewrite
- small witness dataset with explicit result distinction

**Promotion judgment**

Its semantic evidence is excellent, but broad engine evidence is still limited.

**Decision**

Keep as:

> `not_yet_admitted`

and treat it as a high-value staged consistency draft.

---

### 6.4 `PORT_0002`

**Current state**

`PORT_0002` now demonstrates the core portability story more convincingly than before:

- PostgreSQL-style source expression
- MySQL-style positive rewrite preserving the result
- MySQL-style negative rewrite changing the result
- compact witness dataset with explicit numeric difference

**Promotion judgment**

This is now strong enough to move beyond ordinary staging.

**Decision**

Promote from ordinary external draft handling into:

> `common-core candidate`

but do **not** yet mark it as formally admitted.

---

## 7. Current Promotion Decision

The current project-level promotion decision is:

### Promote to `common-core candidate`
- `PERF_0002`
- `PORT_0002`

### Keep as `not_yet_admitted`
- `LONGTAIL_0002`
- `CONS_0002`

This means the project now distinguishes between:

- external draft cases that are strong enough to enter promotion review
- external draft cases that are already useful, but should remain staged

---

## 8. Implementation Consequence

This review implies the following expected metadata consequences:

### `PERF_0002`
Expected direction:
- move toward `dataset_line_candidate: common-core candidate` semantics
- keep final admission pending separate decision

### `PORT_0002`
Expected direction:
- move toward `dataset_line_candidate: common-core candidate` semantics
- keep final admission pending separate decision

### `LONGTAIL_0002`
No promotion yet:
- keep `not_yet_admitted`

### `CONS_0002`
No promotion yet:
- keep `not_yet_admitted`

This document itself does not force the metadata change automatically, but it should guide the next synchronized update of manifests and decision logs.

---

## 9. Why This Review Exists

Without a promotion review layer, the project risks two mistakes:

### Mistake A
Treating all external draft cases as equally mature.

### Mistake B
Promoting a technically successful case too early, without a documented project-level decision.

This document reduces both risks by explicitly separating:

- draft case success
- pool-specific usefulness
- promotion readiness
- final admission readiness

---

## 10. Update Rule

This file should be updated whenever:

- an external draft case gains a new engine validation
- an external draft case gains positive and/or negative rewrites
- an external draft case is promoted toward `common-core candidate`
- an external draft case is formally admitted
- an external draft case is explicitly deferred from promotion

Related updates should also be reflected in:

- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- case-local `manifest.yaml`
- case-local `taxonomy_trial_v0.2.yaml`
- `benchmark_spec/decision_log.md`
- `inventory/seed_candidates_phase3a_batch1.csv` when applicable

---

## 11. Current Bottom Line

At the current stage, the project has already shown that all four formal pools can absorb external-source-derived draft cases.

That is a construction milestone.

The next step is no longer “collect more source data first.”

The next step is:

- promote the strongest external cases into explicit `common-core candidate` status
- keep weaker-but-valuable cases staged
- make formal admission a separate, explicit, reviewable decision