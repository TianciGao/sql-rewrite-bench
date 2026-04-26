# EXECUTION_STATUS.md
## 当前执行状态与近期动作入口

---

## 1. 文档角色

本文档是本仓库的**唯一动态状态入口**，也是当前阶段的**状态仪表盘 / 解释层**。

它负责记录：

- 当前阶段判断
- 当前 active focus
- 当前 step 进度
- 当前代表 case package 状态矩阵
- 当前 source line 使用现状
- 当前 blockers / risks
- 近期下一步动作

本文档不负责：

- 重写长期研究计划
- 定义 benchmark 规则
- 替代 decision log
- 替代 registry
- 承载一次性 scratch 分析
- 记录所有历史聊天或所有执行细节
- 作为 case / source 级完整 source-of-truth
- 替代 review-history 文件

换句话说：

- `PROJECT_PLAN.md` 讲长期稳定框架
- `benchmark_spec/*.md` 讲规则与冻结边界
- `benchmark_spec/reviews/*.md` 讲批次级 review-history
- `inventory/source_registry.csv` 讲 source 级实时事实
- `inventory/case_registry.csv` 讲 case 级实时事实
- `EXECUTION_STATUS.md` 只讲：**现在做到哪里、这些事实当前应如何被解释**

其中：

- case 级实时事实以 `inventory/case_registry.csv` 为准
- source 级真实纳入状态以 `inventory/source_registry.csv` 为准
- review-history 以 `benchmark_spec/reviews/*.md` 为准
- 本文件只保留代表性快照与当前解释，不承担完整 source-of-truth

---

## 2. 更新规则

### 2.1 默认更新时机
以下情况发生时，应优先更新本文件：

- 当前阶段判断发生变化
- 当前 active focus 发生变化
- 某个重要 step 状态发生变化
- 某个关键 case 的代表性状态快照需要更新
- 某条 source line 的代表性状态快照需要更新
- 当前 blockers / risks 发生变化
- 下一步行动清单发生变化

### 2.2 registry-first 更新顺序
若某次任务同时影响规则、对象状态与执行状态，推荐更新顺序为：

1. 先更新规则文件（如适用）
2. 再更新 registry / case files（如适用）
3. 再更新 review-history 文件（如适用）
4. 最后更新本文件做摘要性回写

更具体地说：

- 若 source / case 的实时事实发生变化，必须先改对应 registry
- 若规则发生变化，必须先改对应 rules / decision log
- 若批次审查结论发生变化，应先改对应 `benchmark_spec/reviews/*.md`
- 本文件只负责在此基础上做当前解释和快照更新

### 2.3 不应在此文件中完成的动作
若变更属于以下内容，不应只改本文件：

- 冻结决策变化 → `benchmark_spec/decision_log.md`
- 规则变化 → 对应 `benchmark_spec/*rules*.md`
- review 结论变化 → 对应 `benchmark_spec/reviews/*.md`
- source 结构化状态变化 → `inventory/source_registry.csv`
- case 结构化状态变化 → `inventory/case_registry.csv`
- taxonomy 定义变化 → 对应 `taxonomy/*.yaml`

### 2.4 禁止的错误更新方式
以下做法视为不合格更新：

- 只改本文件，不改 registry，却声称 source / case 状态已变化
- 只改本文件，不改 review 文件，却声称 promotion / admission 结论已变化
- 在本文件中手工维护完整 case 世界观，而不回写 `case_registry.csv`
- 在本文件中重新定义规则口径，而不更新 rules / decision log

---

## 3. 基本信息

- **Status Owner：**（填写负责人）
- **Last Updated：**（填写日期）
- **Current Repository Branch：**（可选）
- **Current Phase Label：** pilot benchmark consolidation with selective deepening and governance hardening
- **Snapshot Basis：**
  - source facts → `inventory/source_registry.csv`
  - case facts → `inventory/case_registry.csv`
  - batch review history → `benchmark_spec/reviews/BATCH1_EXTERNAL_CASE_REVIEW_v1.md`

---

## 4. 当前阶段判断（多轴）

### 4.1 总体阶段标签

当前项目处于：

> **pilot benchmark consolidation with selective deepening and governance hardening**

这意味着当前重点不是“先做更大规模扩张”，而是：

- 稳定现有最强 case
- 深化外部 archetype case
- 把 promotion / admission / common-core / extended 规则进一步收口
- 把 package engineering 与 characterization 准备做扎实
- 让 registry、review-history、当前状态解释三层彼此对齐

