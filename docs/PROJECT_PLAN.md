# PROJECT_PLAN.md
## 面向 SQL Rewriting 的一致性感知、计划可观测、跨引擎 Benchmark 项目计划

---

## 1. 文档角色

本文档是本项目的**正式总计划**，用于定义项目的长期研究主线、范围边界、benchmark 设计框架、数据构建策略、评测维度与阶段性里程碑。

本文档不承担以下职责：

- 不记录日常执行进度
- 不记录当前 case 的实时状态变化
- 不记录某周完成了哪些具体操作
- 不替代 decision log
- 不替代当前版本的 executable spec
- 不承载单 case 的完成门槛、admission 细则或实时治理状态

因此：

- `docs/PROJECT_PLAN.md` 负责回答：**为什么做、整体怎么做、最终想做成什么**
- `docs/EXECUTION_STATUS.md` 负责回答：**现在做到哪里、当前 focus 是什么、下一步做什么**
- `benchmark_spec/decision_log.md` 负责回答：**哪些决策已经冻结**
- `benchmark_spec/*rules*.md` 负责回答：**什么算 archetype-complete、什么能 admission、什么进入 common-core / extended**
- `benchmark_spec/reviews/*.md` 负责回答：**某一批 case 在某次 promotion / admission 审查中是如何被判断的**
- `inventory/source_registry.csv` 负责回答：**source 级真实纳入状态是什么**
- `inventory/case_registry.csv` 负责回答：**case 级实时事实是什么**
- `docs/DOC_MAP.md` 负责回答：**各文件应该写什么、更新顺序是什么、哪些文件应归档**

其中：

- case 级实时状态以 `inventory/case_registry.csv` 为准
- source 级真实纳入状态以 `inventory/source_registry.csv` 为准
- review-history 以 `benchmark_spec/reviews/*.md` 为准
- `docs/EXECUTION_STATUS.md` 只保留代表性快照与当前解释，不承担完整 source-of-truth

---

## 2. 项目背景与核心判断

现有 SQL rewrite benchmark 在数据库优化和自动改写评测中具有重要作用，但公开生态仍存在几个系统性问题：

1. 许多 benchmark 以**最终性能**为核心，往往将 rewrite 的**语义一致性**默认化处理，而不是把它作为一等评测对象。
2. 许多 benchmark 只报告**端到端 latency**，缺少**计划级可观测性**，因此难以解释 rewrite 为什么变快、为什么失效、收益来自哪里。
3. 许多 benchmark 仍然偏向**单引擎、单方言、单场景**评测，难以刻画 rewrite 方法在跨系统环境中的可执行性、一致性与收益迁移能力。
4. 许多 benchmark 仍依赖**少量固定模板**或较窄的 SQL 表达面，难以充分暴露 rewrite 方法在长尾 SQL、复杂结构和真实 workload 风格上的失效模式。

基于上述问题，本项目拟构建一个新的 SQL rewrite benchmark，使以下三个维度成为一等公民：

- 一致性
- 计划级可观测性
- 跨方言 / 跨引擎泛化

---

## 3. 论文主张

本项目建立在以下三条主张之上：

### 主张一：一致性不应再被视为默认前提
现有 SQL rewrite benchmark 多以最终性能为核心，往往将 rewrite 的语义一致性视为默认前提，而不是正式的一等评测对象；同时它们常依赖少量固定模板，难以系统暴露 rewrite 方法在长尾 SQL、复杂结构和真实 workload 风格下的失效模式。

### 主张二：计划级可观测性应成为 benchmark 的正式维度
现有 benchmark 通常只报告端到端 latency，缺少计划级可观测性，因而难以把 SQL 改动映射到逻辑/物理计划节点变化，也难以解释性能收益或回归的来源。

### 主张三：泛化性不能只在单引擎 / 单方言中讨论
现有评测大多局限于单引擎、单方言，因此无法充分检验 rewrite 方法在不同系统中的可执行性、一致性和收益迁移能力。

### Supporting Evidence（非 claim 本体）
在真实 workload 场景中，rewrite correctness 并不能被安全地默认化处理；因此一致性校验必须进入 benchmark 核心定义，而不能仅作为附属实验或附录分析。

---

## 4. v1 范围与非目标

### 4.1 v1 范围

v1 的范围固定为：

