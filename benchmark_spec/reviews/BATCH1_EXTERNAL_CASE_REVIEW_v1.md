---
batch: Batch-1
review_layer: consolidated_external_case_review
supersedes:
  - benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md
  - benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md
effective_status_layer: review-history only
live_facts:
  - inventory/case_registry.csv
  - docs/EXECUTION_STATUS.md
frozen_decisions:
  - benchmark_spec/decision_log.md
---

# BATCH1_EXTERNAL_CASE_REVIEW_v1.md

## 1. Document Role

This document records the **consolidated Batch-1 external case review** for:

- `PERF_0002`
- `LONGTAIL_0002`
- `CONS_0002`
- `PORT_0002`

It merges the first-round promotion and admission judgments into one batch-scoped review record.

This file is:

- a **review-history document**
- a **project-level judgment layer**
- a **consolidated explanation** of why Batch-1 external cases currently occupy different statuses

It is not the live source-of-truth for current case facts.

---

## 2. Scope and supersession

This review covers the first Batch-1 external draft cases derived from early external source lines.

It supersedes, at the review-history layer:

- `benchmark_spec/EXTERNAL_CASE_PROMOTION_REVIEW_v0.md`
- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`

Those files remain useful as historical inputs, but this file should be treated as the consolidated Batch-1 review record.

---

## 3. Methodological boundary

The following distinctions remain in force:

### 3.1 Archetype completion is not admission
A case may already be witness-validated or archetype-complete without being formally admitted.

### 3.2 Promotion is not the same as admission
A case may be strong enough to become a `common-core candidate` without yet becoming an admitted external `common-core` case.

### 3.3 Common-core / extended is not the same as primary pool
Pool role, reporting line, promotion status, and admission status are related but different layers.

---

## 4. Consolidated review criteria

The Batch-1 review uses the following combined criteria:

- provenance completeness
- case-package completeness
- execution evidence
- rewrite behavior evidence (`source == positive`, `source != negative`)
- plan evidence
- pool-specific usefulness
- conservative admission judgment

The review does not treat “interestingness” or “one successful run” as sufficient for promotion or admission.

---

## 5. Consolidated Batch-1 review table

| case_id | primary_pool | strongest current evidence | consolidated review outcome | current interpretation | remaining blocker |
|---|---|---|---|---|---|
| `PERF_0002` | performance | tri-engine source + positive/negative validation; plan artifacts across all three engines; benchmark-shaped package | **admit as external `common-core`** | strongest external performance case in Batch 1 | release-grade stabilization still incomplete, but no longer blocked at admission level |
| `LONGTAIL_0002` | longtail | PG witness validation clearly distinguishes positive vs negative; structurally valuable long-tail coverage | **keep staged** | high-value longtail archetype / coverage case | multi-engine closure still too weak for common-core promotion |
| `CONS_0002` | consistency | PG witness validation clearly proves source/positive equivalence and source/negative divergence | **keep staged** | high-value consistency archetype / semantic methodology case | broader engine evidence and stronger package completion still needed |
| `PORT_0002` | portability | tri-engine closure now available; package skeleton complete; portability story already clear | **admit as external `common-core`** | strongest portability case in Batch 1; now stable enough to act as admitted external common-core | portability-specific deeper checker / observability work remains, but not as an admission blocker |

---

## 6. Per-case consolidated notes

### 6.1 `PERF_0002`
`PERF_0002` is the strongest Batch-1 external performance case.
It already behaves like a benchmark unit rather than an ordinary staged draft.

Consolidated outcome:

> admitted external `common-core`

### 6.2 `LONGTAIL_0002`
`LONGTAIL_0002` already demonstrates the core value of a longtail case:

- structurally rich SQL
- realistic query style
- witness-driven rewrite sensitivity
- clear positive/negative distinction

Consolidated outcome:

> keep staged / `not_yet_admitted`

Its value is real, but current evidence is still too concentrated on the PostgreSQL side for common-core promotion.

### 6.3 `CONS_0002`
`CONS_0002` already demonstrates the core value of a consistency case:

- semantic source query
- equivalent positive rewrite
- non-equivalent negative rewrite
- witness data exposing the difference

Consolidated outcome:

> keep staged / `not_yet_admitted`

Its semantic methodology value is already clear, but broader engine evidence and stronger package completion are still limited.

### 6.4 `PORT_0002`
`PORT_0002` now demonstrates the strongest portability story in Batch 1:

- source-side dialect behavior
- target-side positive preservation
- target-side negative divergence
- tri-engine validation now available
- formal skeleton complete

Consolidated outcome:

> admitted external `common-core`

The case may still benefit from deeper portability-specific checker and observability work, but that is no longer treated as an admission blocker.

---

## 7. Consolidated Batch-1 outcome

The consolidated Batch-1 outcome is:

### Admit as external `common-core`
- `PERF_0002`
- `PORT_0002`

### Keep staged / `not_yet_admitted`
- `LONGTAIL_0002`
- `CONS_0002`

This is the current consolidated interpretation of Batch 1.

---

## 8. Metadata consequence

This review implies the following metadata direction:

### `PERF_0002`
- keep as admitted external `common-core`
- use as the first admitted external performance reference case

### `PORT_0002`
- keep as admitted external `common-core`
- use as the first admitted external portability reference case

### `LONGTAIL_0002`
- keep staged
- continue treating it as a strong longtail archetype / coverage case

### `CONS_0002`
- keep staged
- continue treating it as a strong semantic methodology case

---

## 9. Why this review structure matters

Without a consolidated review layer, the repository risks:

- treating all external draft cases as equally mature
- confusing archetype completion with admission
- confusing promotion with admission
- letting old review prose and current live status drift apart

This file reduces those risks by preserving one readable record of the first Batch-1 external review cycle.

---

## 10. Current bottom line

At the current repository stage, Batch 1 has already achieved an important construction milestone:

- all four formal pools now have external-source-derived draft cases
- two external cases have crossed the line into admitted `common-core`
- two external cases remain staged for good methodological reasons

The next step is **not** broad expansion first.

The next step is:

- keep the strongest external cases admitted
- keep high-value longtail and consistency cases staged
- continue strengthening reusable construction workflow and review discipline