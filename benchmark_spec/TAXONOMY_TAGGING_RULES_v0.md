# TAXONOMY_TAGGING_RULES_v0.md

## 1. 文档目的

本文件定义 **case-level taxonomy annotation contract**。  
它不重写 taxonomy 词表本体；taxonomy 的正式定义仍以 `taxonomy/*.yaml` 为准。  
本文件回答：

- taxonomy 如何用于 case 审核
- 哪些标签是必打 / 条件打 / 暂不打
- primary / secondary 的使用规则
- 标签数量控制
- 证据来源与继承规则
- 人工审核与 ChatGPT/Codex 辅助的边界

---

## 2. 分层原则

### 2.1 taxonomy 定义层
- `taxonomy/sql_feature_taxonomy_v0.3.yaml`
- `taxonomy/plan_operator_taxonomy_v0.3.yaml`
- `taxonomy/workload_realism_taxonomy_v0.3.yaml`
- `taxonomy/portability_taxonomy_v0.3.yaml`
- `taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml`

职责：
- 定义允许使用的标签
- 定义标签含义、例子、适用对象、支持引擎、提示信息

### 2.2 case-level annotation 层
建议落在 case-local `manifest.yaml` 的 tag block 中。  
职责：
- 记录某个 case 实际被赋予了哪些标签
- 记录 primary / secondary / confirmed / suspected 等 case-level 结果

### 2.3 registry 层
`inventory/case_registry.csv` 仍然只维护 live facts。  
职责：
- 成熟度、已验证引擎、下一步缺口、当前 benchmark line 等实时事实

约束：
- 不将完整 taxonomy 标签列表直接塞入 registry
- taxonomy 标签本体不以 registry 作为 source of truth

---

## 3. case-level 标签落点建议

建议在 case-local `manifest.yaml` 中使用如下结构：

```yaml
tags:
  sql_feature:
    primary: []
    secondary: []
  rewrite_opportunity:
    primary: []
    secondary: []
  plan_operator:
    present: []
    delta_relevant: []
  workload_realism:
    source_inherited: []
    case_specific: []
  portability:
    confirmed: []
    suspected: []
```

说明：
- 这是 case-level annotation 结构，不是 taxonomy 词表结构
- 若某一层当前不适用，可留空列表
- `suspected` 只作为人工审核辅助，不应直接用于正式 benchmark 统计

---

## 4. 必打 / 条件打 / 暂不打

### 4.1 必打
以下两类标签对每个进入正式 case package 的 case 都必须打：

1. `sql_feature`
2. `rewrite_opportunity`

原因：
- `sql_feature` 支撑 coverage map 与结构去重
- `rewrite_opportunity` 支撑 rewrite benchmark 的任务解释

### 4.2 条件打
以下标签仅在有充分证据时打：

1. `plan_operator`
   - 前提：已有 `runs/pg/plans/*` 或等价可审阅计划 artifact
2. `workload_realism`
   - 前提：存在来源、query shape、generator 语义或人工 gap-fill 证据
3. `portability`
   - 前提：存在 SQL 表面风险或已观察到的跨引擎差异风险

### 4.3 暂不强制
以下内容不作为当前 taxonomy backfill 的硬门槛：

- canonical AST / logical IR 级细粒度标签
- SQL span → logical operator → physical node 的节点映射标签
- node-level benefit attribution 标签

这些属于更高阶的 observability / release-grade 层，不在本轮 taxonomy backfill 中强制要求。

---

## 5. 标签数量控制

### 5.1 `sql_feature`
- 一般建议总标签数：1–5
- `primary`：1–3 个
- `secondary`：0–2 个

原则：
- 优先保留高信号结构
- 不为穷举而把所有琐碎 construct 都打上

### 5.2 `rewrite_opportunity`
- `primary`：必须且仅 1 个
- `secondary`：0–2 个

原则：
- 一个 case 必须能回答“它最主要为什么值得做 rewrite benchmark”
- 如果 `primary` 选不出来，说明 case 设计还不够聚焦

### 5.3 `plan_operator`
- `present`：记录 source/rewrite 任一计划中出现过的 canonical operator families
- `delta_relevant`：记录与 rewrite 变化显著相关的 operator families
- `delta_relevant` 建议不超过 3 个

### 5.4 `workload_realism`
- `source_inherited`：0–3 个
- `case_specific`：0–2 个

原则：
- 先继承 source-level realism
- 再谨慎补 case-specific realism

### 5.5 `portability`
- `confirmed`：0–3 个
- `suspected`：0–2 个

原则：
- `confirmed` 必须有明确证据
- `suspected` 仅作为后续跨引擎补跑提示，不直接用于正式统计

---

## 6. 证据来源规则

### 6.1 `sql_feature`
主要证据：
- `source.sql`
- 必要时对照 raw SQL provenance

判定原则：
- 只根据 SQL 文本与结构证据打
- 不根据“感觉上很复杂”打

