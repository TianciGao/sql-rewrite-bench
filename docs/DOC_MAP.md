# DOC_MAP
## 文档地图与治理规则

---

## 1. 文档目的

本文件不是普通目录清单，而是本仓库的**文档地图、职责边界与治理规则**。

它回答五个问题：

1. 哪些文件是默认必读文件
2. 每类信息应该写到哪里
3. 新文件什么时候允许创建
4. 哪些文件应该合并、归档或降级
5. `PROJECT_PLAN.md`、`EXECUTION_STATUS.md`、registry、规则文件之间如何协同

本文件的目标不是让文档越列越多，而是保证：

- 主线文件保持少而稳
- 规则文件职责清晰
- 动态状态有唯一入口
- 结构化信息尽量回到 registry
- 临时材料不会无控制地升级为正式文件
- 不同层级的文件不会互相重复、互相打架

---

## 2. 总体原则

### 2.1 一类信息只能有一个主入口
同一种信息，不允许长期分散在多个并列 md 文件中。

### 2.2 长期稳定内容与动态状态必须分离
- 长期稳定内容写入计划、spec、规则文件
- 高频变化内容写入执行状态或 registry
- 不允许继续把动态状态混进总计划

### 2.3 结构化信息优先进入 registry
只要信息本质上是表格、状态、清单、字段集合，优先进入 csv / yaml，而不是散落在多个 md 表格中。

### 2.4 临时材料默认不升格
新产生的临时分析、一次性总结、草稿性写作材料，默认进入 scratch 或 archive，不自动升格为正式文档。

### 2.5 新文件不是默认选项
每次想新建 md 文件时，必须先证明：

> 这条信息为什么不能写进现有文件？

如果回答不出来，就不应新建。

### 2.6 先改事实，再改解释
若一次任务同时改变了对象状态和状态说明，必须优先更新 registry，再更新状态文件；不允许只改解释层而不改事实层。

---

## 3. 默认必读文件（主线文件）

以下文件构成仓库的**默认必读集合**。  
除非任务明确要求，否则任何人类或 agent 不应在开工前同时读取大量其他文件。

### 3.1 `docs/PROJECT_PLAN.md`
角色：
- 长期稳定的研究总计划
- 回答项目为什么做、整体怎么做、最终想做成什么

不负责：
- 动态状态
- 当前 case 实时进度
- admission 细则
- 当前周任务
- source / case 的实时事实

### 3.2 `benchmark_spec/benchmark_spec_v0.md`
角色：
- 当前版本 benchmark 的执行合同 / 当前施工蓝图
- 回答当前这版 benchmark 到底在做什么、现在不能做什么、做到哪算成立

### 3.3 `benchmark_spec/decision_log.md`
角色：
- 冻结决策唯一登记簿
- 任何正式决定都必须回写这里，不依赖聊天记录记忆

### 3.4 `docs/EXECUTION_STATUS.md`
角色：
- 当前执行状态唯一入口
- 记录当前 active phase、当前 focus、当前 blockers、下一步动作
- 记录当前代表 case 快照与当前 source line 快照
- 记录阶段完成情况，但不改变长期计划

约束：
- 本文件是**解释层 / 状态仪表盘**
- 它不承担 case 级完整 source-of-truth
- case 级实时事实应回到 `inventory/case_registry.csv`

---

## 4. 规则文件层

规则文件回答“怎么判、怎么管”，但不承担动态状态记录。

### 4.1 当前规则文件类型
典型包括：

- `benchmark_spec/primary_metrics_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/CASE_ADMISSION_RULES_v0.md`
- `docs/POOL_MAPPING_RULES.md`

### 4.2 规则文件的职责
规则文件负责回答：

- 什么算 archetype-complete
- admission 的具体门槛是什么
- common-core 与 extended 如何划分
- pool mapping 如何判断
- primary metrics 如何定义
- review 时必须检查哪些 artifact

### 4.3 规则文件不负责
规则文件不负责：

- 当前哪些 case 已完成
- 本周谁被提升为 candidate / admitted
- 当前外部 draft case 的实时状态
- 某一轮实验具体跑到了哪里

这些内容应进入 `docs/EXECUTION_STATUS.md` 或 registry。

---