### 4.2 source 层判断

当前 source 层的总体状态不是“还在早期下载阶段”，而是：

- Batch-1 关键 source 体系已基本建立
- 部分 source 已进入 seed / case materialization
- 部分 target source 仍处于 planned / partial realized 状态
- 当前阶段不应回到 broad source expansion

简言之：

> 当前 source 层是“已形成主干，但仍有未闭合支线”的状态。

### 4.3 case 层判断

当前 case 层已经形成以下结构：

- anchor layer 已稳定
- external archetype layer 已形成
- selective promotion 已发生
- first external admissions 已发生
- staged / candidate / admitted 分层开始真正发挥作用

简言之：

> 当前 case 层不是“只有锚点的 bootstrap 仓库”，而是“已经进入 pilot-level case governance 的仓库”。

### 4.4 package engineering 层判断

当前 package engineering 的总体状态是：

- anchor packages 稳定
- 多个 external cases 已达到 formal skeleton complete
- release-grade completeness 仍明显不足
- canonical AST / logical IR / span→logical→physical mapping 仍是后续深化重点

简言之：

> 当前更像“package skeleton 已成、release-grade engineering 尚未完成”。

### 4.5 evaluation 层判断

当前 evaluation 层的总体状态是：

- tri-engine closure 已在 anchor 层建立
- 部分 external cases 已有 tri-engine closure
- plan artifacts 已有基础
- characterization 准备中
- 尚未进入大规模 baseline ranking 阶段

简言之：

> 当前 evaluation 层已具备 pilot characterization 前提，但还不适合宣布大规模 comparative benchmark fully open。

---

## 5. 仓库基线快照

### 5.1 基础设施与协议基线
当前仓库已具备的基础状态：

- tri-engine smoke completed
- minimal CLI scaffolding completed
- artifact-preflight completed
- source inventory v0 established
- pool mapping rules established
- common-core / extended rules established
- primary metrics v0 established
- taxonomy v0.2 established

### 5.2 含义解释
这意味着仓库已经不再处于“纯 bootstrap”阶段，  
而是已经具备：

- 基本执行链路
- 基本规则层
- 基本 source / pool / metric / taxonomy 结构
- 初步 case governance 能力

后续工作重点应转向：

- selective deepening
- case governance hardening
- package engineering 深化
- benchmark characterization preparation

---

## 6. Step 进度快照

> 说明：本节只记录当前 step 状态摘要。  
> 长期 step 设计见 `docs/PROJECT_PLAN.md`。

| Step | 名称 | 当前状态 | 备注 |
|---|---|---|---|
| 1 | Machine bring-up and tri-engine smoke | completed | 三引擎 smoke 已完成 |
| 2 | Taxonomy and case schema | completed at current pilot level | taxonomy / schema 基线已建立 |
| 3A | Controlled Batch-1 source acquisition and staging | completed | Batch-1 核心来源已进入受控获取 |
| 3B | Batch-1 source inspection and seed extraction | completed | inspection / seed extraction 已初步完成 |
| 4 | Data loading and preprocessing | completed for current pilot archetypes | 对当前 archetype 所需范围已足够 |
| 5 | First anchor cases | completed | 四个 anchor case 已建立 |
| 6 | First external draft cases | completed | 第一批 external draft 已形成 |
| 7 | Archetype completion | completed | `002` archetypes 已形成当前 archetype-complete 参考层 |
| 8 | Promotion review and first admission | completed for first review cycle | 第一轮 promotion / admission 已完成，并已收口为 consolidated Batch-1 review |
| 9 | Selective deepening, not broad expansion | active | 当前主阶段 |
| 10 | Reusable case construction workflow | in progress | 当前持续推进 |
| 11 | Pilot benchmark characterization | next | 进入准备期，尚未正式收口 |
| 12 | Draft the first benchmark paper story | next | 尚未正式展开 |

---

## 7. 当前代表 Case Package 状态矩阵

> 本节记录当前最能代表仓库能力和成熟度结构的 case 快照。  
> **case 级完整实时事实以 `inventory/case_registry.csv` 为准。**  
> 若本节与 `inventory/case_registry.csv` 冲突，应优先以 `case_registry.csv` 为准。  
> 对于 Batch-1 external cases 的批次级审查解释，可参见：`benchmark_spec/reviews/BATCH1_EXTERNAL_CASE_REVIEW_v1.md`。

