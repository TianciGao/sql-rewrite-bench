# PORT_0002 准入评审 v0

## 1. 文档作用

本文件记录了对 `PORT_0002` 的第一次明确准入评审。

其目的，是回答一个比更广义的 external-draft 状态总结更窄的问题：

> 基于当前证据，`PORT_0002` 是否应继续保持为 `common-core_candidate`，还是现在就应被正式接纳为一个 external common-core case？

本文件**不替代**以下文档：

- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- `benchmark_spec/COMMON_CORE_ADMISSION_CHECK_v0.md`
- case 本地的 manifest 和 taxonomy 文件

相反，它作为该 portability case 的项目级评审记录而存在。

---

## 2. 被评审的 Case

**Case ID**: `PORT_0002`  
**Primary pool**: portability  
**当前 dataset-line 状态**: `common-core_candidate`

**来源溯源信息（source provenance）**

- Source family: PARROT
- Source subset: BIRD
- Source entry: `benchmark/BIRD/pg_res.json[0]`

**当前 case 结构**

- PostgreSQL 风格的 source query
- MySQL 风格的正例 rewrite
- MySQL 风格的负例 rewrite
- 基于 `votes` 的 witness dataset

---

## 3. 当前证据摘要

`PORT_0002` 当前具备以下证据：

### 3.1 Provenance
source 记录、provenance note 以及冻结后的 case 文件均已具备。

### 3.2 Source 证据
PostgreSQL 的 source query 已在 witness dataset 上成功执行。

观测到的 source 结果：

- PostgreSQL `source.sql` → `1.5`

### 3.3 正例 rewrite 证据
MySQL 的正例 rewrite 已在 witness dataset 上成功执行。

观测到的正例结果：

- MySQL `rewrite_pos_01.sql` → `1.5`

该结果保持了 source 的结果。

### 3.4 负例 rewrite 证据
MySQL 的负例 rewrite 也已成功执行。

观测到的负例结果：

- MySQL `rewrite_neg_01.sql` → `1`

该结果与 source 的结果发生了分歧。

### 3.5 Plan 证据
目前已经收集到以下 plan artifacts：

- PostgreSQL source
- MySQL positive rewrite
- MySQL negative rewrite

### 3.6 当前 portability 价值
该 case 已经展示出一个清晰的 portability 故事：

- source 中使用 PostgreSQL 风格的年份提取表达式
- 正例 rewrite 中使用 MySQL 风格的年份提取表达式
- 一个看起来合理、但会改变结果的负例区间边界 rewrite

这已经构成了较强的 portability 证据。

---

## 4. 评审问题

`PORT_0002` 现在是否应被正式接纳为一个 external common-core case？

---

## 5. 评审结论

### Promotion review
**PASS**

`PORT_0002` 足够强，应继续作为一个明确的 `common-core_candidate` 进入评审。

### Admission review
**NOT YET**

`PORT_0002` **暂时还不应**被正式接纳为一个 external common-core case。

---

## 6. 判定理由

`PORT_0002` 已经是一个很强的 portability draft case，但当前证据的广度仍然窄于当初接纳 `PERF_0002` 时所使用的证据。

目前暂不接纳它的主要原因如下：

1. **跨引擎闭环仍不完整**
   - PostgreSQL source 已验证
   - MySQL 的正例和负例已验证
   - Spark 还没有进入该 case 的闭环证据链

2. **当前验证仍然是不对称的**
   - source-side 证据在 PostgreSQL 上最强
   - rewrite-side 证据在 MySQL 上最强
   - 这对 portability 来说是有意义的，但仍弱于一个更完整、已接纳的 common-core case

3. **即使不接纳，该 case 也已经有用**
   - 它已经能够很好地作为一个 `common-core_candidate` 发挥作用
   - 它要为 benchmark 提供价值，并不要求立刻被正式接纳

换句话说：

> `PORT_0002` 已经足够强，可以通过 promotion review；但还不够强，无法通过最终 admission。

---

## 7. 当前决定

当前决定如下：

- 保持 `PORT_0002` 为 **`common-core_candidate`**
- **暂不**正式接纳
- 在获得更广泛的验证证据后，再重新审视其准入问题

---

## 8. 实施后果

本次评审意味着：

- `cases/PORT/PORT_0002/manifest.yaml` 应继续使用 `dataset_line_candidate: common-core_candidate`
- `cases/PORT/PORT_0002/taxonomy_trial_v0.2.yaml` 应继续与 candidate 状态保持一致
- 暂时不应添加 admitted-common-core 标记
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md` 仍应将 `PORT_0002` 描述为在 `PERF_0002` 之后最强的剩余 candidate

---

## 9. 建议的下一步

对 `PORT_0002` 来说，下一步最有价值的动作**不是**立即接纳。

下一步应当优先做以下事情之一：

1. 扩展验证证据
2. 完善 source / rewrite 对称性的闭环叙事
3. 在收集到额外证据后重新进行准入评审

在此之前，`PORT_0002` 应继续保持为最强的 portability candidate，而不是一个已接纳的 case。

---

## 10. 最终结论

`PORT_0002` 已经跨过了以下门槛：

> **严肃的 common-core candidate 评审**

但它**尚未**跨过以下门槛：

> **已正式接纳的 external common-core case**

因此，当前正确的状态应当是：

> **继续保持为 `common-core_candidate`**