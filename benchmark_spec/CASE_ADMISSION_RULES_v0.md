# CASE_ADMISSION_RULES_v0.md

## 1. Role of this document

This file defines the rules for **formal case admission**.

It answers a narrower project-level question than archetype completion:

> When is a case strong enough to be treated as part of the benchmark's admitted population?

This document does **not** define:

- long-term project direction
- live case facts
- batch-specific review history
- current status dashboard interpretation

Related but different documents:

- `benchmark_spec/benchmark_spec_v0.md`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/decision_log.md`
- `benchmark_spec/reviews/*.md`

---

## 2. Core distinctions

### 2.1 Archetype completion is not formal admission
A case may already be:

- `draft_constructed`
- `witness_validated`
- `archetype_complete`

without being admitted.

Archetype completion is a construction threshold.  
Admission is a benchmark-governance decision.

### 2.2 Candidate status is not formal admission
A case may be marked as:

- `common-core_candidate`

without becoming:

- `admitted_common_core`

Candidate status means the case is strong enough to be seriously reviewed.
It does not mean the project has already admitted it.

### 2.3 Reporting line is not pool assignment
A case's admission outcome may interact with `common-core` / `extended`, but that does not replace its `primary_pool`.

---

## 3. Admission status labels

This ruleset recognizes the following project-level admission states:

### `staging_not_yet_admitted`
The case is still below formal admission threshold or still under evidence gathering.

### `common-core_candidate`
The case appears strong enough to be reviewed for `common-core`, but formal admission has not yet been granted.

### `admitted_common_core`
The case has passed admission review and belongs to the admitted `common-core` benchmark population.

### `admitted_extended`
The case is admitted as a benchmark case, but it belongs to the controlled `extended` line rather than the main `common-core` line.

---

## 4. Shared admission minimum

A case should not be formally admitted unless all of the following are true.

### 4.1 Identity and provenance
The case has:

- stable `case_id`
- explicit pool assignment or final candidate pool
- explicit provenance
- explicit source/seed lineage

### 4.2 Case-package completeness
The case has at least:

- `manifest.yaml`
- `source.sql`
- positive rewrite where methodologically required
- negative rewrite where methodologically required
- machine-readable profile artifact
- taxonomy layer

### 4.3 Data / witness clarity
The case has an explicit and reproducible data strategy:

- imported subset
- witness dataset
- generated subset
- or manually constructed witness data

### 4.4 Execution evidence
The case has actual execution evidence on the engines required for its current admission target.

### 4.5 Result-checking path
The case has either:

- an explicit checker
- or a clearly reproducible result-comparison path

### 4.6 Plan evidence
The case has plan artifacts for the validated engines that matter for its current admission target.

### 4.7 Registry / metadata completeness
The case has a usable row in `inventory/case_registry.csv` with:

- current maturity
- benchmark line
- package engineering state
- validated engines
- admission-related blockers / next gap
- review pointer where relevant

---

## 5. Common-core admission rules

A case may be admitted as `admitted_common_core` only if:

1. it satisfies the shared admission minimum
2. it satisfies the current `common-core` rules
3. the expected engines for the comparison are all executable
4. cross-engine result comparison is available and considered fair
5. the case does not depend on unstable or strongly engine-specific semantics that would break the fairness of the main comparison set
6. a project-level review basis exists

In the current v0 / early-pilot setting, this normally means:

- Spark SQL, PostgreSQL, and MySQL execution evidence
- result comparability across the three engines
- stable enough interpretation to belong to the main benchmark score/report set

---

## 6. Extended admission rules

A case may be admitted as `admitted_extended` only if:

1. it satisfies the shared admission minimum
2. it is relevant to at least one formal pool
3. it has meaningful benchmark value
4. it does not satisfy full `common-core` requirements
5. its limitations are explicit
6. a project-level review basis exists

Typical reasons for `admitted_extended` include:

- partial engine support
- meaningful coverage value but imperfect cross-engine fairness
- dialect-specific or engine-specific retained value

`extended` is not a discard bucket.
It is a controlled admitted population outside the main `common-core` set.

---

## 7. Non-admission blockers

A case should remain `staging_not_yet_admitted` if any of the following remain unresolved:

- provenance is incomplete
- pool assignment is not yet stable
- source meaning is still unclear
- positive / negative layer is missing where required
- witness / data strategy is unclear
- execution evidence is incomplete for the intended admission target
- result-checking path is missing
- plan artifacts are missing for relevant validated engines
- registry row is incomplete
- semantics are still under review
- fair `common-core` comparison is not yet established

A single successful execution is not enough.
Interestingness is not enough.
A promising archetype is not enough.

---

## 8. Admission workflow

Formal admission should follow this order:

1. determine whether the case is structurally mature enough for review
2. determine pool assignment
3. determine whether the target line is `common-core` or `extended`
4. record the review outcome
5. update the live registry state
6. update current-status interpretation if needed

This avoids confusing:

- archetype completion
- candidate status
- reporting line
- formal admission

---

## 9. Update protocol

If a formal admission judgment is made or changed, the update order should be:

1. update the relevant review-history file
2. update `benchmark_spec/decision_log.md` if the decision is project-level and frozen
3. update `inventory/case_registry.csv`
4. update `docs/EXECUTION_STATUS.md` if the representative snapshot changes

Do not change admission only in prose while leaving registries stale.

---

## 10. Current bottom line

Formal admission should remain conservative.

The project should not ask only:

> “Is this case interesting?”

It should ask:

> “Is this case complete, evidenced, review-backed, and stable enough to be treated as part of the admitted benchmark population?”