### 7.1 Performance cases

| case_id | 数据集 / 来源 | 当前成熟度 | package engineering 状态 | 已验证引擎 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| PERF_0001 | 手工 smoke / manual_smoke 锚点（非外部 benchmark） | stable pilot anchor | anchor package（尚未按 formal skeleton validator 全量回扫） | PostgreSQL / MySQL / Spark | 无 admission 缺口；继续作为 smoke / pipeline anchor；后续统一一版 package 工艺后再做 schema / validator 回扫 |
| PERF_0002 | TPC-DS query53.tpl，经 dsqgen materialize 成实例 | admitted external common-core | formal skeleton complete；release-grade incomplete | PostgreSQL / MySQL / Spark | admission 已过；后续转向 deeper package engineering，补 canonical AST / logical IR / SQL span→logical→physical mapping，及短期 characterization / stabilization |
| PERF_0003 | JOB / IMDB，27a.sql | PG validated performance draft with positive / negative pair | formal skeleton complete；release-grade incomplete（PG-only validated） | PostgreSQL | 还缺 MySQL / Spark closure；当前继续保持 not_yet_admitted staged；后续再决定是否推进 common-core candidate |
| PERF_0004 | JOB / IMDB，30b.sql | PG validated performance draft with positive / negative pair | formal skeleton complete；release-grade incomplete（PG-only validated） | PostgreSQL | 还缺 MySQL / Spark closure；当前继续保持 not_yet_admitted staged；后续优先看是否复用 PERF_0003 的跨引擎扩展工艺 |

### 7.1.1 Recent TPC-DS selective deepening checkpoint

当前 TPC-DS performance 线的 selective deepening 已形成最新一轮 tri-engine closure checkpoint。  
目前 `PERF_0033`、`PERF_0034`、`PERF_0035`、`PERF_0036`、`PERF_0038`、`PERF_0043`、`PERF_0044`、`PERF_0047`、`PERF_0050`、`PERF_0052`、`PERF_0053`、`PERF_0054`、`PERF_0056`、`PERF_0062`、`PERF_0063`、`PERF_0065`、`PERF_0066`、`PERF_0071`、`PERF_0072`、`PERF_0073`、`PERF_0074`、`PERF_0075`、`PERF_0076` 已具备 PostgreSQL / MySQL / Spark closure。  
`PERF_0032` 仍不计入 routine closed 集合，当前仍待单独 human SQL normalization decision；`PERF_0046` / `PERF_0048` 保持 deferred；`PERF_0067` / `PERF_0068` 仍未形成 tri-engine closure，留待后续单独 decision 或 future work。  
这些变化已经与 `inventory/case_registry.csv` 对齐；case 级 live facts 仍以 `inventory/case_registry.csv` 为准。  
本 checkpoint 只表示当前 selective closure 进展，不意味着 admission、promotion、common-core movement，或 formal review completion。

### 7.2 Long-tail cases

| case_id | 数据集 / 来源 | 当前成熟度 | package engineering 状态 | 已验证引擎 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| LONGTAIL_0001 | 手工构造的 long-tail anchor case（非外部 benchmark） | stable pilot anchor | anchor package（尚未按 formal skeleton validator 全量回扫） | PostgreSQL / MySQL / Spark | 无 admission 缺口；继续作为 structure-rich longtail anchor；后续统一 package 工艺后再做 schema / validator 回扫 |
| LONGTAIL_0002 | SQLStorm / StackOverflow workload seed | PG-validated draft with positive / negative pair；remain not_yet_admitted | formal skeleton complete；release-grade incomplete（PG-only validated） | PostgreSQL | benchmark 侧还缺 MySQL / Spark 验证；当前价值主要在 long-tail 结构覆盖，不急于推进 common-core |

### 7.3 Consistency cases

