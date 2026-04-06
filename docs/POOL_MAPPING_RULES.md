# Pool Mapping Rules
## SQL Rewrite Benchmark 正式池子归类规则（v0.1）

## 1. 文档角色

本文件用于定义 **case package** 如何进入正式 benchmark 池子，以及 source inventory 与正式 pool 之间的关系。

本文件的目标不是描述完整 benchmark 研究计划，而是把以下问题写成稳定、可执行、可审阅的规则：

1. 当前正式池子有哪些
2. pool 是给什么对象用的
3. case 进入某个 pool 需要满足什么条件
4. 哪些来源可以作为某个 pool 的主要种子
5. 哪些情况必须留在 staging / not yet admitted 状态
6. 当一个 case 同时满足多个池子特征时，如何决定 primary pool

本文件与以下文件的关系如下：

- `docs/PROJECT_PLAN.md`：项目总计划与 phase 路线
- `benchmark_spec/benchmark_spec_v0.md`：当前版本执行边界
- `benchmark_spec/decision_log.md`：冻结决策
- `inventory/source_registry.csv`：source 登记表
- `docs/INVENTORY_TEMPLATE.md`：source inventory 填写规范

---

## 2. 当前版本适用范围

本文件适用于：

- v1 bootstrap / early pilot
- Spark SQL / PostgreSQL / MySQL
- case package 级别的正式归类
- source 到 pool 的预映射说明
- 后续 pool validator / admission checker 的实现依据

本文件当前 **不** 适用于：

- UDF / stored procedure / trigger benchmarking
- compositional OOD split
- engine / dialect hold-out split
- 新引擎家族扩张
- 完整大规模 workload curation

---

## 3. 核心原则

### 3.1 正式池子只有四个
当前版本正式池子固定为：

- performance
- longtail
- consistency
- portability

### 3.2 pool 面向 case package，而不是 source
source inventory 记录的是来源；  
正式 pool 归类发生在 **case package** 层。

一行 source 不是一个 pool 成员；  
一个 case package 才是最终进入 benchmark pool 的单位。

### 3.3 每个 case 最多只有一个 primary pool
一个 case 可以拥有很多标签，但正式统计时只允许一个 `primary_pool`。  
其他相关维度使用 tags、notes 或 secondary attributes 表达。

### 3.4 `Manual Seed Cases` 不是第五个 pool
`Manual Seed Cases` 是 `manual_seed` 来源家族或人工补洞通道。  
它后续形成的 case package 仍然必须进入四个正式池子之一，或保持 `not_yet_admitted` 状态。

### 3.5 `plan observability` 与 `workload realism` 是横切维度
它们不是独立 pool。  
它们通过：
- taxonomy tags
- metadata
- annotation status
- coverage fields
来体现。

### 3.6 允许 staging / not yet admitted 状态
如果一个 case 目前：
- provenance 未完全确认
- 三引擎可执行性未确认
- result checker 未完成
- primary pool 不明确

则它应保持在 `staging` / `not_yet_admitted` 状态，而不是被强行塞入某个正式池子。

---

## 4. 术语

### 4.1 Source
source 指来源家族，例如：
- TPC-H
- SQLStorm
- Calcite Seeds
- PARROT
- Manual Seed Cases

### 4.2 Case package
case package 是 benchmark 的最小单位，至少应包含：
- source SQL
- positive rewrites / negatives（视任务而定）
- provenance
- feature tags
- result checker
- source / rewritten plans
- engine / dialect metadata

### 4.3 Primary pool
primary pool 指一个 case 在正式 benchmark 中的主归类，用于：
- 汇总统计
- leaderboard / 分组实验
- benchmark characterization

### 4.4 Secondary attributes
secondary attributes 指不改变 primary pool，但可以补充说明 case 侧重点的字段，例如：
- realism-heavy
- plan-rich
- cross-engine partial
- hard-negative-present

---

## 5. Source 与 Pool 的关系

## 5.1 Source 只能做预映射
`inventory/source_registry.csv` 中记录的 `primary_pool` 是 source 级别的**预期主要去向**，不是最终 case 归类。

例如：
- TPC-H → performance（预期主去向）
- SQLStorm → longtail（预期主去向）
- PARROT → portability（预期主去向）
- Manual Seed Cases → none_yet（等待 case 形成后再决定）

## 5.2 Case 才做正式落池
当且仅当一个 case 满足本文件中的 admission rules，并完成基本验证后，才可被赋予正式 `primary_pool`。

