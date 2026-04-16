# Common-Core 与 Extended 规则 v0

## 1. 本文档的作用

本文件定义了基准如何将 case 划分为：

- `common-core`
- `extended`

其目的，是避免不公平比较，同时在不把所有内容都混进同一个排行榜的前提下，保留更广泛的覆盖范围。

关于 pool 的规则，参见 `docs/POOL_MAPPING_RULES.md`。  
关于当前 benchmark 的边界，参见 `benchmark_spec/benchmark_spec_v0.md`。

---

## 2. 为什么需要这种划分

一个 SQL 重写 benchmark 通常同时服务于两个目标，而这两个目标往往存在张力：

1. 跨引擎的公平比较  
2. 广泛的真实世界覆盖

如果 benchmark 只保留最小的共享子集，它就会过于保守。  
如果 benchmark 把所有 case 混在一起比较，结果就会变得嘈杂且不公平。

`common-core` / `extended` 这一区分，正是为了同时保留这两点：

- `common-core` = 可比较的核心集合
- `extended` = 更丰富、但可比较性不那么统一的覆盖集合

---

## 3. 定义

## 3.1 Common-Core
一个 case 只有在满足以下全部条件时，才属于 **common-core**：

1. 对于相关任务下当前预期纳入范围的所有引擎，它都可以执行  
2. 可以在这些引擎之间进行结果比较  
3. 该 case 的语义足够稳定，能够直接用于跨引擎报告  
4. 该 case 的核心含义不依赖于不受支持或高度引擎特定的构造

当前预期纳入的引擎为：

- Spark SQL
- PostgreSQL
- MySQL

`common-core` 是用于公平横向比较的主要集合。

---

## 3.2 Extended
一个 case 如果与 benchmark 相关，但不满足完整的 common-core 要求，则属于 **extended**。

典型原因包括：

- 只有当前引擎中的一部分能够执行它  
- 某种方言特定构造具有保留价值  
- 它对于覆盖面非常有价值，但并不完全适合做跨引擎公平比较  
- 它仍然是有用的 benchmark case，但不应混入 `common-core` 的记分板

`extended` 不是一个“丢弃桶”。  
它是一个受控的扩展集合。

---

## 4. 判定规则

## 4.1 Common-Core 准入规则
一个 case 只有在满足以下条件时，才能被标记为 `common-core`：

- 当前纳入范围的所有目标引擎都可以执行它  
- 可以在这些引擎之间检查结果一致性  
- 这种比较被认为足够公平，可用于主要报告  
- 该 case 的含义不会被重大的引擎特定语义所主导

## 4.2 Extended 准入规则
一个 case 在满足以下条件时，可以被标记为 `extended`：

- 它至少与一个正式 pool 相关  
- 它能为 benchmark 增加有意义的价值  
- 它保留了 provenance 和 case 元数据  
- 它未满足一项或多项 common-core 要求，但仍然有用

---

## 5. 与 formal pools 的关系

`common-core` / `extended` **并不**替代 primary pool。

每个被接纳的 case 仍然应该具有：

- 一个 `candidate_primary_pool` 或最终的 `primary_pool`
- 一条 dataset line：
  - `common-core`
  - 或 `extended`

例如：

- 一个 case 可以是 `primary_pool = longtail` 且 `dataset_line = common-core`
- 另一个 case 可以是 `primary_pool = portability` 且 `dataset_line = extended`

Pool 回答的是：**这个 case 服务于哪一类 benchmark 问题**  
Dataset line 回答的是：**这个 case 应该如何被报告和比较**

---

## 6. 当前 v0 规则

在当前的早期 pilot 阶段：

- 只有当三引擎执行和结果比较已经被证明成立时，case 才应默认归入 `common-core`
- 仍然缺少执行或比较证据的 case，不应被默认视为 `common-core`
- 存在未解决的引擎特定语义问题的 case，应继续保留在 `extended` 或 `not_yet_admitted`

---

## 7. 当前 not-yet-admitted 规则

如果一个 case 仍存在以下任一未解决问题，则应暂时不归入 `common-core` 或 `extended`：

- provenance 不完整  
- primary pool 尚不明确  
- result checker 不完整  
- 尚未证明三引擎（或目标引擎）可执行  
- 语义仍在审查中

此类 case 应标记为：

- `staging`
- 或 `not_yet_admitted`

---

## 8. 报告规则

对于当前版本的 benchmark：

1. 应首先报告 `common-core` 的结果  
2. `extended` 的结果应单独报告  
3. 不应将 `common-core` 和 `extended` 合并成一个不加区分的总分  
4. 如果某个指标只在 `extended` 上报告，必须明确说明

---

## 9. 升级 / 降级规则

一个 case 可以在所需证据具备之后被升级：

- 从 `not_yet_admitted` → `extended`
- 从 `extended` → `common-core`

一个 case 也可以被降级：

- 从 `common-core` → `extended`

如果后续证据表明，跨引擎比较实际上并不公平或不稳定，就应进行降级。

此类变更应记录在项目备注中；如果涉及策略变更，还应记录在 `benchmark_spec/decision_log.md` 中。

---

## 10. 当前实践指引

在当前仓库阶段，建议按如下顺序进行判定：

1. 先判断这个 case 是否应被接纳  
2. 分配 candidate / primary pool  
3. 再决定它属于 `common-core` 还是 `extended`  
4. 只有在此之后，才把它纳入总结或 benchmark 表格

这一顺序可以避免把 source 层面的假设与最终 case 层面的报告混淆起来。