| case_id | 数据集 / 来源 | 当前成熟度 | package engineering 状态 | 已验证引擎 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| CONS_0001 | 手工 consistency 锚点包；小型员工 witness 数据 | stable pilot anchor | anchor package（尚未按 formal skeleton validator 全量回扫） | PostgreSQL / MySQL / Spark | 无 admission 任务；继续作为 correctness anchor；后续统一 package 工艺后再做 schema / validator 回扫 |
| CONS_0003 | VeriEQL / calcite subset，Calcite-397 / 159 | PG + MySQL validated staged consistency draft | formal skeleton complete；release-grade incomplete | PostgreSQL / MySQL | benchmark 仍缺 Spark closure；当前保持 staged / not_yet_admitted；下一步重点是 Spark 或继续补 AST / IR / mapping / checker，而不是 admission |
| CONS_0004 | VeriEQL / calcite subset，Calcite-397 / 362 | PG + MySQL validated staged consistency draft | formal skeleton complete；release-grade incomplete | PostgreSQL / MySQL | benchmark 仍缺 Spark closure；当前保持 staged / not_yet_admitted；下一步与 CONS_0003 同步推进更整齐 |
| CONS_0002 | Calcite seeds，core/src/test/resources/sql/new-decorr.iq | PG-validated draft with positive / negative pair；remain not_yet_admitted | staged draft（pre-skeleton / 尚未完全回填 formal package 结构） | PostgreSQL | 还缺 broader engine validation；package 侧也还没 formal skeleton；当前先保持 staged 更稳 |

### 7.4 Portability cases

| case_id | 数据集 / 来源 | 当前成熟度 | package engineering 状态 | 已验证引擎 | 下一步缺口 |
| --- | --- | --- | --- | --- | --- |
| PORT_0001 | `PORT_0001_package.zip` 锚点包（repo 内 portability anchor；非外部 seed） | stable pilot anchor | anchor package（尚未按新 formal skeleton validator 全量回扫） | PostgreSQL / MySQL / Spark | 无 admission 缺口；继续作为 clean portability anchor；若后续统一 package 工艺，再按新 schema / validator 回扫 |
| PORT_0002 | PARROT / BIRD，`benchmark/BIRD/pg_res.json[0]` | admitted external common-core | formal skeleton complete；release-grade incomplete | PostgreSQL / MySQL / Spark（PG source；MySQL+Spark rewrite closure） | admission 已过；package 骨架已补齐；后续若继续深化，应优先做 portability-specific checker / deeper observability，而不是继续争 admission |

### 7.5 快照维护原则
- 本节只保留代表性 case
- 本节不负责维护完整 case 宇宙
- 新的 case 状态变化，必须先更新 `inventory/case_registry.csv`
- 只有当这些变化影响“当前阶段判断”或“代表性快照”时，才回写本节
- 若涉及批次级 promotion / admission 结论，也应同步检查 `benchmark_spec/reviews/*.md` 是否需要更新

---

## 8. 当前 Source Line 状态快照

> 本节回答的不是“目标 source 全集是什么”，而是“这些 source 现在在仓库里真实被用到了什么程度”。  
> **source 级完整实时事实以 `inventory/source_registry.csv` 为准。**  
> 若本节与 `inventory/source_registry.csv` 冲突，应优先以 `source_registry.csv` 为准。

| 目标源 | 预定角色 | 当前真实状态 | 现在该怎么理解 |
| --- | --- | --- | --- |
| TPC-H | performance | Batch-1 已 staged，但 inspection 只算 partial。它在 source inspection 表里是 staged、license_visible=yes，但 inspection_status=partial，说明源已经到位，不算彻底没做，但也不是 fully inspected。 | 已纳入 Batch-1 完成面，但还不是最成熟的 seed 来源。 |
| TPC-DS | performance | Batch-1 已完成 staging + inspection，并已进入 seed / case 流程。inspection_status=good，而且后续 external seed / case 线里已经 materialize 出 PERF_0002。 | 这是目前最成熟的 performance 外部 source。 |
| DSB | performance realism supplement | 基本还没开始。在最早的 source_registry 口径里它仍是 planned，并且 decision_needed=yes。 | 目前仍停留在“保留为 target source”的层面，尚未进入实质 acquisition / inspection。 |
| JOB | performance realism supplement | 已部分 materialize 到 PERF_0003 / PERF_0004，但当前明确冻结为 partial realized performance supplement。 | 不是 fully closed source line；当前阶段不继续 deepen，保留为部分实现的 performance supplement。 |
| SQLStorm | long-tail | Batch-1 已完成 staging + inspection，在 inspection 表里是 good，且被当成长尾覆盖源而不是立即大规模 case 扩展源。 | 这是目前最成熟的 long-tail source。 |
| Stack | long-tail / realism | 当前拿到的是 Stack Exchange dumps / substrate，不是 direct SQL query corpus。 | 当前已冻结为 realism substrate only；不是 active direct-query source。 |
| Calcite | consistency | Batch-1 已完成 staging + inspection，inspection 口径是 good。后续 CONS_0002 也已经沿着这条 consistency seed 线推进。 | Calcite 这条一致性主线已经立住。 |
| SQLEquiQuest / VeriEQL（二选一） | consistency supplement | 这条“二选一决策”本身已经完成：当前实际上已经选了 VeriEQL。后续记录明确写了 VeriEQL 已被接受为 Batch-2 consistency supplement source，并产出 CONS_0003 / CONS_0004。 | 所以这项不该再算 pending choice；真正没做的是 SQLEquiQuest 分支。 |
| PARROT | portability | Batch-1 已完成 staging + inspection，并已进入 seed / case 流程。inspection 表里 good，source_registry 也已更新到 downloaded/staged；后续 portability 线 materialize 出 PORT_0002。 | 这是目前最成熟的 portability source。 |
| Manual Seed Cases | manual_seed / coverage hole filler | 不是“下载型 source”，而是内部 source family，且其实已经在用。早前明确过它是 manual_seed，不是第五个 pool；四个 anchor cases 和手工 smoke / witness 线，本质上就是这条来源在发挥作用。 | 这项不能按“有没有下载完”来判断，因为它本来就不是外部 acquisition 对象。 |

