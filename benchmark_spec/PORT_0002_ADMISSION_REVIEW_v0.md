# PORT_0002 Admission Review v0

## 1. Document Role

This document records the first explicit admission review for `PORT_0002`.

Its purpose is to answer a narrower question than the broader external-draft status summary:

> Given the current evidence, should `PORT_0002` remain a `common-core_candidate`, or should it now be admitted as an external common-core case?

This document does not replace:

- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`
- case-local manifests and taxonomy files

Instead, it serves as the project-level review note for this specific portability case.

---

## 2. Case Under Review

**Case ID**: `PORT_0002`  
**Primary pool**: portability  
**Current dataset-line status**: `common-core_candidate`

**Source provenance**

- Source family: PARROT
- Source subset: BIRD
- Source entry: `benchmark/BIRD/pg_res.json[0]`

**Current case structure**

- PostgreSQL-style source query
- MySQL-style positive rewrite
- MySQL-style negative rewrite
- witness dataset over `votes`

---

## 3. Current Evidence Summary

`PORT_0002` currently has the following evidence:

### 3.1 Provenance
The source record, provenance note, and frozen case files are all present.

### 3.2 Source evidence
The PostgreSQL source query has been executed successfully on the witness dataset.

Observed source result:

- PostgreSQL `source.sql` → `1.5`

### 3.3 Positive rewrite evidence
The MySQL positive rewrite has been executed successfully on the witness dataset.

Observed positive result:

- MySQL `rewrite_pos_01.sql` → `1.5`

This preserves the source result.

### 3.4 Negative rewrite evidence
The MySQL negative rewrite has also been executed successfully.

Observed negative result:

- MySQL `rewrite_neg_01.sql` → `1`

This diverges from the source result.

### 3.5 Plan evidence
Plan artifacts have been collected for:

- PostgreSQL source
- MySQL positive rewrite
- MySQL negative rewrite

### 3.6 Current portability value
The case already demonstrates a clear portability story:

- PostgreSQL-style year extraction in the source
- MySQL-style year extraction in the positive rewrite
- a negative range-boundary rewrite that appears plausible but changes the result

This is already strong portability evidence.

---

## 4. Review Question

Should `PORT_0002` now be admitted as an external common-core case?

---

## 5. Review Judgment

### Promotion review
**PASS**

`PORT_0002` is strong enough to remain under explicit `common-core_candidate` review.

### Admission review
**NOT YET**

`PORT_0002` should **not yet** be admitted as an external common-core case.

---

## 6. Rationale

`PORT_0002` is already a strong portability draft case, but the current evidence is still narrower than the evidence used to admit `PERF_0002`.

The main reasons for not admitting it yet are:

1. **Cross-engine closure is still incomplete**
   - PostgreSQL source is validated
   - MySQL positive and negative are validated
   - Spark is not yet part of this case's closure story

2. **The current validation is asymmetric**
   - source-side evidence is strongest in PostgreSQL
   - rewrite-side evidence is strongest in MySQL
   - this is meaningful for portability, but still weaker than a broader admitted common-core case

3. **The case is already useful without admission**
   - it already functions well as a `common-core_candidate`
   - immediate admission is not required for it to contribute benchmark value

In other words:

> `PORT_0002` is already strong enough for promotion review, but not yet strong enough for final admission.

---

## 7. Current Decision

The current decision is:

- keep `PORT_0002` as **`common-core_candidate`**
- do **not** admit it yet
- revisit admission after broader validation evidence is available

---

## 8. Implementation Consequence

This review implies:

- `cases/PORT/PORT_0002/manifest.yaml` should continue to use `dataset_line_candidate: common-core_candidate`
- `cases/PORT/PORT_0002/taxonomy_trial_v0.2.yaml` should remain aligned with candidate status
- no admitted-common-core flag should be added yet
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md` should continue to describe `PORT_0002` as the strongest remaining candidate after `PERF_0002`

---

## 9. Suggested Next Step

The next most useful step for `PORT_0002` is **not** immediate admission.

The next step should instead be one of the following:

1. broaden validation evidence
2. improve closure story around source/rewrite symmetry
3. revisit admission after that additional evidence is collected

Until then, `PORT_0002` should remain the strongest portability candidate rather than an admitted case.

---

## 10. Bottom Line

`PORT_0002` has already passed the threshold for:

> **serious common-core candidate review**

But it has **not yet** passed the threshold for:

> **admitted external common-core case**

Therefore, the correct current status is:

> **keep as `common-core_candidate`**