- 引擎 / 方言：Spark SQL、PostgreSQL、MySQL
- 任务对象：声明式 SQL rewrite benchmark
- benchmark 最小单元：case package
- 目标阶段：pilot-scale benchmark construction and evaluation

### 4.2 v1 明确不纳入

以下内容不纳入 v1：

- compositional OOD split
- engine / dialect hold-out split
- UDF / stored procedure / trigger benchmarking
- procedural SQL pipelines
- 新增其他数据库引擎家族
- 大规模无约束 workload 扩张
- 依赖本地大模型作为项目启动前提

### 4.3 v1 的工作原则

- 先覆盖、后规模
- 先一致性、后速度
- 先闭环、后扩张
- 先 pilot 稳定、后大规模扩展
- 先机器可读 artifact，后外部发布包装

---

## 5. Benchmark 任务结构

本项目的 benchmark 不设计为单一 leaderboard，而设计为三个任务轨道。

### Track A：同引擎 rewrite
给定原 SQL，在同一引擎内产生语义一致且更优的 rewrite。

核心问题：

- rewrite 是否仍然正确
- rewrite 是否更快
- 收益是否稳定

主要输出：

- source SQL
- positive rewrites
- hard negatives
- 执行结果
- 收益数据

### Track B：计划可观测 rewrite
评测 SQL 改动能否映射到逻辑/物理计划变化，并解释收益来源。

核心问题：

- SQL 改动影响了哪类逻辑计划结构
- 哪些物理节点变化对应了收益或回归
- 节点级归因是否可信

主要输出：

- 计划节点对齐
- logical / physical delta
- 节点级指标
- 收益归因记录

### Track C：跨方言 / 跨引擎 rewrite
给定源方言 SQL，输出在目标引擎上仍可执行、结果一致，并尽可能保留收益的 rewrite。

核心问题：

- 方言变体是否可执行
- 结果是否一致
- 收益是否能迁移

主要输出：

- 方言变体
- 跨引擎执行记录
- 一致性结果
- 收益迁移结果

---

## 6. Benchmark 设计原则

### 6.1 一致性优先于速度
任何 rewrite 如果无法通过结果一致性校验，即使性能提升明显，也不能被视为有效正例。

### 6.2 case package 优先于单条 SQL
benchmark 的最小单元不是 query string，而是具有完整上下文的 case package。

### 6.3 覆盖先行，规模其次
先定义 coverage taxonomy，再扩大样本规模，避免用 query 数量掩盖 coverage 空洞。

### 6.4 多引擎统一协议
Spark SQL、PostgreSQL、MySQL 的解析、执行、结果校验、计划采集与日志归档必须采用一致口径。

### 6.5 LLM 受约束使用
LLM 只能作为 benchmark 构造流程中的受限工具，而不是 benchmark 设计规则的制定者。

### 6.6 artifact 可复验
所有关键运行都必须生成 machine-readable artifact，以支撑复验、回归与论文写作。

---

## 7. Taxonomy 框架（4+1）

本项目采用 **5 张机器可读 taxonomy 表**。  
其中：

- **4 张构成 coverage taxonomy**
- **1 张构成 rewrite-opportunity 横切层**

taxonomy 是 benchmark 的第一性约束。  
任何样本收集、case 构造、promotion 或 admission 决策，都必须回到 taxonomy 回答：

- 它覆盖了什么
- 它补了哪块空洞
- 它是否与现有样本高度重复

### 7.1 Coverage Taxonomy 之一：SQL 特性层
回答：SQL 本身长什么样。

代表性特征包括：

- CTE
- correlated subquery
- outer join
- non-equi join
- window
- set operations
- deep nesting
- grouping sets
- date function variation
- string function variation
- large LIMIT
- expression complexity

### 7.2 Coverage Taxonomy 之二：逻辑/计划层
回答：计划里发生了什么。

代表性节点或变化包括：

- scan
- filter
- project
- join
- aggregate
- sort
- limit
- window
- subquery decorrelation
- materialization
- exchange

### 7.3 Coverage Taxonomy 之三：workload realism 层
回答：这个 SQL/工作负载像不像真实场景。

代表性维度包括：

- query length
- join count
- nesting depth
- operator ratio
- repetition
- temporal dynamics
- read/write mix
- skew / correlation
- result cardinality
- realistic query style
- long-tail structure