---

## 6. 所有正式 pool 共享的总 admission gate

一个 case 要进入任一正式池子，至少满足以下条件：

### 6.1 provenance 完整
至少能回答：
- 该 case 来自哪个 source
- 是原始来源、派生来源还是人工构造
- 生成/整理责任归属是谁

### 6.2 语句可解析
在声明的 source dialect 下，source SQL 可稳定解析。  
若该 case 声称支持 target dialect / engine，则目标侧也必须能稳定解析。

### 6.3 结果校验能力存在
至少具备以下之一：
- result checker
- witness data
- differential execution 路径
- 明确的正/负例判别机制

### 6.4 计划可采集
至少 source SQL 的计划可采集。  
若 case 依赖 rewrite 比较，则 source / rewritten plans 都应可采集。

### 6.5 标签最小集完整
至少具备：
- source_id
- source provenance
- feature tags
- task role
- candidate primary pool
- engine / dialect metadata

### 6.6 不与现有 case 高度重复
重复度高、结构近乎等价、贡献极低的 case，应优先拒绝或保留在 staging。

---

## 7. 四个正式池子的定义与规则

# 7.1 performance pool

## 7.1.1 目标
performance pool 用于回答：

> 在稳定、经典、可复现的基线上，rewrite 是否带来可重复的性能收益？

## 7.1.2 典型来源
- TPC-H
- TPC-DS
- DSB
- JOB
- 其他稳定 analytical benchmark 子集

## 7.1.3 纳入条件
一个 case 可进入 performance pool，当它满足以下大部分条件：

1. 来源于稳定 benchmark / workload
2. 查询语义清晰、输出稳定
3. 至少在一个当前引擎上可重复执行
4. source 与 rewrite 的收益可比较
5. 计划采集可用
6. 存在明确 rewrite opportunity
7. 不只是 trivial query

## 7.1.4 更理想的纳入条件
- 可在多个当前引擎上复验
- before / after plan 差异可解释
- 可作为后续 baseline 对比用的 common-core case

## 7.1.5 不纳入条件
- 只有 correctness 价值，没有性能价值
- 过于 trivial，没有可比 rewrite 空间
- 强依赖单引擎私有行为，无法作为稳定基线
- 结果或性能波动过大，难以复验
- 无法稳定采集计划

---

# 7.2 longtail pool

## 7.2.1 目标
longtail pool 用于回答：

> 现有 rewrite 方法是不是只会做模板题，还是能覆盖复杂结构和长尾 SQL？

## 7.2.2 典型来源
- SQLStorm
- Stack Queries
- 手工构造的复杂 SQL seeds
- 其他明显补 coverage hole 的来源

## 7.2.3 纳入条件
一个 case 可进入 longtail pool，当它满足以下大部分条件：

1. 明显补充 SQL feature coverage
2. 在结构上区别于经典模板基准
3. 具有复杂表达面，例如：
   - window
   - outer join
   - non-equi join
   - deep nesting
   - complex predicate combination
4. 具有长尾特征而不是仅仅“变长”
5. 至少在一个当前引擎上可执行并可采计划

## 7.2.4 更理想的纳入条件
- 与 performance pool 的 coverage profile 明显不同
- 可在 common-core 范围内跨多个引擎复验
- 能在 benchmark characterization 中体现“为什么它是 long-tail”

## 7.2.5 不纳入条件
- 仅文本很长，但没有实质 coverage 增益
- 无法做结果一致性检查
- 过度依赖超出当前三引擎范围的私有特性
- 与现有 longtail cases 高度重复

---

# 7.3 consistency pool

## 7.3.1 目标
consistency pool 用于回答：

> rewrite 有没有改错，以及系统能不能识别或拒绝错误 rewrite？

## 7.3.2 典型来源
- Calcite Seeds
- SQLEquiQuest / VeriEQL
- 手工构造的 positive / negative pairs
- 规则测试中的可判别重写对

## 7.3.3 纳入条件
一个 case 可进入 consistency pool，当它满足以下大部分条件：

1. 具备正例 / 负例，或可稳定构造正例 / 负例
2. 具有 witness data 或明确的 result checker
3. 可明确判断 source 与 variant 的语义关系
4. 不依赖“肉眼感觉正确”
5. 结果差异可重复暴露
6. 至少能采 source plan，并尽可能采 rewrite plan

