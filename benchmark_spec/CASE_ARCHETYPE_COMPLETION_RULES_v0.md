# Case Archetype Completion Rules v0

## 1. Document Role

This document defines what it means for a case to be **archetype-complete**.

Its purpose is not to decide formal benchmark admission.
Instead, it defines when a case is complete enough to serve as a **reusable construction prototype** for future large-scale case building.

This document therefore answers a narrower methodological question:

> When can a case be considered complete enough to act as the standard pattern for its pool?

Related but different documents:

- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`
- `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`

---

## 2. Core Distinction

### 2.1 Archetype completion is not the same as admission

A case may be archetype-complete without being formally admitted.

Archetype completion means:

- the case has enough structure
- the case has enough evidence
- the case has enough metadata
- the construction workflow is clear enough to reuse

Formal admission means:

- the project is willing to treat that case as part of the benchmark's admitted population

Therefore:

- **archetype completion** is a construction and methodology threshold
- **admission** is a project-level benchmark decision

### 2.2 Why this distinction matters

The project plans to construct many future cases.

That means the current `002` cases should not only be treated as isolated examples.
They should be treated as **pool-specific archetypes**.

The main purpose of archetype completion is therefore to ensure that future cases can be built by following a stable template rather than by re-thinking the workflow from scratch every time.

---

## 3. Scope

This ruleset applies to the four major case archetypes represented by the current `002` cases:

- performance archetype
- longtail archetype
- consistency archetype
- portability archetype

The current intended reference cases are:

- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

---

## 4. Shared Completion Layers

Every archetype-complete case should satisfy the following shared layers.

### 4.1 Identity and provenance
The case must have:

- stable `case_id`
- pool assignment
- frozen provenance
- explicit source / seed lineage
- case-local provenance files

### 4.2 Frozen source layer
The case must include:

- `source.sql`
- a stable interpretation of what the source means
- case-local notes explaining why this source was selected

### 4.3 Rewrite layer
When applicable, the case should include:

- at least one positive rewrite
- at least one negative rewrite

The rewrite layer must be consistent with the pool's methodological purpose.

### 4.4 Dataset layer
The case must include at least one usable data strategy:

- full imported data subset
- minimal generated subset
- witness dataset
- manually constructed witness data

The data strategy must be explicit and reproducible.

### 4.5 Execution layer
The case must include actual execution evidence on the engines required by that archetype.

### 4.6 Plan layer
The case must include plan artifacts for the validated engine(s) that matter for the archetype.

### 4.7 Taxonomy layer
The case must include:

- `taxonomy_trial_v0.2.yaml`
- pool-relevant tags
- provisional but meaningful plan/operator tags when available

### 4.8 Machine-readable profile layer
The case must include at least one machine-readable profile artifact, typically:

- `data_profile.json`

### 4.9 Checker layer
Whenever the archetype depends on equivalence or divergence, the case should include a small checker or explicit result comparison workflow.

---

## 5. Archetype Completion Status Labels

This document uses the following construction labels.

### `draft_constructed`
The case exists structurally but does not yet demonstrate its pool's core value.

### `witness_validated`
The case has enough data and execution evidence to demonstrate its main behavior on at least one relevant engine.

### `archetype_complete`
The case is complete enough to serve as the reference pattern for future cases in the same pool.

### `common-core_candidate`
The case is not only archetype-complete, but also strong enough to be considered for common-core promotion.

### `admitted_common_core`
The case has passed a separate project-level admission decision and is no longer just a prototype.

---

## 6. Pool-Specific Completion Rules

## 6.1 Performance Archetype

### Goal
A performance archetype should demonstrate a reusable pattern for:

- stable analytical source construction
- cross-engine execution
- meaningful positive/negative rewrite behavior
- plan observability

### Minimum rule for `archetype_complete`
A performance case is archetype-complete when it has:

- complete provenance
- frozen `source.sql`
- positive rewrite
- negative rewrite
- reusable data subset
- source execution on PostgreSQL, MySQL, and Spark
- positive rewrite validated as result-preserving on PostgreSQL, MySQL, and Spark
- negative rewrite validated as result-changing on PostgreSQL, MySQL, and Spark
- plans collected on PostgreSQL, MySQL, and Spark
- taxonomy trial
- data profile
- a result comparison/checker path

### Promotion tendency
A performance archetype that reaches this threshold is a strong candidate for `common-core_candidate` and possibly admission.

---

## 6.2 Longtail Archetype

### Goal
A longtail archetype should demonstrate a reusable pattern for:

- structurally rich SQL
- non-trivial syntax / logic coverage
- rewrite sensitivity on a controlled witness dataset

### Minimum rule for `archetype_complete`
A longtail case is archetype-complete when it has:

- complete provenance
- frozen `source.sql`
- positive rewrite
- negative rewrite
- explicit witness or minimal dataset
- source execution on at least one primary engine
- positive rewrite validated as result-preserving on that engine
- negative rewrite validated as result-changing on that engine
- at least one source plan on a validated engine
- taxonomy trial
- data profile
- a result comparison/checker path

### Promotion tendency
Longtail archetypes do not need immediate multi-engine closure to be archetype-complete.
They may remain staged even after archetype completion.

---

## 6.3 Consistency Archetype

### Goal
A consistency archetype should demonstrate a reusable pattern for:

- semantic source query
- semantically equivalent positive rewrite
- semantically incorrect negative rewrite
- witness data that exposes the difference

### Minimum rule for `archetype_complete`
A consistency case is archetype-complete when it has:

- complete provenance
- frozen `source.sql`
- positive rewrite
- negative rewrite
- explicit witness dataset
- source execution on at least one primary engine
- positive rewrite validated as result-preserving on that engine
- negative rewrite validated as result-changing on that engine
- plan artifact for at least the source and preferably rewrites
- taxonomy trial
- data profile
- explicit checker or clearly reproducible comparison path

### Promotion tendency
Consistency archetypes can be archetype-complete while still remaining staged, because their first job is to prove semantic methodology, not immediate cross-engine admission.

---

## 6.4 Portability Archetype

### Goal
A portability archetype should demonstrate a reusable pattern for:

- source dialect behavior
- target dialect rewrite behavior
- positive portability preservation
- negative portability failure

### Minimum rule for `archetype_complete`
A portability case is archetype-complete when it has:

- complete provenance
- frozen source query
- positive rewrite in the target dialect
- negative rewrite in the target dialect
- explicit witness dataset
- source execution on the source-side engine
- positive rewrite execution on the target-side engine
- negative rewrite execution on the target-side engine
- clear positive preservation and negative divergence
- plan artifacts for the validated engines
- taxonomy trial
- data profile
- explicit portability checker or reproducible comparison path

### Promotion tendency
A portability archetype can become a `common-core_candidate` without full three-engine closure, but admission should remain conservative.

---

## 7. Minimum File / Artifact Matrix

| artifact | performance | longtail | consistency | portability |
|---|---|---|---|---|
| `manifest.yaml` | required | required | required | required |
| `taxonomy_trial_v0.2.yaml` | required | required | required | required |
| provenance files | required | required | required | required |
| `source.sql` | required | required | required | required |
| `rewrite_pos_01.sql` | required | required | required | required |
| `rewrite_neg_01.sql` | required | required | required | required |
| `data_profile.json` | required | required | required | required |
| source result artifact | required | required | required | required |
| positive result artifact | required | required | required | required |
| negative result artifact | required | required | required | required |
| plan artifact(s) | required | required | required | required |
| checker or explicit comparison | required | required | required | required |

---

## 8. Current Intended Interpretation of the `002` Cases

The current intended use of the four `002` cases is:

- `PERF_0002` → performance archetype
- `LONGTAIL_0002` → longtail archetype
- `CONS_0002` → consistency archetype
- `PORT_0002` → portability archetype

The project should judge them first against **archetype completion** rules, and only then decide whether to admit or stage them.

---

## 9. Practical Use in Future Scaling

Future cases should not be built by improvising from scratch.

Instead, for each future case, the constructor should ask:

1. Which archetype does this case belong to?
2. Which completion rule applies?
3. Which shared layers are still missing?
4. Is the case merely a draft, archetype-complete, a candidate, or admitted?

This turns the current `002` cases into reusable templates for later batch construction.

---

## 10. Update Rule

This file should be updated whenever:

- the project changes what “archetype-complete” means
- a new pool-specific archetype is introduced
- the minimum file/artifact matrix changes
- the project concludes that one archetype needs stricter or looser completion standards

Related updates should also be reflected in:

- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`
- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`
- case-local manifests and taxonomy files

---

## 11. Current Bottom Line

The `002` cases should be completed not merely as four isolated examples, but as four reusable archetypes.

That means the success criterion is not:

> “Did we manage to build this one case?”

The real criterion is:

> “Did we make the construction method reusable for the next hundreds of cases?”