## 5. Registry / 机器可读主表层

只要信息本质上是“对象列表、状态表、字段表、可筛选清单”，应优先放到 registry。

### 5.1 Source registry
- `inventory/source_registry.csv`

角色：
- source inventory 的机器可读主表
- 记录来源、许可、角色、纳入状态、当前阶段处理状态

约束：
- source 级实时事实以本表为准
- `PROJECT_PLAN.md` 只定义 source/pool 的长期框架，不定义实时纳入状态

### 5.2 Case registry
- `inventory/case_registry.csv`

角色：
- case inventory 的机器可读主表
- 记录 case_id、primary_pool、source_family、maturity、benchmark_line、package engineering 状态、closure、admission status、next gap 等

约束：
- case 级实时事实以本表为准
- `EXECUTION_STATUS.md` 只保留代表性 case 快照，不承担完整 source-of-truth
- 若 case 状态发生变化，必须先更新本表，再更新状态文件

### 5.3 Taxonomy tables
- `taxonomy/*.yaml`

角色：
- taxonomy 的机器可读 source of truth

说明：
- taxonomy 的正式定义以 yaml 为准
- md 文件可以解释 taxonomy，但不应替代 yaml 作为主定义

---

## 6. 动态状态文件层

动态状态文件只回答：**现在是什么状态**。

### 6.1 默认唯一入口
- `docs/EXECUTION_STATUS.md`

它应优先承载：

- 当前 active phase
- 当前 focus
- 当前 blockers
- 近期完成事项
- 下一个 checkpoint
- 各 step 当前状态摘要
- 当前代表 case 快照
- 当前 source line 快照

### 6.2 动态状态文件的边界
`docs/EXECUTION_STATUS.md` 应做到：

- 解释当前状态
- 汇总代表性快照
- 不重复维护完整 source / case 实时事实
- 不承载规则全文
- 不改写长期项目计划

### 6.3 不应再横向扩张的状态文件
以下类型文件原则上不应继续作为并列主线扩张：

- `CURRENT_PHASE_CLOSEOUT_CHECKLIST.md`
- `STATE_ALIGNMENT_MATRIX.md`
- `EXTERNAL_DRAFT_CASE_STATUS.md`
- `ANCHOR_CASE_SUMMARY.md`
- 其他只服务于当前阶段状态汇报的 md

处理原则：
- 若仍有价值，则保留为辅助视图
- 若与 `EXECUTION_STATUS.md` 职责重复，应逐步合并
- 若仅有阶段性价值，应归档

---

## 7. 辅助说明文件层

辅助说明文件可以存在，但不应被误读为 source of truth。

典型包括：

- `docs/INVENTORY_TEMPLATE.md`
- `docs/DOC_MAP.md`
- `docs/STACK_DECISION_NOTE.md`
- 其他模板、导航、解释性说明文件

原则：
- 解释已有结构
- 不单独定义主规则
- 不替代 registry / spec / plan / decision log

---

## 8. 论文写作文件层

论文写作文件服务于 paper narrative，不是执行治理入口。

典型包括：

- `paper/outline.md`
- `paper/notes_week1_closeout.md`
- 其他写作草稿、图表说明、叙事整理文件

原则：
- 可以总结阶段成果
- 可以为论文做 narrative support
- 不能替代正式执行规则或当前状态主入口

---

## 9. scratch 与 archive 规则

### 9.1 scratch 区
建议维护：

- `docs/_scratch/`
- 或 `paper/_scratch/`

角色：
- 暂存一次性分析
- 暂存未决定是否转正的草稿
- 暂存某轮 review 的临时整理

原则：
- scratch 文件默认不升格
- 只有在被证明会长期复用时，才允许转正

### 9.2 archive 区
建议维护：

- `docs/archive/`

角色：
- 保存历史快照
- 保存不再代表当前口径，但仍有参考价值的旧文件

归档文件必须明确标记为：

- 历史快照
- 不再作为当前 source of truth
- 仅供回溯参考

---

## 10. 新文件准入规则

任何新文件创建前，必须先回答以下问题：

### 10.1 这条信息属于哪一类？
只能四选一：

- 长期稳定计划
- 执行规则
- 动态状态
- 临时材料