### 6.2 `rewrite_opportunity`
主要证据：
- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`

判定原则：
- 回答“这个 case 为什么值得做 rewrite benchmark”
- 至少选出 1 个 primary

### 6.3 `plan_operator`
主要证据：
- `runs/pg/plans/source.json`
- `runs/pg/plans/rewrite_pos_01.json`
- `runs/pg/plans/rewrite_neg_01.json`
- `runs/pg/plans/plan_check.json`

判定原则：
- 没有计划 artifact 就不打
- 先记录 coarse canonical operator family
- 不在本轮强行做节点级归因标签

### 6.4 `workload_realism`
主要证据：
- `manifest.yaml`
- `provenance/raw_record.json`
- `provenance/dsqgen_command.txt`
- `provenance/provenance_notes.txt`
- query shape 本身（长度、join 数、nesting、表达式密度等）

判定原则：
- 优先 source-level
- case-level 需高置信补充

### 6.5 `portability`
主要证据：
- SQL 文本中的函数、类型、NULL、日期时间、limit/fetch、grouping feature、join syntax 等风险面
- 已观察到的跨引擎差异（若有）

判定原则：
- 不把“复杂”误当 portability 风险
- 必须指出风险来自哪里

---

## 7. source-level 与 case-level 继承规则

### 7.1 `workload_realism`
允许从 source 继承到 case：
- `classic_analytical_baseline`
- `dynamic_workload_characteristic`
- `real_data_correlation`
- `realistic_query_style`
- `manual_gap_fill_realism`

但若某个 case 明显不体现该 realism，可人工去除继承标签。

### 7.2 `sql_feature`
不从 source 继承。  
必须按 case 的实际 SQL 文本打。

### 7.3 `rewrite_opportunity`
不从 source 继承。  
必须按 case 的 source/rewrite 组合单独判断。

### 7.4 `plan_operator`
不从 source 继承。  
必须按 case 的实际 plan artifacts 判断。

### 7.5 `portability`
不做自动继承。  
只能由 SQL 风险证据或跨引擎观察结果支持后再标注。

---

## 8. 人工审核流程

### Step 0：准备材料
至少应具备：
- `manifest.yaml`
- `source.sql`
- `rewrite_pos_01.sql`
- `rewrite_neg_01.sql`
- `runs/pg/result_check.json`

若要打 `plan_operator`，还需具备：
- `runs/pg/plans/*`

### Step 1：身份与 provenance 核对
确认：
- case_id 清晰
- source family 清晰
- raw provenance 完整
- source_detail 可追溯
- 无 provenance 冲突

### Step 2：`sql_feature`
回答：
- SQL 本身长什么样？

输出：
- `sql_feature.primary`
- `sql_feature.secondary`

### Step 3：`rewrite_opportunity`
回答：
- 这个 case 为什么值得进行 rewrite 评测？

输出：
- `rewrite_opportunity.primary`
- `rewrite_opportunity.secondary`

### Step 4：`plan_operator`（若已有 plan）
回答：
- 计划里发生了什么？

输出：
- `plan_operator.present`
- `plan_operator.delta_relevant`

### Step 5：`workload_realism`
回答：
- 这个 case 为什么像真实 workload，而不是只是语法练习题？

输出：
- `workload_realism.source_inherited`
- `workload_realism.case_specific`

### Step 6：`portability`
回答：
- 跨引擎最可能在哪出问题？

输出：
- `portability.confirmed`
- `portability.suspected`

### Step 7：最终人工拍板
强制确认四项：
1. primary sql_feature
2. primary rewrite_opportunity
3. 是否具备 `plan_operator` 标签条件
4. 是否存在明显 portability risk

若这四项答不出来，则该 case 不应直接进入正式标签回填阶段。

---

## 9. ChatGPT / Codex 辅助边界

### 9.1 ChatGPT 可以辅助
- 读取 case 包核心材料
- 生成候选标签草单
- 给出每个候选标签的证据说明
- 指出歧义点与漏标点
- 帮助整理人工审核记录

### 9.2 Codex 可以辅助
- 批量检查标签名是否存在于 taxonomy 词表
- 检查 case-local tag block 是否格式正确
- 批量回填已人工确认的标签
- 生成 coverage summary / gap report / consistency check

### 9.3 不应让 ChatGPT / Codex 独立决定
- taxonomy 原则变更
- 最终标签裁定
- ground-truth 等价性判断
- admission / promotion / common-core / extended 判断

---

## 10. 歧义处理规则

若出现以下情况，默认不硬打标签：

- 证据不足
- 标签边界不清
- 需要 plan 证据但当前没有 plan
- portability 风险只是模糊猜测
- 多个 rewrite-opportunity 都像 primary，但无法区分主次

此时应：
- 在人工审核记录里标注 `ambiguous`
- 暂不正式写回
- 等后续补证据后再决定

---

## 11. 与论文分析的关系

taxonomy 标签最终应服务于以下分析，不是为了“看起来完整”：

- coverage map
- feature bucket density / gap
- benchmark characterization
- ranking shift by bucket
- failure analysis by bucket
- portability risk slicing
- plan-operator delta slicing

因此，正式写回的标签必须尽量：
- 稳定
- 可比较
- 可复验
- 能支持后续统计

---

## 12. 版本说明

本文件定义的是 **v0 tagging rules**，用于与当前 `taxonomy/*_v0.3.yaml` 配套。  
当以下内容发生变化时，应升级版本：

- 必打 / 条件打规则改变
- primary / secondary 规则改变
- case-level tag block 结构改变
- 证据来源规则改变
- 继承规则改变
