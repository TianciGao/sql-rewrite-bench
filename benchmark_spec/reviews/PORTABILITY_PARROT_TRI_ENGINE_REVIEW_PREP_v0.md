---
review_layer: portability_review_prep
effective_status_layer: review-prep only
live_facts:
  - inventory/case_registry.csv
  - docs/EXECUTION_STATUS.md
  - cases/PORT/PORT_0003/runs/result_check.json
  - cases/PORT/PORT_0003/runs/plan_check.json
  - cases/PORT/PORT_0004/runs/result_check.json
  - cases/PORT/PORT_0004/runs/plan_check.json
  - cases/PORT/PORT_0006/runs/result_check.json
  - cases/PORT/PORT_0006/runs/plan_check.json
frozen_decisions:
  - benchmark_spec/decision_log.md
---

# PORTABILITY_PARROT_TRI_ENGINE_REVIEW_PREP_v0.md

## 1. Title and Scope

This document is a **PARROT / BIRD portability staged draft review-prep packet**.

Covered cases:

- `PORT_0003`
- `PORT_0004`
- `PORT_0006`

Explicitly excluded cases:

- `PORT_0005`
- `PORT_0007`

Those excluded cases are not covered here because they remain draft packages without tracked validation evidence in the current repository status layer.

---

## 2. Status Boundary

This document is:

- review-prep only
- not an admission review
- not a common-core promotion
- not formal review completion
- not release-grade certification

The covered cases remain:

- staged
- `not_yet_admitted`
- `not_under_review`

Nothing in this document should be read as an admission, common-core, or formal review conclusion.

---

## 3. Case Summary Table

| case_id | source subset / source entry | source-reference engine | target engines | result_check status | plan_check status | current registry status | remaining gaps |
|---|---|---|---|---|---|---|---|
| `PORT_0003` | `BIRD` / `benchmark/BIRD/pg_res.json[3]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0004` | `BIRD` / `benchmark/BIRD/mysql_res.json[3]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0006` | `BIRD` / `benchmark/BIRD/mysql_res.json[22]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |

---

## 4. Evidence Matrix

### 4.1 `PORT_0003`

- Source reference output:
  `cases/PORT/PORT_0003/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0003/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0003/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0003/runs/spark/rewrite_pos_02_spark.tsv`
  - `cases/PORT/PORT_0003/runs/spark/rewrite_neg_02_spark.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0003/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0003/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0003/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0003/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0003/runs/spark/plans/rewrite_pos_02_spark.txt`
  - Spark: `cases/PORT/PORT_0003/runs/spark/plans/rewrite_neg_02_spark.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0003/runs/plan_check.json`

### 4.2 `PORT_0004`

- Source reference output:
  `cases/PORT/PORT_0004/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0004/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0004/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0004/runs/spark/rewrite_pos_02_spark.tsv`
  - `cases/PORT/PORT_0004/runs/spark/rewrite_neg_02_spark.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0004/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0004/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0004/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0004/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0004/runs/spark/plans/rewrite_pos_02_spark.txt`
  - Spark: `cases/PORT/PORT_0004/runs/spark/plans/rewrite_neg_02_spark.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0004/runs/plan_check.json`

### 4.3 `PORT_0006`

- Source reference output:
  `cases/PORT/PORT_0006/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0006/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0006/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0006/runs/spark/rewrite_pos_02_spark.tsv`
  - `cases/PORT/PORT_0006/runs/spark/rewrite_neg_02_spark.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0006/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0006/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0006/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0006/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0006/runs/spark/plans/rewrite_pos_02_spark.txt`
  - Spark: `cases/PORT/PORT_0006/runs/spark/plans/rewrite_neg_02_spark.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0006/runs/plan_check.json`

---

## 5. Validation Model

The covered cases use a **cross-dialect reference model**.

### 5.1 `PORT_0003`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.2 `PORT_0004`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.3 `PORT_0006`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

This validation model supports draft portability evidence, but by itself it does not imply admission or formal review completion.

---

## 6. Plan Evidence Boundary

The current plan layer should be interpreted conservatively:

- plan artifacts are tracked
- `plan_check.json` is a presence / completeness check only
- plan semantics are not formally reviewed
- no admission conclusion follows from plan presence

Case-level status within that boundary:

- `PORT_0003`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0004`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0006`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed

The current plan evidence is therefore useful as review-prep input, not as a completed portability judgment.

---

## 7. Risks and Remaining Gaps

Current risks and remaining gaps include:

- human review is still needed for all covered cases
- this portability review packet is preparatory, not dispositive
- plan semantics review still needs to happen
- admission decision remains deferred
- package release hardening remains incomplete

Case-local design notes also continue to point to portability-specific risk surfaces:

- `PORT_0003`: identifier quoting, null semantics, and top-1 / ordering portability risk
- `PORT_0004`: year extraction semantics, numeric normalization, and source-vs-target scalar portability risk
- `PORT_0006`: identifier quoting, boolean semantics, threshold-boundary semantics, and type semantics risk

These risks are consistent with keeping all covered cases staged while using the tracked draft evidence to prepare a later formal review.

---

## 8. Recommendation

Current recommendation:

- keep `PORT_0003` as `staged_not_yet_admitted`
- keep `PORT_0004` as `staged_not_yet_admitted`
- keep `PORT_0006` as `staged_not_yet_admitted`
- use this packet as the basis for a later formal portability review
- do not promote or admit any covered case yet

The current evidence is strong enough for structured review-prep, but not yet for admission, common-core promotion, or formal review closure.