### 8.1 当前 source 使用情况总览

- **手工锚点 / repo 内 package**：`PERF_0001`, `LONGTAIL_0001`, `CONS_0001`, `PORT_0001`
- **TPC-DS**：`PERF_0002`
- **JOB**：`PERF_0003`, `PERF_0004`
- **SQLStorm**：`LONGTAIL_0002`
- **Calcite Seeds**：`CONS_0002`
- **VeriEQL**：`CONS_0003`, `CONS_0004`
- **PARROT**：`PORT_0002`

### 8.2 解释原则
本节的作用不是定义“最终 source roster”，而是解释：

- 哪些 source 已经真实进入 case 流程
- 哪些 source 仍停留在 target / planned / partial realized
- 当前仓库真正的 source backbone 是什么

### 8.3 快照维护原则
- 本节只保留对当前阶段最重要的 source line 解释
- source 级事实变化，必须先更新 `inventory/source_registry.csv`
- 本节只在这些变化影响当前阶段判断或当前 source backbone 解释时回写

---

## 9. 当前 active focus

当前项目的 active focus 应限定为以下几项：

- selective deepening
- external case promotion / admission governance
- review-history consolidation and registry alignment
- package engineering 深化
- documentation and workflow consolidation
- preparation for later scalable case construction
- preparation for pilot benchmark characterization

当前不应把主要精力放在：

- broad source expansion
- large-scale workload curation
- mass case generation
- 无约束 LLM case 扩张
- 过早开始大规模 baseline 排行实验

---

## 10. 当前 blockers / risks

> 本节只写当前仍影响推进的关键问题。  
> 若某项已成为稳定规则，应移入 rules 或 decision log，而不是长期停留在这里。

### 10.1 文档治理仍需收口
当前仓库已有较多 md 文件与状态说明，仍存在：

- 文件职责边界不够稳定
- 动态状态入口历史上分散
- 一次性文档容易升格为正式文件

### 10.2 registry-first 更新纪律尚需稳定
当前 source / case 层虽然已有 registry 方向，但仍需继续强化以下纪律：

- source 事实先改 `source_registry.csv`
- case 事实先改 `case_registry.csv`
- review-history 先改 `benchmark_spec/reviews/*.md`
- 本文件只做快照与解释层回写

### 10.3 package engineering 与 benchmark maturity 仍未完全解耦
当前多个 case 已达到 formal skeleton complete，但 release-grade completeness 仍不足。  
若不显式区分这两层状态，后续容易在 maturity 判断上发生混读。

### 10.4 selective deepening 的边界需要继续守住
当前最容易出现的偏移，是在 selective deepening 尚未完成前，又重新回到 broad expansion 或 mass case generation。

### 10.5 source line 真实状态与目标 roster 仍可能混读
例如：

- 把 target source roster 误读为“当前都已 fully active”
- 把 partial realized supplement 误读为 fully closed source line
- 把 realism substrate 误读为 direct query corpus

### 10.6 review-history 与 live status 仍需持续对齐
当前已经建立 consolidated Batch-1 review-history 层，但后续若 case 状态继续演化，仍需防止：

