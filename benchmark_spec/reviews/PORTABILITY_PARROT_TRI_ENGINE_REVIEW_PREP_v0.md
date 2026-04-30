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
  - cases/PORT/PORT_0005/runs/result_check.json
  - cases/PORT/PORT_0005/runs/plan_check.json
  - cases/PORT/PORT_0006/runs/result_check.json
  - cases/PORT/PORT_0006/runs/plan_check.json
  - cases/PORT/PORT_0008/runs/result_check.json
  - cases/PORT/PORT_0008/runs/plan_check.json
  - cases/PORT/PORT_0009/runs/result_check.json
  - cases/PORT/PORT_0009/runs/plan_check.json
  - cases/PORT/PORT_0010/runs/result_check.json
  - cases/PORT/PORT_0010/runs/plan_check.json
  - cases/PORT/PORT_0011/runs/result_check.json
  - cases/PORT/PORT_0011/runs/plan_check.json
  - cases/PORT/PORT_0012/runs/result_check.json
  - cases/PORT/PORT_0012/runs/plan_check.json
  - cases/PORT/PORT_0013/runs/result_check.json
  - cases/PORT/PORT_0013/runs/plan_check.json
  - cases/PORT/PORT_0014/runs/result_check.json
  - cases/PORT/PORT_0014/runs/plan_check.json
  - cases/PORT/PORT_0015/runs/result_check.json
  - cases/PORT/PORT_0015/runs/plan_check.json
  - cases/PORT/PORT_0016/runs/result_check.json
  - cases/PORT/PORT_0016/runs/plan_check.json
  - cases/PORT/PORT_0017/runs/result_check.json
  - cases/PORT/PORT_0017/runs/plan_check.json
  - cases/PORT/PORT_0018/runs/result_check.json
  - cases/PORT/PORT_0018/runs/plan_check.json
  - cases/PORT/PORT_0019/runs/result_check.json
  - cases/PORT/PORT_0019/runs/plan_check.json
  - cases/PORT/PORT_0020/runs/result_check.json
  - cases/PORT/PORT_0020/runs/plan_check.json
  - cases/PORT/PORT_0021/runs/result_check.json
  - cases/PORT/PORT_0021/runs/plan_check.json
  - cases/PORT/PORT_0022/runs/result_check.json
  - cases/PORT/PORT_0022/runs/plan_check.json
  - cases/PORT/PORT_0023/runs/result_check.json
  - cases/PORT/PORT_0023/runs/plan_check.json
  - cases/PORT/PORT_0024/runs/result_check.json
  - cases/PORT/PORT_0024/runs/plan_check.json
  - cases/PORT/PORT_0025/runs/result_check.json
  - cases/PORT/PORT_0025/runs/plan_check.json
frozen_decisions:
  - benchmark_spec/decision_log.md
---

# PORTABILITY_PARROT_TRI_ENGINE_REVIEW_PREP_v0.md

## 1. Title and Scope

This document is a **PARROT / BIRD portability staged draft review-prep packet**.

