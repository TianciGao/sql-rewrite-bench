# Performance Tri-Engine Review Synthesis v0

## 1. Document role and scope

This document is a short **synthesis note** over the current tri-engine performance review-prep packets for:

- TPC-H
- TPC-DS
- JOB / IMDB

Its role is limited to:

- cross-packet comparison
- paper-table planning
- review-prep ordering support

Live case facts remain in:

- `inventory/case_registry.csv`

This document is **not** a formal admission review, promotion decision, `common-core` movement, `extended-line` movement, or formal-review completion claim.

---

## 2. Cross-family count summary

| source family | registered tri-engine draft count | review-prep packet path | main coverage contribution | current caveat |
| --- | --- | --- | --- | --- |
| `TPC-H` | `25` | `benchmark_spec/reviews/TPCH_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md` | canonical decision-support baseline; compact, recognizable query families | some cases still carry package-layout or taxonomy/trial backfill caveats in the packet |
| `TPC-DS` | `24` | `benchmark_spec/reviews/TPCDS_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md` | broader template-derived analytical diversity across many benchmark-style query families | `PERF_0002` is registry-backed but follows an older case-local evidence layout than the later `runs/` bundle pattern |
| `JOB/IMDB` | `25` | `benchmark_spec/reviews/JOB_IMDB_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md` | join-heavy real-schema optimizer workload with broader IMDB entity-link diversity | line is evidence-complete at tri-engine draft level, but still generated/promoted and not yet formally reviewed |

Verified current total across these three source families:

- `74` registered tri-engine performance cases

---

## 3. Coverage comparison

`TPC-H` contributes the cleanest canonical decision-support baseline. Its query families are compact, familiar, and easy to discuss in review order and later paper tables.

`TPC-DS` contributes broader benchmark-style analytical diversity. Its template-derived cases expand the review surface across more parameterized reporting, aggregate, and dimension-filtering shapes than TPC-H.

`JOB / IMDB` contributes the most obviously join-heavy real-schema optimizer workload of the three groups. It broadens schema diversity and emphasizes old-style comma-join normalization and hard-negative join/filter perturbation patterns that are less central in the benchmark-template families.

Taken together, the three packets provide complementary coverage rather than redundant coverage.

---

## 4. Evidence status comparison

All three families are currently represented as registry-backed tri-engine groups.

Across the three packets, the common evidence pattern is:

- witness validation exists
- plan artifacts exist
- the groups are strong enough for review-prep and paper-table planning

What they do **not** imply by default:

- admitted status for every case
- `common-core` status for every case
- formal review completion

In other words, these are review-prep / paper-table ready groups, not universally admitted groups.

---

## 5. Backlog and exclusions

### 5.1 JOB / IMDB line

- unresolved / not counted: `PERF_0079`, `PERF_0087`, `PERF_0092`, `PERF_0100`
- legacy JOB rows not counted in the newer `JOB/IMDB` tri-engine set: `PERF_0003`, `PERF_0004`

### 5.2 TPC-DS line

Per the TPC-DS packet, current non-tri-engine backlog includes:

- PG-only cases: `PERF_0005`, `PERF_0032`, `PERF_0037`, `PERF_0039`, `PERF_0040`, `PERF_0041`, `PERF_0042`, `PERF_0045`, `PERF_0049`, `PERF_0051`, `PERF_0055`, `PERF_0057`, `PERF_0058`, `PERF_0059`, `PERF_0060`, `PERF_0061`, `PERF_0064`, `PERF_0067`, `PERF_0068`, `PERF_0069`, `PERF_0070`
- PG + MySQL but Spark-open: `PERF_0046`, `PERF_0048`
- deferred / human-decision note: `PERF_0032`

### 5.3 TPC-H line

- excluded / not tri-engine: `PERF_0029`

These backlog items should remain separated from the current tri-engine packet counts.

---

## 6. Recommended paper-table usage

Conservative paper-table candidates:

- case count by source family
- validation depth by source family
- review-prep packet summary by family
- backlog / deferred case summary by family

These tables can describe current benchmark readiness without implying that all tri-engine drafts have already passed a formal review gate.

---

## 7. Open questions before formal review

- Which subset should enter a later formal review pass first?
- Is taxonomy or mapping backfill required before that review pass?
- Should backlog cases be repaired or left deferred?
- How should the paper label tri-engine drafts without implying admission or broader benchmark-line movement?

---

## 8. Bottom line

The current performance benchmark now has a strong tri-engine draft substrate across:

- `TPC-H`
- `TPC-DS`
- `JOB/IMDB`

That substrate is suitable for paper-table planning and later human review-prep.

This document records no admission, promotion, `common-core`, `extended`, or formal-review completion claim beyond current registry facts.