### 7.4 Coverage Taxonomy 之四：portability 层
回答：跨方言 / 跨引擎差异来自哪里。

代表性维度包括：

- dialect-specific functions
- type semantics
- null semantics
- date-time semantics
- string function differences
- limit/fetch differences
- engine-specific syntax constraints

### 7.5 Rewrite-Opportunity 横切层
回答：这个 case 为什么值得进行 rewrite 评测。

代表性维度包括：

- predicate pushdown
- projection pruning
- join reorder
- subquery decorrelation
- aggregation rewrite
- function normalization
- dialect adaptation
- materialization strategy

### 7.6 口径说明
论文叙事层面，不把上述 5 张表写成“5 层 coverage taxonomy”。  
更稳的表述是：

- **4 层 coverage taxonomy**
- **1 个 rewrite-opportunity 横切层**

---

## 8. Case Package 定义

benchmark case 不是单条 SQL，而是一个能够独立复现的 case package。

### 8.1 pilot minimum 要求
pilot 阶段每个 case 至少应包含：

- schema + data profile
- source SQL
- positive rewrites
- hard negatives
- feature tags
- source plan
- rewritten plan
- result checker
- engine / dialect metadata

### 8.2 release-grade 目标
随着 benchmark 走向更正式发布，case package 应进一步包含：

- canonical AST / logical IR
- SQL span → logical operator → physical node 映射
- 更完整的节点级收益归因
- 更系统的 provenance 与 review metadata

### 8.3 基本原则
每个 case package 必须支持：

- 独立执行
- 结果校验
- 计划采集
- 失败复验
- provenance 追踪

---

## 9. 数据来源与四池策略

本项目不采用“简单并表 / 直接拼接 query 集”的构建方式，而采用分层组装策略。

### 9.1 总体原则

池子的**角色**在本文件中冻结。  
池子里的**具体 source roster**不在本文件中写死为最终名单。  
case 的**实时实现状态**也不在本文件中逐条维护。

本文件只定义：

- 每个池子的角色
- 每个池子的优先候选源
- 每个池子的扩展候选源
- 四池策略的长期构建原则

实际纳入哪一批 source，由以下文件维护：

- `inventory/source_registry.csv`
- `coverage map`
- `docs/EXECUTION_STATUS.md`（摘要性快照）

实际哪些 case 已经实现、成熟到什么程度、进入哪条统计线，由以下文件维护：

- `inventory/case_registry.csv`
- `docs/EXECUTION_STATUS.md`（代表性快照）

因此，本节中的 source / pool 描述属于**长期框架口径**，不应与实时状态文件混读。

### 9.2 池 1：性能主池（performance）
作用：

- 提供稳定、经典、可复现的 rewrite performance 基线

优先候选源：

- TPC-H
- TPC-DS

扩展候选源：

- DSB
- JOB

原则：

- 先取稳定 query
- 先跑 source case
- 先确定三引擎 common-core 子集
- 后补 positive rewrite 与 negative

### 9.3 池 2：长尾覆盖池（longtail）
作用：

- 补模板 benchmark 覆盖不到的复杂结构和长尾表达面

优先候选源：

- SQLStorm
- Stack / StackOverflow 查询

扩展候选源：

- 手工复杂 SQL seeds
- 其他经 coverage map 证明具有增量价值的长尾来源

原则：

- 先小样本抽取
- 先 parse / dedupe / tag
- 跨三引擎不稳定的样本可先进入 extended backlog

### 9.4 池 3：一致性池（consistency）
作用：

- 把 correctness 作为 benchmark 的正式任务线

优先候选源：

- Calcite Seeds

候选补充源：

- SQLEquiQuest 或 VeriEQL 的受控子集
- 人工构造的 positive / negative pairs

原则：

- 需要 witness dataset
- 每个 case 尽量同时有正例与负例
- hard negative 必须“看起来合理但语义不对”

### 9.5 池 4：跨方言 / 跨引擎池（portability）
作用：

- 验证 rewrite 在跨方言 / 跨引擎场景中的可执行性、一致性与收益迁移

优先候选源：

- PARROT

扩展候选源：

- 人工补充的 Spark / PostgreSQL / MySQL triplets
- 其他来源中抽取的 portability seeds
- 受限 SQLGlot 辅助生成候选

