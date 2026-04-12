# PORT_0002 Admission Review v1

## 1. Document Role

This document records the second explicit admission review for `PORT_0002`.

Its purpose is to answer the updated review question:

> Given the current evidence, should `PORT_0002` remain a `common-core_candidate`, or is it now strong enough to be admitted as an external common-core case?

This file supersedes the judgment context of:

- `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v0.md`

but does not erase the historical value of that earlier review.

---

## 2. Case Under Review

**Case ID**: `PORT_0002`  
**Primary pool**: portability  
**Previous dataset-line status**: `common-core_candidate`

**Source provenance**

- Source family: PARROT
- Source subset: BIRD
- Source entry: `benchmark/BIRD/pg_res.json[0]`

**Current case structure**

- PostgreSQL-style source query
- MySQL-style positive rewrite
- MySQL-style negative rewrite
- Spark-style positive rewrite
- Spark-style negative rewrite
- witness dataset over `votes`

---

## 3. Evidence Summary

`PORT_0002` now has the following evidence:

### 3.1 Provenance
The source record, provenance note, and frozen case files are all present.

### 3.2 Source evidence
The PostgreSQL source query executes successfully.

Observed result:

- PostgreSQL `source.sql` → `1.5`

### 3.3 MySQL rewrite evidence
The MySQL target-side rewrites execute successfully.

Observed results:

- MySQL `rewrite_pos_01.sql` → `1.5`
- MySQL `rewrite_neg_01.sql` → `1`

### 3.4 Spark rewrite evidence
The Spark target-side rewrites also execute successfully.

Observed results:

- Spark `rewrite_pos_02_spark.sql` → `1.5`
- Spark `rewrite_neg_02_spark.sql` → `1.0`

### 3.5 Preservation / divergence behavior
The case now demonstrates:

- source == positive
- source != negative

for both MySQL and Spark target-side rewrites.

### 3.6 Plan evidence
Plan artifacts are now available for:

- PostgreSQL source
- MySQL positive rewrite
- MySQL negative rewrite
- Spark positive rewrite
- Spark negative rewrite

---

## 4. Review Question

Should `PORT_0002` now be admitted as an external common-core case?

---

## 5. Review Judgment

### Promotion review
**PASS**

`PORT_0002` remains clearly strong enough for `common-core` review.

### Admission review
**PASS**

`PORT_0002` is now strong enough to be admitted as an external common-core case.

---

## 6. Rationale

In `v0`, admission was deferred because the portability closure was still too narrow:

- source-side evidence was mainly in PostgreSQL
- rewrite-side evidence was mainly in MySQL
- Spark was missing

That gap has now been reduced substantially.

The case now demonstrates a reusable portability pattern:

1. a source-side PostgreSQL expression
2. a target-side MySQL positive rewrite preserving semantics
3. a target-side MySQL negative rewrite changing semantics
4. a target-side Spark positive rewrite preserving semantics
5. a target-side Spark negative rewrite changing semantics

This is now strong enough to treat `PORT_0002` not merely as a portability candidate, but as an admitted external benchmark unit.

---

## 7. Current Decision

The current decision is:

> Admit `PORT_0002` as an external common-core case.

---

## 8. Implementation Consequence

This review implies:

- `cases/PORT/PORT_0002/manifest.yaml` should move from `common-core_candidate` to `common-core`
- `cases/PORT/PORT_0002/taxonomy_trial_v0.2.yaml` should reflect admitted-common-core status
- case-local metadata should record this as an explicit admission outcome
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md` should no longer describe `PORT_0002` as merely a candidate

---

## 9. Bottom Line

`PORT_0002` has now crossed the threshold from:

> strong portability candidate

to:

> admitted external common-core portability case