Covered cases:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0006`
- `PORT_0008`
- `PORT_0009`
- `PORT_0010`
- `PORT_0011`
- `PORT_0012`
- `PORT_0013`
- `PORT_0014`
- `PORT_0015`
- `PORT_0016`
- `PORT_0017`
- `PORT_0018`
- `PORT_0019`
- `PORT_0020`
- `PORT_0021`
- `PORT_0022`
- `PORT_0023`
- `PORT_0024`
- `PORT_0025`

Explicitly excluded cases:

- `PORT_0007`

Those excluded cases are not covered here because they remain outside the current registry-backed staged PARROT tri-engine draft subset used in this review-prep packet.

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
| `PORT_0005` | `BIRD` / `benchmark/BIRD/pg_res.json[9]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0006` | `BIRD` / `benchmark/BIRD/mysql_res.json[22]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0008` | `BIRD` / `benchmark/BIRD/pg_res.json[4]` | PostgreSQL | MySQL, Spark | `draft_result_artifacts_present`, `ok=true` | `draft_plan_artifacts_present`, `ok=true` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0009` | `BIRD` / `benchmark/BIRD/pg_res.json[6]` | PostgreSQL | MySQL, Spark | `draft_result_artifacts_present`, `ok=true` | `draft_plan_artifacts_present`, `ok=true` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0010` | `BIRD` / `benchmark/BIRD/pg_res.json[10]` | PostgreSQL | MySQL, Spark | `draft_result_artifacts_present`, `ok=true` | `draft_plan_artifacts_present`, `ok=true` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0011` | `BIRD` / `benchmark/BIRD/pg_res.json[11]` | PostgreSQL | MySQL, Spark | `draft_result_artifacts_present`, `ok=true` | `draft_plan_artifacts_present`, `ok=true` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0012` | `BIRD` / `benchmark/BIRD/pg_res.json[12]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0013` | `BIRD` / `benchmark/BIRD/mysql_res.json[23]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0014` | `BIRD` / `benchmark/BIRD/mysql_res.json[25]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0015` | `BIRD` / `benchmark/BIRD/mysql_res.json[41]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0016` | `BIRD` / `benchmark/BIRD/mysql_res.json[44]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0017` | `BIRD` / `benchmark/BIRD/mysql_res.json[46]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0018` | `BIRD` / `benchmark/BIRD/pg_res.json[14]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0019` | `BIRD` / `benchmark/BIRD/pg_res.json[15]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0020` | `BIRD` / `benchmark/BIRD/pg_res.json[16]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0021` | `BIRD` / `benchmark/BIRD/pg_res.json[17]` | PostgreSQL | MySQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0022` | `BIRD` / `benchmark/BIRD/mysql_res.json[0]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0023` | `BIRD` / `benchmark/BIRD/mysql_res.json[5]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0024` | `BIRD` / `benchmark/BIRD/mysql_res.json[18]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |
| `PORT_0025` | `BIRD` / `benchmark/BIRD/mysql_res.json[47]` | MySQL | PostgreSQL, Spark | `validated`, `ok=true` | `complete` | registry-backed staged draft; `staged_not_yet_admitted`; `not_yet_admitted`; `not_under_review` | human review; portability review-prep packet follow-through; later admission decision; plan semantics not formally reviewed |

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

### 4.3 `PORT_0005`

- Source reference output:
  `cases/PORT/PORT_0005/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0005/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0005/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0005/runs/spark/rewrite_pos_02_spark.tsv`
  - `cases/PORT/PORT_0005/runs/spark/rewrite_neg_02_spark.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0005/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0005/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0005/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0005/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0005/runs/spark/plans/rewrite_pos_02_spark.txt`
  - Spark: `cases/PORT/PORT_0005/runs/spark/plans/rewrite_neg_02_spark.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0005/runs/plan_check.json`

### 4.4 `PORT_0006`

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

### 4.5 `PORT_0008`

- Source reference output:
  `cases/PORT/PORT_0008/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0008/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0008/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0008/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0008/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0008/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0008/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0008/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0008/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0008/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0008/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0008/runs/plan_check.json`

### 4.6 `PORT_0009`

- Source reference output:
  `cases/PORT/PORT_0009/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0009/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0009/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0009/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0009/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0009/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0009/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0009/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0009/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0009/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0009/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0009/runs/plan_check.json`

### 4.7 `PORT_0010`

- Source reference output:
  `cases/PORT/PORT_0010/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0010/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0010/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0010/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0010/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0010/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0010/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0010/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0010/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0010/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0010/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0010/runs/plan_check.json`

### 4.8 `PORT_0011`

- Source reference output:
  `cases/PORT/PORT_0011/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0011/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0011/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0011/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0011/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0011/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0011/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0011/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0011/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0011/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0011/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0011/runs/plan_check.json`

### 4.9 `PORT_0012`

- Source reference output:
  `cases/PORT/PORT_0012/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0012/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0012/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0012/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0012/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0012/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0012/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0012/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0012/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0012/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0012/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0012/runs/plan_check.json`

### 4.10 `PORT_0013`

- Source reference output:
  `cases/PORT/PORT_0013/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0013/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0013/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0013/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0013/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0013/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0013/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0013/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0013/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0013/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0013/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0013/runs/plan_check.json`

### 4.11 `PORT_0014`

- Source reference output:
  `cases/PORT/PORT_0014/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0014/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0014/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0014/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0014/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0014/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0014/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0014/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0014/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0014/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0014/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0014/runs/plan_check.json`

### 4.12 `PORT_0015`

- Source reference output:
  `cases/PORT/PORT_0015/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0015/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0015/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0015/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0015/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0015/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0015/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0015/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0015/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0015/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0015/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0015/runs/plan_check.json`

### 4.13 `PORT_0017`

- Source reference output:
  `cases/PORT/PORT_0017/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0017/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0017/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0017/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0017/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0017/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0017/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0017/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0017/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0017/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0017/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0017/runs/plan_check.json`

### 4.14 `PORT_0016`

- Source reference output:
  `cases/PORT/PORT_0016/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0016/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0016/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0016/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0016/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0016/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0016/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0016/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0016/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0016/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0016/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0016/runs/plan_check.json`

### 4.15 `PORT_0018`

- Source reference output:
  `cases/PORT/PORT_0018/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0018/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0018/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0018/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0018/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0018/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0018/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0018/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0018/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0018/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0018/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0018/runs/plan_check.json`

### 4.16 `PORT_0019`

- Source reference output:
  `cases/PORT/PORT_0019/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0019/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0019/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0019/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0019/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0019/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0019/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0019/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0019/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0019/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0019/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0019/runs/plan_check.json`

### 4.17 `PORT_0020`

- Source reference output:
  `cases/PORT/PORT_0020/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0020/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0020/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0020/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0020/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0020/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0020/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0020/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0020/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0020/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0020/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0020/runs/plan_check.json`

### 4.18 `PORT_0021`

- Source reference output:
  `cases/PORT/PORT_0021/runs/pg/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0021/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0021/runs/mysql/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0021/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0021/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0021/runs/result_check.json`
- Plan files by engine:
  - PostgreSQL: `cases/PORT/PORT_0021/runs/pg/plans/source.json`
  - MySQL: `cases/PORT/PORT_0021/runs/mysql/plans/rewrite_pos_01.json`
  - MySQL: `cases/PORT/PORT_0021/runs/mysql/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0021/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0021/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0021/runs/plan_check.json`

### 4.19 `PORT_0022`

- Source reference output:
  `cases/PORT/PORT_0022/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0022/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0022/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0022/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0022/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0022/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0022/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0022/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0022/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0022/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0022/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0022/runs/plan_check.json`

### 4.20 `PORT_0023`

- Source reference output:
  `cases/PORT/PORT_0023/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0023/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0023/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0023/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0023/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0023/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0023/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0023/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0023/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0023/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0023/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0023/runs/plan_check.json`

### 4.21 `PORT_0024`

- Source reference output:
  `cases/PORT/PORT_0024/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0024/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0024/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0024/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0024/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0024/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0024/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0024/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0024/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0024/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0024/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0024/runs/plan_check.json`

### 4.22 `PORT_0025`

- Source reference output:
  `cases/PORT/PORT_0025/runs/mysql/source.tsv`
- Target positive / negative outputs:
  - `cases/PORT/PORT_0025/runs/pg/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0025/runs/pg/rewrite_neg_01.tsv`
  - `cases/PORT/PORT_0025/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/PORT_0025/runs/spark/rewrite_neg_01.tsv`
- Result evidence summary:
  `cases/PORT/PORT_0025/runs/result_check.json`
- Plan files by engine:
  - MySQL: `cases/PORT/PORT_0025/runs/mysql/plans/source.json`
  - PostgreSQL: `cases/PORT/PORT_0025/runs/pg/plans/rewrite_pos_01.json`
  - PostgreSQL: `cases/PORT/PORT_0025/runs/pg/plans/rewrite_neg_01.json`
  - Spark: `cases/PORT/PORT_0025/runs/spark/plans/rewrite_pos_01.txt`
  - Spark: `cases/PORT/PORT_0025/runs/spark/plans/rewrite_neg_01.txt`
- Plan evidence summary:
  `cases/PORT/PORT_0025/runs/plan_check.json`

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

### 5.4 `PORT_0005`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.5 `PORT_0008`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.6 `PORT_0009`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.7 `PORT_0010`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.8 `PORT_0011`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.9 `PORT_0012`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.10 `PORT_0013`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.11 `PORT_0014`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.12 `PORT_0015`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.13 `PORT_0017`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.14 `PORT_0016`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.15 `PORT_0018`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.16 `PORT_0019`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.17 `PORT_0020`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.18 `PORT_0021`

- PostgreSQL source output is the semantic reference.
- MySQL and Spark run target rewrites only.
- Positive rewrites must equal the PostgreSQL source reference.
- Negative rewrites must differ from the PostgreSQL source reference.

### 5.19 `PORT_0022`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.20 `PORT_0023`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.21 `PORT_0024`

- MySQL source output is the semantic reference.
- PostgreSQL and Spark run target rewrites only.
- Positive rewrites must equal the MySQL source reference.
- Negative rewrites must differ from the MySQL source reference.

### 5.22 `PORT_0025`

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
- `PORT_0005`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0006`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0008`: `result_check.json` `ok=true`; `plan_check.json` indicates tracked draft plan artifacts are present; plan semantics not formally reviewed
- `PORT_0009`: `result_check.json` `ok=true`; `plan_check.json` indicates tracked draft plan artifacts are present; plan semantics not formally reviewed
- `PORT_0010`: `result_check.json` `ok=true`; `plan_check.json` indicates tracked draft plan artifacts are present; plan semantics not formally reviewed
- `PORT_0011`: `result_check.json` `ok=true`; `plan_check.json` indicates tracked draft plan artifacts are present; plan semantics not formally reviewed
- `PORT_0012`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0013`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0014`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0015`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0016`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0017`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0018`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0019`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0020`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0021`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0022`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0023`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0024`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed
- `PORT_0025`: `result_check.json` `ok=true`; `plan_check.json` `status=complete`; plan semantics not formally reviewed

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
- `PORT_0005`: string normalization, ordering, and top-1 selection portability risk
- `PORT_0006`: identifier quoting, boolean semantics, threshold-boundary semantics, and type semantics risk
- `PORT_0008`: type coercion, identifier case / quoting, and date-time semantics portability risk
- `PORT_0009`: date-time semantics and pagination / limit-offset portability risk
- `PORT_0010`: date-time semantics and boolean semantics portability risk
- `PORT_0011`: null semantics and pagination / limit-offset portability risk
- `PORT_0012`: date-time semantics and boolean semantics portability risk
- `PORT_0013`: boolean semantics and type coercion portability risk
- `PORT_0014`: boolean semantics portability risk
- `PORT_0015`: aggregate edge case portability risk
- `PORT_0016`: date-time semantics portability risk
- `PORT_0017`: type coercion, identifier case / quoting, and threshold-boundary portability risk
- `PORT_0018`: pagination / limit-offset portability risk
- `PORT_0019`: aggregate edge case and pagination / limit-offset portability risk
- `PORT_0020`: aggregate edge case and pagination / limit-offset portability risk
- `PORT_0021`: aggregate edge case and pagination / limit-offset portability risk
- `PORT_0022`: date-time semantics and type coercion portability risk
- `PORT_0023`: aggregate edge case and type coercion portability risk
- `PORT_0024`: boolean semantics portability risk
- `PORT_0025`: date-time semantics and pagination / limit-offset portability risk

These risks are consistent with keeping all covered cases staged while using the tracked draft evidence to prepare a later formal review.

---

## 8. Recommendation

Current recommendation:

- keep `PORT_0003` as `staged_not_yet_admitted`
- keep `PORT_0004` as `staged_not_yet_admitted`
- keep `PORT_0005` as `staged_not_yet_admitted`
- keep `PORT_0006` as `staged_not_yet_admitted`
- keep `PORT_0008` as `staged_not_yet_admitted`
- keep `PORT_0009` as `staged_not_yet_admitted`
- keep `PORT_0010` as `staged_not_yet_admitted`
- keep `PORT_0011` as `staged_not_yet_admitted`
- keep `PORT_0012` as `staged_not_yet_admitted`
- keep `PORT_0013` as `staged_not_yet_admitted`
- keep `PORT_0014` as `staged_not_yet_admitted`
- keep `PORT_0015` as `staged_not_yet_admitted`
- keep `PORT_0016` as `staged_not_yet_admitted`
- keep `PORT_0017` as `staged_not_yet_admitted`
- keep `PORT_0018` as `staged_not_yet_admitted`
- keep `PORT_0019` as `staged_not_yet_admitted`
- keep `PORT_0020` as `staged_not_yet_admitted`
- keep `PORT_0021` as `staged_not_yet_admitted`
- keep `PORT_0022` as `staged_not_yet_admitted`
- keep `PORT_0023` as `staged_not_yet_admitted`
- keep `PORT_0024` as `staged_not_yet_admitted`
- keep `PORT_0025` as `staged_not_yet_admitted`
- use this packet as the basis for a later formal portability review
- do not promote or admit any covered case yet

The current evidence is strong enough for structured review-prep, but not yet for admission, common-core promotion, or formal review closure.