### 10.2 是否已有承载位置？
如果已有承载位置，则必须优先更新旧文件，而不是新建。

### 10.3 是否本质上是表格 / 状态 / 清单？
如果是，应优先进入 registry，而不是 md。

### 10.4 两周后还会被重复引用吗？
- 若不会：默认放 scratch
- 若会：才考虑转正

### 10.5 为什么不能写进已有文件？
如果不能清楚回答，就不应新建。

---

## 11. 文件合并规则

以下情况应优先触发“合并”而不是“继续保留多个入口”：

### 11.1 状态型 md 重复
若多个 md 文件都在记录：

- 当前做到了哪里
- 当前哪些 case 完成
- 当前 focus 是什么
- 当前 source line 真实状态

则它们应优先合并进 `docs/EXECUTION_STATUS.md` 或对应 registry。

### 11.2 表格型 md 重复
若多个 md 里都在维护：

- source 清单
- case 状态表
- pool 状态表
- admission / maturity 快照

则应优先合并到 csv / yaml registry。

### 11.3 规则型 md 重复
若多个文件都在定义：

- completion rules
- admission criteria
- mapping rules

则应合并为单一规则文件，并在 `decision_log` 中记录最新正式位置。

---

## 12. 文件归档规则

满足以下任一条件的文件，应优先进入 archive，而不是继续保留在主线目录中：

- 不再代表当前项目口径
- 已被更正式文件替代
- 只服务于某一阶段性 closeout
- 长期不再作为默认阅读入口
- 仅用于历史回溯

归档动作必须伴随：

- 在 `DOC_MAP.md` 中更新归类
- 在必要时于 `decision_log` 或 `EXECUTION_STATUS.md` 说明替代关系

---

## 13. 每次任务结束后的最小更新协议

每次任务结束后，必须先判断这次变动属于哪一层：

- 长期方向
- 执行规则
- 对象事实
- 当前解释

### A. 主线文件
当且仅当长期计划、版本边界或冻结决策发生变化时更新：

- `docs/PROJECT_PLAN.md`
- `benchmark_spec/benchmark_spec_v0.md`
- `benchmark_spec/decision_log.md`

### B. 规则文件
当且仅当规则本身发生变化时更新：

- `benchmark_spec/*rules*.md`

### C. 事实层
若 source / case 的实时状态变化，应优先更新：

- `inventory/source_registry.csv`
- `inventory/case_registry.csv`

### D. 解释层
若只是需要说明当前状态，应更新：

- `docs/EXECUTION_STATUS.md`

**默认禁止**因为一次任务结束就额外新建一个“总结.md”。

---

## 14. 默认阅读顺序

对于大多数常规任务，默认阅读顺序应收敛为：

1. `benchmark_spec/decision_log.md`
2. `docs/PROJECT_PLAN.md`
3. `benchmark_spec/benchmark_spec_v0.md`
4. `docs/EXECUTION_STATUS.md`

若任务涉及规则判定，再额外读取相应规则文件：

- `benchmark_spec/primary_metrics_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/CASE_ADMISSION_RULES_v0.md`
- `docs/POOL_MAPPING_RULES.md`

若任务涉及对象清单，再额外读取相应 registry：

- `inventory/source_registry.csv`
- `inventory/case_registry.csv`

---

## 15. 当前推荐结构（目标状态）

本仓库的目标文档结构应当收敛为：

### 主线文件（极少数）
- `docs/PROJECT_PLAN.md`
- `benchmark_spec/benchmark_spec_v0.md`
- `benchmark_spec/decision_log.md`
- `docs/EXECUTION_STATUS.md`

### 规则文件（受控数量）
- `benchmark_spec/primary_metrics_v0.md`
- `benchmark_spec/common_core_extended_rules_v0.md`
- `benchmark_spec/CASE_ARCHETYPE_COMPLETION_RULES_v0.md`
- `benchmark_spec/CASE_ADMISSION_RULES_v0.md`
- `docs/POOL_MAPPING_RULES.md`

### registry
- `inventory/source_registry.csv`
- `inventory/case_registry.csv`
- `taxonomy/*.yaml`

### 辅助说明
- `docs/DOC_MAP.md`
- `docs/INVENTORY_TEMPLATE.md`

