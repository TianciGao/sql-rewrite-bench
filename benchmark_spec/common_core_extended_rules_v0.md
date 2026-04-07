# Common-Core and Extended Rules v0

## 1. Role of this document

This file defines how the benchmark separates cases into:

- common-core
- extended

Its purpose is to prevent unfair comparisons and to keep broad coverage without collapsing everything into one mixed leaderboard.

For pool rules, see `docs/POOL_MAPPING_RULES.md`.
For current benchmark boundary, see `benchmark_spec/benchmark_spec_v0.md`.

---

## 2. Why this split exists

A SQL rewrite benchmark serves two goals that are often in tension:

1. fair cross-engine comparison
2. broad real-world coverage

If the benchmark keeps only the smallest shared subset, it becomes too conservative.
If the benchmark mixes all cases together, comparisons become noisy and unfair.

The common-core / extended split exists to preserve both:
- common-core = comparable core
- extended = richer but less uniformly comparable coverage

---

## 3. Definitions

## 3.1 Common-Core
A case belongs to **common-core** if it satisfies all of the following:

1. it is executable in all intended current engines for the relevant task
2. result comparison is available across those engines
3. the case semantics are stable enough for direct cross-engine reporting
4. the case does not rely on unsupported or highly engine-specific constructs for its core meaning

Current intended engines:
- Spark SQL
- PostgreSQL
- MySQL

Common-core is the primary set for fair horizontal comparison.

---

## 3.2 Extended
A case belongs to **extended** if it is benchmark-relevant but does not satisfy full common-core requirements.

Typical reasons:
- only a subset of current engines can execute it
- a dialect-specific construct is important to keep
- it is highly valuable for coverage, but not fully fair for cross-engine comparison
- it is still useful as a benchmark case, but should not be mixed into the common-core scoreboard

Extended is not a discard bucket.
It is a controlled expansion set.

---

## 4. Decision rules

## 4.1 Common-Core admission rule
A case may be labeled `common-core` only if:

- all intended engines in scope can execute it
- result consistency can be checked across those engines
- the comparison is considered fair enough for primary reporting
- no major engine-specific semantics dominate the meaning of the case

## 4.2 Extended admission rule
A case may be labeled `extended` if:

- it is relevant to at least one formal pool
- it adds meaningful benchmark value
- it preserves provenance and case metadata
- it fails one or more common-core requirements, but is still useful

---

## 5. Relationship with formal pools

Common-core / extended is **not** a replacement for primary pool.

Each admitted case should still have:
- one `candidate_primary_pool` or final `primary_pool`
- one dataset line:
  - `common-core`
  - or `extended`

Example:
- a case may be `primary_pool = longtail` and `dataset_line = common-core`
- another case may be `primary_pool = portability` and `dataset_line = extended`

Pool answers: **what kind of benchmark question this case serves**  
Dataset line answers: **how this case should be reported and compared**

---

## 6. Current v0 rule

In the current early pilot stage:

- cases should default to `common-core` only when tri-engine execution and result comparison have already been demonstrated
- cases that are still missing execution or comparison evidence should not be assumed to be common-core
- cases with unresolved engine-specific semantics should remain in `extended` or `not_yet_admitted`

---

## 7. Current not-yet-admitted rule

A case should remain outside both common-core and extended if any of the following is still unresolved:

- provenance is incomplete
- primary pool is unclear
- result checker is incomplete
- tri-engine (or intended-engine) execution has not been demonstrated
- semantics are still under review

Such a case should be marked as:
- `staging`
- or `not_yet_admitted`

---

## 8. Reporting rule

For the current benchmark version:

1. common-core results should be reported first
2. extended results should be reported separately
3. common-core and extended should not be merged into one undifferentiated score
4. if a metric is reported on extended only, that must be stated explicitly

---

## 9. Upgrade / downgrade rule

A case may be upgraded:
- from `not_yet_admitted` → `extended`
- from `extended` → `common-core`

only when the required evidence becomes available.

A case may also be downgraded:
- from `common-core` → `extended`

if later evidence shows that cross-engine comparison is not actually fair or stable.

Such changes should be documented in project notes and, when policy changes are involved, in `benchmark_spec/decision_log.md`.

---

## 10. Current practical guidance

For the current repository stage, use the following decision order:

1. decide whether the case is admitted at all
2. assign candidate / primary pool
3. decide whether it belongs to common-core or extended
4. only then include it in summaries or benchmark tables

This order prevents source-level assumptions from being confused with final case-level reporting.