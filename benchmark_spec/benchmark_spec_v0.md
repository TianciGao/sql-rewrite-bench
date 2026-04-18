# benchmark_spec_v0.md

## 1. Role of this document

This file defines the **current executable benchmark contract** for the repository.

It is narrower than `docs/PROJECT_PLAN.md` and more stable than `docs/EXECUTION_STATUS.md`.

It answers:

- what the current benchmark version is
- what is currently in scope
- what is currently out of scope
- what the minimum executable repository contract is
- what must exist for the repository to count as a valid early-pilot benchmark workspace

This file does **not** replace:

- long-term project direction in `docs/PROJECT_PLAN.md`
- dynamic status interpretation in `docs/EXECUTION_STATUS.md`
- rules in `benchmark_spec/*rules*.md`
- live facts in `inventory/*.csv`
- review history in `benchmark_spec/reviews/*.md`

---

## 2. Current benchmark identity

The repository currently implements a SQL rewrite benchmark with the following fixed v0 / early-pilot identity:

- Engines / dialects:
  - Spark SQL
  - PostgreSQL
  - MySQL

- Minimum benchmark unit:
  - case package

- Current top-level evaluation dimensions:
  - correctness
  - performance
  - plan observability
  - generalization

- Current reporting lines:
  - `common-core`
  - `extended`
  - `staging / not_yet_admitted`

The benchmark is not a single-score benchmark.
It is a multi-dimension benchmark with explicit separation between correctness, performance, observability, and portability/generalization.

---

## 3. Current task tracks

### Track A — Same-engine rewrite
Given a source SQL query, evaluate whether a rewrite remains semantically valid and improves runtime within the same engine.

### Track B — Plan-observable rewrite
Evaluate whether SQL changes can be mapped to logical / physical plan changes and interpreted at the plan level.

### Track C — Cross-dialect / cross-engine rewrite
Evaluate whether a rewrite or adaptation remains executable and semantically stable across Spark SQL, PostgreSQL, and MySQL.

---

## 4. Current executable boundary

At the current repository stage, the benchmark **is** in scope for:

- tri-engine smoke and preflight checks
- case package engineering
- provenance completion
- result-checking / witness-checking paths
- plan artifact collection and normalization
- registry-first maintenance
- review-history consolidation
- reusable CLI / validator / reporting scaffolding
- selective deepening of already approved cases
- pilot characterization preparation

At the current repository stage, the benchmark is **not** in scope for:

- broad source expansion
- workload curation
- mass case generation
- unconstrained LLM case generation
- benchmark protocol redesign
- new engine families
- compositional OOD split
- engine / dialect hold-out split

---

## 5. Current repository contract

For the repository to count as a valid v0 / early-pilot benchmark workspace, the following must exist:

### 5.1 Project contract files
- `benchmark_spec/benchmark_spec_v0.md`
- `benchmark_spec/decision_log.md`
- `docs/PROJECT_PLAN.md`
- `docs/EXECUTION_STATUS.md`

### 5.2 Rules / taxonomy / schema layer
- `benchmark_spec/case_schema_v0.1.yaml`
- at least one current taxonomy file under `taxonomy/`
- the current rules files required by the repository

### 5.3 Case-package layer
- at least one case package with:
  - `manifest.yaml`
  - `source.sql`
  - at least one positive rewrite
  - at least one negative rewrite

### 5.4 Artifact layer
- `runs/smoke_case/`
- `runs/plans/`

### 5.5 Registry layer
- `inventory/source_registry.csv`
- `inventory/case_registry.csv`

Not every case must already be fully admitted.
But the repository must already support the case-package model and machine-readable artifact model.

---

## 6. Current status model

The repository distinguishes the following layers and does not collapse them:

### 6.1 Construction layer
A case may be:

- `draft_constructed`
- `witness_validated`
- `archetype_complete`

### 6.2 Promotion / admission layer
A case may be:

- `staging / not_yet_admitted`
- `common-core_candidate`
- `admitted_common_core`
- `admitted_extended`

### 6.3 Reporting-line layer
A case may belong to:

- `common-core`
- `extended`

### 6.4 Pool layer
A case may belong to:

- `performance`
- `longtail`
- `consistency`
- `portability`

These layers answer different questions and must not be merged.

---

## 7. Current engineering expectations

The current repository expects the following engineering discipline:

- registry-first updates for source / case facts
- one dynamic status dashboard (`docs/EXECUTION_STATUS.md`)
- machine-readable outputs for important checks
- reusable CLI / validator entrypoints
- plan artifacts saved per engine
- review-history separated from live facts
- no silent protocol drift

A successful engineering task at this stage should usually improve:

- reproducibility
- validation
- artifact completeness
- reportability
- case-package reusability

without changing benchmark policy.

---

## 8. Current out-of-scope changes

The following changes require explicit human approval and are out of scope for ordinary engineering work:

- changing benchmark scope
- changing engines / dialects
- changing primary metrics
- changing taxonomy principles
- changing admission semantics
- adding new workload families
- adding new benchmark cases beyond explicitly approved scope
- changing result-checking semantics
- entering workload curation
- broadening to post-v0 benchmark expansion

---

## 9. Related documents

### Long-term project direction
- `docs/PROJECT_PLAN.md`

### Current dynamic interpretation
- `docs/EXECUTION_STATUS.md`

### Rules
- `benchmark_spec/*rules*.md`

### Live facts
- `inventory/source_registry.csv`
- `inventory/case_registry.csv`

### Review history
- `benchmark_spec/reviews/*.md`

### File-role governance
- `docs/DOC_MAP.md`

---

## 10. Current bottom line

The current repository should be understood as:

> a pilot benchmark workspace with a valid case-package model, tri-engine smoke closure, plan artifact collection, rules/governance separation, and machine-readable preflight/reporting discipline.

It should **not** be understood as:

> a fully expanded benchmark release or an open-ended workload curation repo.