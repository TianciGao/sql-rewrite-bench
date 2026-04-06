# Inventory Template
## SQL Rewrite Benchmark Source Inventory 填写规范（v0.1）

## 1. 文档角色

本文件用于定义 `inventory/source_registry.csv` 的填写口径、字段含义、允许取值、更新流程与常见错误处理方式。

本文件的目标不是描述完整 benchmark 研究计划，而是保证 source inventory 在当前仓库中具备：

- 一致的行粒度
- 一致的字段语义
- 一致的填写风格
- 可供后续脚本和人工审阅共同使用的稳定规范

本文件与以下文件的关系如下：

- `docs/PROJECT_PLAN.md`：说明项目总体研究计划与阶段路线
- `benchmark_spec/benchmark_spec_v0.md`：说明当前版本的执行边界
- `benchmark_spec/decision_log.md`：记录冻结决策
- `inventory/source_registry.csv`：实际 source 登记表
- `docs/POOL_MAPPING_RULES.md`：说明四个正式池子的归类规则

---

## 2. 当前阶段适用范围

当前文档适用于：

- Week 2 早期的 source inventory 设计
- source family 登记
- source 到 pool 的预映射
- provenance 与风险标记
- 后续 inventory validator 的实现依据

当前文档 **不** 用于：

- case package 级别字段填写
- benchmark case admission 决策
- 新 benchmark workload 的自动导入
- pool 内部抽样策略
- final benchmark release governance

---

## 3. 一行代表什么

`inventory/source_registry.csv` 中 **一行代表一个 source artifact family**，而不是：

- 一条 SQL
- 一个 case package
- 一个计划文件
- 一个 rewrite 对
- 一个 model output

### 正例
以下对象适合作为一行 source：

- TPC-H
- TPC-DS
- DSB
- JOB
- SQLStorm
- Stack Queries
- Calcite Seeds
- SQLEquiQuest
- PARROT
- Manual Seed Cases

### 反例
以下对象 **不应该** 单独作为 source 行：

- `TPC-H Q3`
- `PERF_0001`
- `rewrite_pos_01.sql`
- `runs/plans/pg/source.json`
- 某一次 LLM 生成结果

### 原因
source inventory 负责管理“来源”，不是管理“最终 case”。  
最终进入 benchmark 的最小单元仍然是 **case package**。

---

## 4. source family 与正式 pool 的区别

### source family
source family 描述“这个来源是什么类型”，例如：

- benchmark
- workload
- rule_suite
- equivalence_benchmark
- translation_seed
- manual_seed

### formal pool
formal pool 描述“最终 case package 进入哪个正式池子”，当前正式池子只有四个：

- performance
- longtail
- consistency
- portability

### 重要说明
`Manual Seed Cases` 是 `manual_seed`，**不是第五个 pool**。  
它是一个来源家族，后续生成的 case package 再根据内容进入四个正式池子之一。

---

## 5. 字段总览

`inventory/source_registry.csv` 当前采用以下字段：

```csv
source_id,source_name,source_family,source_version,owner_or_origin,primary_pool,secondary_pool_or_notes,task_role,expected_use_level,coverage_sql_features,coverage_plan_features,coverage_realism_features,coverage_portability_features,access_type,license_or_terms,acquisition_status,three_engine_fit,provenance_risk,curation_risk,decision_needed,storage_path,notes