- review 文件停留在旧批次判断
- registry 已更新但 review-history 未同步
- status dashboard 与 review-history 口径重新漂移

---

## 11. 近期下一步动作

### 11.1 文档与治理层
- 固定 `PROJECT_PLAN.md` 为长期稳定计划文件
- 固定本文件为唯一动态状态入口
- 固定 `decision_log.md` 为冻结决策入口
- 固定 rules 文件为 completion / admission / common-core 细则入口
- 固定 `benchmark_spec/reviews/` 为批次级 review-history 层
- 强制执行 registry-first 更新顺序
- 持续维护 `source_registry.csv` 与 `case_registry.csv`

### 11.2 case 与 workflow 层
- 继续收口 `002` archetype 的 reusable workflow
- 将 selective promotion / admission 的流程进一步规则化
- 明确 common-core / extended 的实际应用边界
- 补 formal skeleton → release-grade 的中间工艺缺口
- 在 review-history、registry 与 case-local artifacts 三层之间保持同步

### 11.3 benchmark characterization 准备层
- 在不 broad expansion 的前提下，稳定现有 strongest cases
- 整理 anchor + external archetype 的第一版 characterization 支撑材料
- 为后续 benchmark story 与 paper narrative 做结构准备

---

## 12. 当前推荐读取顺序

对于大多数当前阶段任务，推荐读取顺序为：

1. `benchmark_spec/decision_log.md`
2. `docs/PROJECT_PLAN.md`
3. `benchmark_spec/benchmark_spec_v0.md`
4. `docs/EXECUTION_STATUS.md`

若任务涉及规则判定，再额外读取：

- `benchmark_spec/primary_metrics_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/CASE_ADMISSION_RULES_v0.md`
- `docs/POOL_MAPPING_RULES.md`

若任务涉及批次审查依据，再额外读取：

- `benchmark_spec/reviews/BATCH1_EXTERNAL_CASE_REVIEW_v1.md`

若任务涉及 source / case 对象状态，再额外读取：

- `inventory/source_registry.csv`
- `inventory/case_registry.csv`

说明：

- 若任务目标是**判断当前阶段与当前 focus**，优先读本文件
- 若任务目标是**确认 source / case 的实时事实**，优先读 registry
- 若任务目标是**理解 Batch-1 promotion / admission 的历史判断依据**，优先读 review-history 文件
- 若本文件与 registry 冲突，应优先以 registry 为准

---

## 13. 本文件不应承载的内容

以下内容不应继续写入本文件：

- 长期研究主张与完整方法论叙事
- 冻结规则细则全文
- taxonomy 正式定义
- source / case 的完整实时事实表
- 单个 batch 的完整 review-history 正文
- 一次性 scratch 分析
- 某轮临时实验长报告

若这些内容出现在本文件中，应考虑迁移至：

- `PROJECT_PLAN.md`
- `benchmark_spec/*rules*.md`
- `benchmark_spec/reviews/*.md`
- `taxonomy/*.yaml`
- `inventory/*.csv`
- `docs/_scratch/`
- `docs/archive/`

---

## 14. 维护提醒

如果本文件开始不断长出：

- 多个并列状态小节
- 多个 case 专用状态块
- 多个 source 专用状态块
- 多个阶段性 checklist
- 多个 review-history 摘抄块
- 多个临时 closeout 记录

那么说明动态状态再次发生扩散，  
应优先执行：

1. 先看该信息是否本质上属于事实层
2. 若属于事实层，先吸收到 registry
3. 若属于批次级审查解释，先吸收到 `benchmark_spec/reviews/`
4. 若属于解释层，合并回本文件
5. 若仅有短期价值，降级归档到 `docs/archive/` / `docs/_scratch/`

若本文件与其他层发生冲突，处理顺序应为：

- case 级事实冲突 → 以 `inventory/case_registry.csv` 为准
- source 级事实冲突 → 以 `inventory/source_registry.csv` 为准
- Batch-level review-history 冲突 → 以 `benchmark_spec/reviews/*.md` 为准
- 当前阶段判断 / 当前 focus 冲突 → 以本文件最新版本为准
- 长期方向冲突 → 回到 `PROJECT_PLAN.md` 与 `decision_log.md`

本文件的目标不是变成“另一个总计划”，  
也不是变成“另一个完整 registry”，  
也不是变成“另一个 review 文档”，  
而是始终保持为：

> **唯一动态状态入口 + 当前状态仪表盘 + 解释层**