### 写作文件
- `paper/outline.md`
- `paper/notes_*.md`

### 临时材料
- `docs/_scratch/`
- `paper/_scratch/`

### 历史归档
- `docs/archive/`

---

## 16. 四文件最终协同协议

本仓库中，`PROJECT_PLAN.md`、`inventory/case_registry.csv`、`EXECUTION_STATUS.md`、`DOC_MAP.md` 四个文件分别承担不同层级的职责。

### 16.1 `PROJECT_PLAN.md`
角色：方向文件  
职责：

- 定义长期稳定研究方向
- 定义 v1 范围与非目标
- 定义 benchmark 任务结构、taxonomy 框架、case package 理想形态、四池策略、指标框架与里程碑

不负责：

- 当前阶段判断
- 当前 case 状态
- 当前 source line 真实推进情况
- 当前 step 完成状态

### 16.2 `inventory/case_registry.csv`
角色：case 级 live source-of-truth  
职责：

- 记录 case 的稳定身份字段
- 记录 case 当前成熟度、benchmark_line、package engineering 状态、validated engines、closure、admission 状态与下一步缺口
- 作为 case 级实时状态的唯一主表

不负责：

- 长篇解释
- 当前阶段叙事
- 规则定义

### 16.3 `docs/EXECUTION_STATUS.md`
角色：状态仪表盘 / 解释层  
职责：

- 给出当前阶段判断
- 给出当前 active focus
- 给出当前 blockers / risks
- 给出 step 快照
- 给出代表 case 快照
- 给出 source line 快照

约束：

- case 级实时事实以 `inventory/case_registry.csv` 为准
- 本文件只保留代表性快照，不承担完整 source-of-truth

### 16.4 `docs/DOC_MAP.md`
角色：导航与治理文件  
职责：

- 定义默认必读文件
- 定义每类信息应该写到哪里
- 定义新文件准入规则
- 定义合并、归档与更新顺序
- 定义四文件之间的协同协议

不负责：

- 记录当前状态细节
- 记录 case 实时状态
- 替代规则文件或 registry

### 16.5 更新顺序规则

#### A. 当 case 状态发生变化时
例如：

- validated engines 增加
- benchmark_line 改变
- admission_status 改变
- next_gap 改变

更新顺序必须是：

1. 先更新 `inventory/case_registry.csv`
2. 若涉及正式规则或准入结论，再更新 `decision_log` 或对应 rules
3. 最后更新 `docs/EXECUTION_STATUS.md` 的代表性快照
4. 不更新 `PROJECT_PLAN.md`

#### B. 当规则发生变化时
例如：

- completion rules 变化
- admission rules 变化
- common-core / extended 规则变化

更新顺序必须是：

1. 先更新对应 `benchmark_spec/*rules*.md`
2. 再更新 `benchmark_spec/decision_log.md`
3. 如有必要，在 `docs/EXECUTION_STATUS.md` 用一句话回写“当前规则已调整”
4. 不直接改 `PROJECT_PLAN.md`，除非长期方向也变了

#### C. 当长期方向或范围发生变化时
例如：

- v1 范围变化
- track 改变
- taxonomy 主框架改变
- milestone 改变

更新顺序必须是：

1. 更新 `PROJECT_PLAN.md`
2. 更新 `decision_log.md`
3. 如有必要，同步调整 `DOC_MAP.md`
4. `EXECUTION_STATUS.md` 只做一句话说明，不承担长期协议正文

### 16.6 冲突处理规则

若四文件之间出现口径冲突，按以下优先级处理：

1. case 级事实冲突：`inventory/case_registry.csv` 优先
2. 当前阶段 / 当前 focus 冲突：`docs/EXECUTION_STATUS.md` 优先
3. 长期范围 / 长期方向冲突：`PROJECT_PLAN.md` + `decision_log.md` 优先
4. 文件职责或放置位置冲突：`DOC_MAP.md` 优先

---

## 17. 一句话规则

如果一个新文件：

- 不能成为长期稳定 source of truth
- 不能成为明确规则入口
- 不能成为唯一状态入口
- 不能成为 registry

那么它就不应该直接变成正式文档，  
而应先进入 scratch，等待后续决定是否转正。