原则：

- 明确区分 common-core 与 extended
- SQLGlot 可做候选助手，但不能当 ground truth
- 结果一致性优先于“转得出来”

### 9.6 样本治理原则
所有 case 都必须保留：

- provenance
- coverage tags
- task role
- 当前成熟度状态
- promotion / admission 轨迹

---

## 10. `common-core / extended` 两条统计线

本项目采用两条统计线，而不是只维护单一 benchmark 口径：

- `common-core`
- `extended`

它们的作用不是把 benchmark 拆成两个互不相关的集合，而是为了同时满足：

1. **公平横向比较**
2. **更丰富、更真实的覆盖面保留**

### 10.1 `common-core`

`common-core` 只包含那些在当前 v1 范围内，能够在 Spark SQL、PostgreSQL、MySQL 三个目标引擎上形成**相对公平、可复验、可直接横向比较**的 case。

这类 case 通常满足以下特征：

- 三引擎均可执行
- 结果可直接比较
- 计划采集与结果校验链路相对稳定
- 不依赖某一单独引擎的特殊语义前提
- 适合作为 benchmark 主体排行榜与主结果表的核心分母

`common-core` 的主要作用是：

- 保证方法比较的公平性
- 保证主结果表的可解释性
- 保证不同方法之间共享相对一致的评测分母
- 作为 benchmark characterization 和 ranking shift study 的核心比较集合

### 10.2 `extended`

`extended` 包含那些**具有明确研究价值**、但在当前阶段尚不适合纳入统一三引擎公平横向比较的 case。

这类 case 可能包括但不限于：

- 仅部分引擎可稳定执行的 case
- 方言差异较强的 portability case
- 具有较高表达面价值但当前三引擎支持不完全对齐的 long-tail case
- 在 correctness 或 observability 上有价值，但当前统一比较条件尚不充分的 case

`extended` 的主要作用是：

- 保留更丰富、更真实的 coverage
- 避免因为追求统一三引擎比较而过早丢弃有价值样本
- 为后续 benchmark 扩展、失败分析和方法泛化研究提供材料
- 支撑 benchmark characterization，而不强行进入主排行榜

### 10.3 两条线的关系

`common-core` 与 `extended` 不是“正式 benchmark / 非正式 benchmark”的关系，  
而是“**统一可比核心集合**”与“**高价值扩展集合**”的关系。

换句话说：

- `common-core` 负责**公平横向比较**
- `extended` 负责**覆盖面与真实世界复杂性保留**

本项目不要求所有高价值 case 都进入 `common-core`。  
相反，如果某个 case 在覆盖、复杂性或跨系统差异上具有明显研究价值，但暂时不满足统一比较条件，则应优先保留在 `extended`，而不是为了追求统一榜单而将其删除。

### 10.4 报告原则

在正式报告中，应明确区分两条统计线：

- 主排行榜、主结果表、主方法比较，优先基于 `common-core`
- benchmark characterization、覆盖分析、失败分析、扩展观察，可同时报告 `extended`
- 不得将 `common-core` 与 `extended` 在未标注的情况下混合为单一统计口径
- 若某项结果仅在 `extended` 上成立，必须显式标明其适用范围与能力边界

### 10.5 与规则文件的关系

本节只定义 `common-core / extended` 的**概念角色和报告原则**。  
具体划分条件、纳入门槛、升级路径与评测口径，不在本文件中展开，而由独立规则文件维护：

- `benchmark_spec/common_core_extended_rules_v0.md`

因此：

- `PROJECT_PLAN.md` 负责说明为什么需要这两条线
- 规则文件负责说明如何具体判断 case 进入哪一条线

---

## 11. Case 治理与规则文件分工

`PROJECT_PLAN.md` 只定义 case 治理的总体框架，不承载具体门槛细则。

与 case 治理相关的具体规则文件应独立维护，包括但不限于：