## 7.3.4 更理想的纳入条件
- 同时具备 positive rewrite 与 hard negative
- negative 差异可通过多实例 differential testing 暴露
- 与 performance case 不同，它的主目标是 correctness，而不是 speedup

## 7.3.5 不纳入条件
- 只有 source query，没有 pairs / variants
- 无法构造 witness data，也没有可靠 checker
- 只有“可能错”，没有可复现区分方式
- 完全只适合性能研究

---

# 7.4 portability pool

## 7.4.1 目标
portability pool 用于回答：

> rewrite 或 translation 到另一种方言 / 引擎时，是否仍然可执行、结果一致、收益可迁移？

## 7.4.2 典型来源
- PARROT
- 人工整理的 Spark / PostgreSQL / MySQL triplets
- 从其他 source 中提炼出的 portability seeds

## 7.4.3 纳入条件
一个 case 可进入 portability pool，当它满足以下大部分条件：

1. 有明确的 source dialect / target dialect 关系
2. 至少覆盖当前三引擎中的一个真实迁移关系
3. 目标侧可解析并可执行
4. 结果一致性可验证
5. 方言差异标签明确
6. 尽量能比较收益是否迁移

## 7.4.4 更理想的纳入条件
- source 与 target 两侧都能采计划
- 不仅能运行，还能说明 portability gain / loss
- 能记录因函数、类型、NULL、时间语义差异造成的行为差异

## 7.4.5 不纳入条件
- 只有语法变形，没有明确语义对等关系
- 目标方言根本不支持，无法验证
- 只能 parser-level 转换，不能执行
- 与当前三引擎范围完全无关

---

## 8. Primary pool 决策规则

当一个 case 同时看起来符合多个池子时，按下面顺序判断：

### 8.1 先看“主问题”是什么
优先问：

- 这个 case 最主要想验证什么？
  - 性能收益
  - 长尾覆盖
  - 一致性判别
  - 跨方言迁移

这个答案决定 primary pool。

### 8.2 再看 secondary attributes
如果一个 case 同时具备别的特征，不改变 primary pool，只在 metadata 中记录 secondary attributes。

例如：
- 一个 portability case 很复杂，不应自动改成 longtail
- 一个 performance case 也有负例，不应自动改成 consistency

### 8.3 不允许多主池
正式 admitted case 只允许一个 `primary_pool`。

### 8.4 允许暂不落池
若 primary pool 无法清晰判定，则进入：
- `staging`
- 或 `not_yet_admitted`

待人工复审后再分配。

---

## 9. Source 到 Pool 的预映射规则

以下规则仅用于 source inventory 的 `primary_pool` 参考，不是最终 case 归类：

- TPC-H → performance
- TPC-DS → performance
- DSB → performance
- JOB → performance
- SQLStorm → longtail
- Stack Queries → longtail
- Calcite Seeds → consistency
- SQLEquiQuest / VeriEQL → consistency
- PARROT → portability
- Manual Seed Cases → none_yet

---

## 10. staging / not yet admitted 规则

以下情况应进入 staging / not yet admitted，而不是正式 pool：

1. provenance 不完整
2. result checker 尚未完成
3. 三引擎适配情况不明确
4. plan 无法采集
5. primary pool 无法判断
6. 与现有 case 的重复度尚未确认
7. 需要进一步人工决策

---

## 11. 常见错误（Do / Don’t）

### Do
- 先判断 case 的主问题，再决定 primary pool
- 用 tags 和 notes 表达附加属性
- 保留 source provenance
- 允许 case 暂时留在 staging
- 保持四个正式池子稳定不膨胀

### Don’t
- 不要把 source 直接视为正式 pool 成员
- 不要把 Manual Seed Cases 当成第五个池子
- 不要把 plan observability 单独做成 pool
- 不要让同一 admitted case 同时属于多个 primary pools
- 不要为了凑数量，把定义不清的 case 硬塞进某个池子

---

## 12. 当前版本说明

本文件为 v0.1。  
其目标是为当前 v1 bootstrap / early pilot 提供稳定、低歧义、可供人工与脚本共同使用的正式 pool 归类规则。

如以下内容发生改变，必须同步更新 `benchmark_spec/decision_log.md`：

- 正式 pool 数量
- primary pool 决策顺序
- staging / not yet admitted 规则
- source 到 pool 的预映射口径
- 某个 pool 的纳入或不纳入条件