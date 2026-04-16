# PORT_0002 准入评审 v1

## 1. 文档作用

本文件记录了对 `PORT_0002` 的第二次明确准入评审。

其目的，是回答更新后的评审问题：

> 基于当前证据，`PORT_0002` 是否应继续保持为 `common-core_candidate`，还是已经足够强，可以被正式接纳为一个 external common-core case？

本文件取代了以下文档中的旧评审语境：

- `benchmark_spec/PORT_0002_ADMISSION_REVIEW_v0.md`

但这并不抹去此前评审的历史价值。

---

## 2. 被评审的 Case

**Case ID**: `PORT_0002`  
**Primary pool**: portability  
**先前的 dataset-line 状态**: `common-core_candidate`

**来源溯源信息（source provenance）**

- Source family: PARROT
- Source subset: BIRD
- Source entry: `benchmark/BIRD/pg_res.json[0]`

**当前 case 结构**

- PostgreSQL 风格的 source query
- MySQL 风格的正例 rewrite
- MySQL 风格的负例 rewrite
- Spark 风格的正例 rewrite
- Spark 风格的负例 rewrite
- 基于 `votes` 的 witness dataset

---

## 3. 证据摘要

`PORT_0002` 目前具备以下证据：

### 3.1 Provenance
source 记录、provenance note 以及冻结后的 case 文件均已具备。

### 3.2 Source 证据
PostgreSQL 的 source query 可以成功执行。

观测结果：

- PostgreSQL `source.sql` → `1.5`

### 3.3 MySQL rewrite 证据
MySQL 目标侧 rewrites 可以成功执行。

观测结果：

- MySQL `rewrite_pos_01.sql` → `1.5`
- MySQL `rewrite_neg_01.sql` → `1`

### 3.4 Spark rewrite 证据
Spark 目标侧 rewrites 也可以成功执行。

观测结果：

- Spark `rewrite_pos_02_spark.sql` → `1.5`
- Spark `rewrite_neg_02_spark.sql` → `1.0`

### 3.5 保持 / 分歧行为
该 case 现在已经证明：

- source == positive
- source != negative

这一性质对 MySQL 和 Spark 的目标侧 rewrite 都成立。

### 3.6 Plan 证据
目前已经具备以下 plan artifacts：

- PostgreSQL source
- MySQL positive rewrite
- MySQL negative rewrite
- Spark positive rewrite
- Spark negative rewrite

---

## 4. 评审问题

`PORT_0002` 现在是否应被正式接纳为一个 external common-core case？

---

## 5. 评审结论

### Promotion review
**PASS**

`PORT_0002` 显然仍然足够强，能够进入 `common-core` 评审。

### Admission review
**PASS**

`PORT_0002` 现在已经足够强，可以被正式接纳为一个 external common-core case。

---

## 6. 判定理由

在 `v0` 中，之所以暂缓接纳，是因为其 portability 闭环仍然过窄：

- source-side 证据主要只在 PostgreSQL 上
- rewrite-side 证据主要只在 MySQL 上
- Spark 证据缺失

而现在，这一缺口已经被大幅缩小。

该 case 现在已经展示出一个可复用的 portability 模式：

1. 一个 source-side 的 PostgreSQL 表达
2. 一个保持语义的 target-side MySQL 正例 rewrite
3. 一个改变语义的 target-side MySQL 负例 rewrite
4. 一个保持语义的 target-side Spark 正例 rewrite
5. 一个改变语义的 target-side Spark 负例 rewrite

这已经足以将 `PORT_0002` 视为不只是一个 portability candidate，而是一个已被接纳的 external benchmark unit。

---

## 7. 当前决定

当前决定如下：

> 将 `PORT_0002` 接纳为一个 external common-core case。

---

## 8. 实施后果

本次评审意味着：

- `cases/PORT/PORT_0002/manifest.yaml` 应从 `common-core_candidate` 改为 `common-core`
- `cases/PORT/PORT_0002/taxonomy_trial_v0.2.yaml` 应体现其已被接纳的 common-core 状态
- case 本地元数据应将本次结果记录为一次明确的 admission outcome
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md` 不应再将 `PORT_0002` 仅描述为 candidate

---

## 9. 最终结论

`PORT_0002` 现在已经跨过了这条门槛：

> 从：强的 portability candidate

到：

> 已正式接纳的 external common-core portability case