- `benchmark_spec/case_archetype_completion_rules_v0.md`
- `benchmark_spec/case_admission_rules_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- 其他与 promotion / review / release 相关的规则文件

### 11.1 本文件负责回答

本文件负责说明：

- 为什么 benchmark 需要显式的 case 治理机制
- staged / candidate / admitted / extended 等状态层级为什么存在
- 为什么 admission、promotion、common-core / extended 分线是 benchmark 可信度的一部分
- 为什么治理规则必须与长期项目计划分层维护

### 11.2 规则文件与 review-history 文件分别负责回答

具体规则文件负责回答：

- 什么算 archetype-complete
- admission 的具体门槛是什么
- common-core 与 extended 如何具体划分
- 哪些 case 可以从 staged 升级
- review 时应检查哪些 artifacts
- 哪些条件下 case 只能留在 extended 或 staging

review-history 文件负责回答：

- 某一批 case 在某一轮 promotion / admission 审查中，实际作出了什么判断
- 当时的判断依据是什么
- 当时预期会带来哪些 metadata consequences

也就是说：

- `benchmark_spec/*rules*.md` 负责长期规则
- `benchmark_spec/reviews/*.md` 负责批次级审查记录

### 11.3 治理目标

样本治理不是附属工作，而是 benchmark 可信度的一部分。

一个 benchmark 不仅要回答“收了哪些 case”，还要回答：

- 这些 case 为什么进入正式集合
- 它们当前处于什么成熟度状态
- 哪些 case 可以参与公平横向比较
- 哪些 case 只适合作为扩展覆盖与失败分析材料

因此，本项目要求将：

- archetype-completion
- promotion / admission
- common-core / extended 分线
- review artifact 要求

都纳入显式、可审阅、可复验的规则体系，而不是留在临时讨论或实验备注中。

### 11.4 治理执行口径

在实际执行中，治理信息按以下层级维护：

- case 级实时状态，以 `inventory/case_registry.csv` 为准
- source 级实时状态，以 `inventory/source_registry.csv` 为准
- 当前阶段判断、当前 focus 与代表性快照，以 `docs/EXECUTION_STATUS.md` 为准
- completion / admission / common-core / extended 的具体判定，以 `benchmark_spec/*rules*.md` 为准
- 某一批 case 的 promotion / admission 审查记录，以 `benchmark_spec/reviews/*.md` 为准
- 本文件只保留长期治理框架，不重复承载实时状态

若不同层之间出现冲突，应优先按以下原则处理：

- source / case 的实时事实，以 registry 为准
- 当前阶段解释，以 `docs/EXECUTION_STATUS.md` 为准
- 批次级审查记录，以 `benchmark_spec/reviews/*.md` 为准
- 长期规则，以 `benchmark_spec/*rules*.md` 与 `benchmark_spec/decision_log.md` 为准

---

## 12. LLM 与 Codex 使用策略

### 12.1 Codex 的角色
Codex 是工程脚手架工具，不是科学决策者。

适合承担：

- CLI scaffolding
- environment checks
- parser / validator glue code
- case manifest validator
- plan normalizer
- report generation
- smoke / preflight automation
- test / CI scaffolding

不适合承担：

- benchmark 口径制定
- metrics 最终定义
- ground-truth 等价性裁定
- 无审阅的新 case 生成
- admission 决策

### 12.2 LLM 的角色
LLM 不是 benchmark 设计者，而是受约束的 coverage hole filler。

LLM 只允许用于：

1. 补 coverage 空洞
2. 生成受限方言变体
3. 生成 hard negatives 候选

所有 LLM 生成结果必须经过：

- parser / formatter checks
- multi-engine execution checks
- differential testing
- multi-dataset consistency checks
- 随机人工审阅

### 12.3 阶段性使用原则
- 前期优先用 Codex 做工程脚手架
- LLM 不应在 bootstrap 阶段大规模自由生成 SQL
- 只有当自动校验与人工审阅机制稳定后，才允许更大规模进入 pipeline

---

## 13. 计划可观测性框架

计划可观测性是本项目最关键的差异化维度之一。

### 13.1 逻辑计划层
用于回答 rewrite 改了什么。

典型变化包括：

- join reorder
- predicate pushdown
- subquery decorrelation
- aggregation placement

### 13.2 物理计划层
用于回答收益或回归从哪里来。

典型变化包括：

- join operator replacement
- spool / materialization creation or removal
- sort creation or removal
- scan range narrowing
- exchange / shuffle behavior change

### 13.3 节点级归因层
用于把性能变化具体归因到节点级指标。

典型指标包括：

- runtime
- rows
- cost
- buffer
- spill
- scan bytes

### 13.4 计划可观测输出目标
每个 case 最终应尽量支持以下输出：

- source plan
- rewrite plan
- logical delta
- physical delta
- node-level metrics
- benefit attribution summary

---

## 14. 指标体系（两层）

本项目指标分为两层：

- **A. 方法排名 primary metrics**
- **B. benchmark / artifact support metrics**

### 14.1 方法排名 primary metrics

#### Correctness / Validity
- ExecutableRate
- ResultConsistencyRate
- NegativeRejectionRate

#### Performance
- GM_Speedup
- RegressionRate@20%

#### Generalization
- CrossEngineExecutableRate
- CrossEngineConsistencyRate
- SpeedupTransferRate

### 14.2 Benchmark / artifact support metrics

#### Verification support
- VerifierSupportRate

#### Plan observability support
- PlanParseRate
- NodeAlignmentCoverage
- AttributionCoverage

#### Benchmark characterization support
- DialectPortabilityCoverage
- OperatorDeltaDiversity
- BottleneckRemovalRate

### 14.3 指标原则
- primary metrics 应在前期冻结
- exploratory / support metrics 可以后加
- support metrics 不能冒充 leaderboard primary metrics
- 所有指标定义都必须可复验、可比较、可追踪

---

## 15. Baseline 与评测协议框架

### 15.1 baseline 类型
正式评测阶段的 baseline 至少应覆盖：

- 规则型 rewrite baseline
- 优化器或候选生成型 rewrite baseline
- LLM 型 rewrite baseline
- 跨方言任务中的 translation baseline

### 15.2 协议要求
所有 baseline 必须在以下条件下运行：

- 同一批 case package
- 同一引擎设置
- 同一结果校验逻辑
- 同一 artifact 记录口径

### 15.3 报告要求
- 必须保留失败样本分析
- 不允许只展示成功子集
- capability boundary 必须显式标记
- 不同能力边界的方法不得直接混报

---

## 16. 里程碑框架

### M0：规格冻结
关键产出：

- 任务定义
- taxonomy
- case schema
- primary metrics
- 冻结边界

通过条件：

- 团队对 v1 范围无冲突
- spec / decision log 可作为执行依据

### M1：覆盖盘点
关键产出：

- source inventory
- coverage map
- gap report

通过条件：

- 能识别优先补齐的 feature buckets
- 能区分现有来源与后续需要补的 coverage holes

### M2：Pilot
关键产出：

- 80–120 个高质量 case package
- 三引擎执行链路
- 初步 baseline 可运行
- 初步 benchmark characterization

通过条件：

- 可复验
- 可对齐
- 可跑 baseline

### M3：Beta
关键产出：

- 扩展 case 集
- 自动校验器
- 计划对齐工具
- 更稳定的报告管线

通过条件：

- 能稳定输出四组指标
- admission / review / regression 管理机制较清晰

### M4：发布候选
关键产出：

- artifact
- 文档
- baseline 结果
- failure analysis
- 论文主故事骨架

通过条件：

- 达到发布门槛
- 可对外审阅
- 论文叙事和 artifact 相互支撑

---

## 17. 数量目标与规模控制

### 17.1 pre-pilot 目标
在正式进入 M2 前，应先完成一批较小但完整的 case 闭环，用于验证 benchmark 机制本身是否成立。

建议目标：

- 20–30 个手工构造或手工打磨的高质量 case
- 每个 case 至少 1 个 positive rewrite
- 每个 case 至少 1 个 hard negative
- 尽可能具备 tri-engine consistency closure

### 17.2 pilot 目标
M2 的建议目标为：

- 80–120 个高质量 case package

可按四池大致分布控制：

- performance：40–60
- long-tail：30–40
- consistency：25–35
- portability：20–30

说明：

- 这些数字是 pilot 目标区间，不要求一步到位
- 实际推进时允许阶段性不平衡
- 数量目标不得替代质量门槛

### 17.3 规模控制原则
- 先做强闭环，再扩规模
- 先保 common-core，再扩 extended
- 先把 archetype 做扎实，再做批量复制
- 不为了凑数牺牲 provenance、校验和计划可观测性

---

## 18. 高层执行路线图

高层执行路线图是**阶段门槛级指导**，不是僵硬的逐日流水线脚本。  
它用于定义依赖关系、推进顺序与阶段转换条件，而不是要求所有 source 必须完全下载后才能开始任何 case。

### Step 1
搭起机器与三引擎 smoke。

### Step 2
完成 taxonomy、case schema 与 spec 初版。

### Step 3
完成首批 benchmark source 的受控获取与 staging。

### Step 4
完成初步数据加载、预处理与执行路径验证。

### Step 5
完成首批 anchor case 与 archetype case。

### Step 6
完成计划采集、节点对齐与基础报告。

### Step 7
在约束条件下引入 LLM 进入 coverage-hole filling 流程。

### Step 8
形成 pilot 级四池 benchmark 结构。

### Step 9
运行 baseline，观察 ranking shift 与 failure distribution。

### Step 10
形成第一版 benchmark characterization 与论文故事。

### 18.1 路线图的执行原则：gated-iterative
本项目采用**硬门槛 + 弹性并行**方式推进。

必须优先满足的硬门槛包括：

- tri-engine smoke
- benchmark spec
- taxonomy 初版
- case schema 初版
- 结果校验闭环
- 计划采集闭环

一旦某个 source 已经满足以下条件：

- 已完成受控获取与 staging
- 已完成初步 inspection
- 已能抽出较清晰的 seed

则允许**不等待所有其他 source 全部到位**，直接进入：

- seed extraction
- prototype case construction
- tri-engine execution 尝试
- 局部 archetype 打磨

也就是说，本路线图不是 waterfall，而是：

- 在全局边界和门槛固定的前提下
- 允许 source 级 prototype case 提前启动
- 允许 selective deepening 先于 broad expansion

---

## 19. 风险与控制原则

### 19.1 范围膨胀
控制原则：
- 坚持三引擎冻结
- 超范围内容进入 backlog，而不是立刻纳入 v1

### 19.2 正确性误判
控制原则：
- 统一结果规范化规则
- 使用 witness dataset
- 关键 case 多实例复验

### 19.3 计划节点对齐不稳
控制原则：
- 先建立 canonical operator taxonomy
- 先做逻辑层，再做物理层

### 19.4 LLM 生成噪声过高
控制原则：
- 仅对 coverage holes 使用
- 设置 parser + execution 双门槛
- 随机人工抽检

### 19.5 provenance 或许可不清
控制原则：
- provenance 不清的样本不得进入正式集

---

## 20. 项目成功标准

本项目的成功，不是“收集了很多 SQL”，而是形成一个真正能支撑 EA&B 论文叙事的 benchmark 体系：

- 能同时覆盖一致性、性能、计划可观测性、跨引擎泛化
- 能用 case package 而不是 query string 组织 benchmark
- 能给出现有方法在新 benchmark 上的 ranking shift 与 failure map
- 能生成可复验 artifact
- 能支撑论文、artifact 和方法比较的一体化叙事

---

## 21. 维护原则

本文档只描述长期稳定计划与正式框架。  
以下内容不写入本文档，而由独立文件维护：

- 当前执行状态 → `docs/EXECUTION_STATUS.md`
- 当前 step 进度 → `docs/EXECUTION_STATUS.md`
- 当前 active focus → `docs/EXECUTION_STATUS.md`
- source 级真实纳入状态 → `inventory/source_registry.csv`
- case 级实时事实 → `inventory/case_registry.csv`
- promotion / admission 的批次级审查记录 → `benchmark_spec/reviews/*.md`
- promotion / admission 的实时状态变化 → `inventory/case_registry.csv` 与对应 rules / decision log
- 每周任务推进记录 → 独立状态文件或归档文件
- 单 case 的 completion / admission 细则 → `benchmark_spec/*rules*.md`
- 文件入口、更新顺序与归档规则 → `docs/DOC_MAP.md`

若本文件中的框架性描述与其他层冲突：

- source 级事实以 `inventory/source_registry.csv` 为准
- case 级事实以 `inventory/case_registry.csv` 为准
- 当前阶段判断与当前 focus 以 `docs/EXECUTION_STATUS.md` 为准
- 批次级审查记录以 `benchmark_spec/reviews/*.md` 为准
- 长期规则与冻结决策以 `benchmark_spec/*rules*.md` 和 `benchmark_spec/decision_log.md` 为准

本文件不重复承担上述内容的实时更新职责。