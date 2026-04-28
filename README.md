# SQL Rewrite Benchmark

一个面向 **SQL rewriting** 的一致性感知、计划可观测、跨引擎 benchmark 工作区。

本仓库当前固定在三个执行目标上：

- PostgreSQL
- MySQL
- Spark SQL

benchmark 的最小单位不是单条 SQL，而是一个可复验的 **case package**。每个 case package 通常包含 source SQL、positive rewrite、hard negative、schema / witness data、跨引擎验证脚本、result artifacts、plan artifacts、manifest 与审查说明。

---

## 1. 当前项目定位

本项目当前处于：

> **pilot benchmark consolidation with selective deepening and governance hardening**

这意味着仓库已经不是纯 bootstrap，也不是无约束扩展阶段。当前重点是：

- 稳定四池 benchmark 结构
- 强化 case package 工程规范
- 收口 registry / dashboard / review packet 的一致性
- 深化已构造 case 的三引擎 witness validation 与 plan artifacts
- 为后续 benchmark characterization 和论文表格准备结构化证据

当前不应被理解为：

- 已完整发布的 benchmark release
- 已完成所有 workload curation 的最终数据集
- 已完成 baseline comparison 的实验包
- 可以无约束继续新增 workload / source 的开放爬取仓库

---

## 2. 固定范围

### 2.1 引擎 / 方言

v1 / early-pilot 范围固定为：

- Spark SQL
- PostgreSQL
- MySQL

不在当前范围内：

- 新增数据库引擎家族
- engine / dialect hold-out split
- compositional OOD split
- UDF / stored procedure / trigger benchmark
- 无约束 workload curation

### 2.2 四个 formal pools

仓库只维护四个 formal pools：

1. `performance`
2. `longtail`
3. `consistency`
4. `portability`

`manual_seed` 是 source family / curation channel，不是第五个 pool。

---

## 3. 仓库分层与 source of truth

本项目严格区分五层：

| 层级 | 主要文件 | 作用 |
|---|---|---|
| 长期方向 | `docs/PROJECT_PLAN.md` | 研究目标、长期框架、四池策略、指标框架 |
| 当前状态解释 | `docs/EXECUTION_STATUS.md` | 当前阶段、active focus、代表性快照、当前 blockers |
| 冻结决策 | `benchmark_spec/decision_log.md` | 已冻结的范围、规则、关键项目决策 |
| 实时事实 | `inventory/source_registry.csv`, `inventory/case_registry.csv` | source / case 的 live facts |
| 批次审查历史 | `benchmark_spec/reviews/*.md` | 某一批 case 的 review-prep / review-history |

重要规则：

- case 级实时状态以 `inventory/case_registry.csv` 为准。
- source 级实时状态以 `inventory/source_registry.csv` 为准。
- `docs/EXECUTION_STATUS.md` 是 dashboard / interpretation layer，不是完整 registry。
- `benchmark_spec/reviews/*.md` 是 review-history / review-prep，不是 live fact table。
- `docs/PROJECT_PLAN.md` 不记录日常执行进度。

---

## 4. 当前能力概览

当前仓库已经具备：

- 四池 case package 结构
- source-to-case 分离
- registry-first case / source 管理
- PostgreSQL / MySQL / Spark 三引擎执行路径
- case-local witness validation scripts
- result_check / plan_check machine-readable artifacts
- TPC-H / TPC-DS / JOB / IMDB performance review-prep packets
- SQLStorm longtail review-prep packet
- Calcite / VeriEQL consistency line 的初步构造与验证流程
- PARROT portability line 的 admitted external reference case
- taxonomy v0.3 与 case-level tag block 规则

---

## 5. 当前四池状态摘要

> 本节只是 README 级摘要。完整实时事实请看 `inventory/case_registry.csv`。

### 5.1 Performance

Performance line 当前包括：

- TPC-H / TPC-DS derived performance cases
- JOB / IMDB derived performance cases
- tri-engine evidence complete 的多批 performance drafts
- 对应 review-prep packets：
  - `benchmark_spec/reviews/TPCH_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md`
  - `benchmark_spec/reviews/TPCDS_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md`
  - `benchmark_spec/reviews/JOB_IMDB_TRI_ENGINE_PERFORMANCE_REVIEW_v0.md`
  - `benchmark_spec/reviews/PERFORMANCE_TRI_ENGINE_REVIEW_SYNTHESIS_v0.md`

这些 packet 是 review-prep / paper-table planning 层，不自动意味着 admission 或 common-core movement。

### 5.2 Longtail

Longtail line 当前以 SQLStorm / StackOverflow-style query structures 为主，已经形成一批 registry-backed tri-engine draft cases，并有对应 review-prep packet：

- `benchmark_spec/reviews/LONGTAIL_SQLSTORM_TRI_ENGINE_REVIEW_v0.md`

`LONGTAIL_0001` 是 manual / legacy tri-engine anchor。  
`LONGTAIL_0002` 仍是 PG-only / staged registered case。  
后续 SQLStorm 扩展应谨慎；当前低/中风险候选池已经明显收窄。

### 5.3 Consistency

Consistency line 当前包括：

- `CONS_0001` manual correctness anchor
- `CONS_0002` Calcite-derived PG-only draft
- `CONS_0003` / `CONS_0004` VeriEQL / Calcite-subset staged drafts
- 新增 Calcite-derived consistency wave packages

Consistency pool 的核心目标不是性能，而是：

- source 与 positive rewrite 结果一致
- source 与 hard negative 可复现地产生差异
- witness data 能暴露语义边界
- 三引擎执行与计划 artifacts 能支持后续审查

### 5.4 Portability

Portability line 当前包括：

- `PORT_0001` manual / anchor package
- `PORT_0002` PARROT / BIRD-derived admitted external common-core case

Portability pool 的重点是跨方言 / 跨引擎可执行性、一致性与 negative portability failure，而不是单纯 SQL 转译是否成功。

---

## 6. Case package 基本结构

一个较完整的 case package 通常类似：

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  source.sql
  rewrite_pos_01.sql
  rewrite_neg_01.sql
  schema/
    ddl_pg.sql
    ddl_mysql.sql
    ddl_spark.sql
  validation/
    pg_witness_data.sql
    mysql_witness_data.sql
    spark_witness_data.sql
    run_pg_validation.sh
    run_pg_plan_collection.sh
    run_mysql_validation.sh
    run_mysql_plan_collection.sh
    run_spark_validation.sh
    run_spark_plan_collection.sh
  runs/
    pg/
      result_check.json
      plans/plan_check.json
    mysql/
      result_check.json
      plans/plan_check.json
    spark/
      result_check.json
      plans/plan_check.json
  schema_notes.md
  witness_design_notes.md
  risk_notes.md
  promotion_checklist.md
```

并不是所有 legacy case 都已经完全符合这个结构。对于 older anchor / staged packages，应以 registry + current review notes 为准。

---

## 7. Taxonomy

当前使用 5 张 taxonomy v0.3：

- `taxonomy/sql_feature_taxonomy_v0.3.yaml`
- `taxonomy/rewrite_opportunity_taxonomy_v0.3.yaml`
- `taxonomy/plan_operator_taxonomy_v0.3.yaml`
- `taxonomy/workload_realism_taxonomy_v0.3.yaml`
- `taxonomy/portability_taxonomy_v0.3.yaml`

case-level 标签建议写入 `manifest.yaml` 的 `tags` block：

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

标签回填原则：

- `sql_feature` 与 `rewrite_opportunity` 是核心层。
- `plan_operator` 需要真实 plan artifacts 支撑。
- `workload_realism` 优先基于 source provenance 与 query shape。
- `portability` 只在有明确 SQL 风险面或跨引擎证据时标注。
- 不应让 ChatGPT / Codex 独立改变 taxonomy 原则或最终科学判断。

---

## 8. 常用工作流

### 8.1 启动环境

```bash
cd ~/code/sql-rewrite-bench
source .venv/bin/activate

export PGPASSWORD='<local-password>'
source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh
```

### 8.2 环境检查

```bash
python -m scripts.cli env-check
python -m scripts.cli pg-check
python -m scripts.cli mysql-check
python -m scripts.cli spark-check
```

### 8.3 Case validation / plan collection

通常使用 case-local wrappers：

```bash
bash cases/<POOL>/<CASE_ID>/validation/run_pg_validation.sh
bash cases/<POOL>/<CASE_ID>/validation/run_pg_plan_collection.sh

bash cases/<POOL>/<CASE_ID>/validation/run_mysql_validation.sh
bash cases/<POOL>/<CASE_ID>/validation/run_mysql_plan_collection.sh

bash cases/<POOL>/<CASE_ID>/validation/run_spark_validation.sh
bash cases/<POOL>/<CASE_ID>/validation/run_spark_plan_collection.sh
```

批量任务通常放在：

```text
runs/codex_overnight/<batch_name>/
```

其中 runner 通常只负责执行并写 result / plan artifacts，不应自动更新 registry 或提交 commit。

---

## 9. Registry-first 规则

如果 case 状态发生变化，例如：

- 新增 tri-engine witness validation
- 新增 plan artifacts
- package status 变化
- admission / review status 变化
- next_gap 变化

更新顺序应为：

1. 先提交 case-local evidence / files
2. 再更新 `inventory/case_registry.csv`
3. 如影响当前解释，再更新 `docs/EXECUTION_STATUS.md`
4. 如形成批次级审查材料，再更新 `benchmark_spec/reviews/*.md`

不要只更新 narrative 文件而不更新 registry。

---

## 10. Codex / LLM 使用边界

Codex 在本项目中主要承担工程与批处理自动化：

- case package scaffolding
- validation wrapper generation
- batch runner generation
- registry consistency checks
- artifact existence checks
- JSON / YAML validation
- review-prep packet drafting

Codex 不应自行决定：

- benchmark 协议
- taxonomy 原则
- primary metrics
- ground-truth 等价性
- admission / promotion / common-core movement
- 新 workload 是否纳入

对于任何 Codex 任务，建议先做只读审计，再执行边界明确的小任务。

---

## 11. 新同学推荐阅读顺序

如果第一次接触本仓库，建议按顺序阅读：

1. `AGENTS.md`
2. `docs/DOC_MAP.md`
3. `docs/EXECUTION_STATUS.md`
4. `benchmark_spec/decision_log.md`
5. `docs/PROJECT_PLAN.md`
6. `benchmark_spec/benchmark_spec_v0.md`
7. `inventory/case_registry.csv`
8. `inventory/source_registry.csv`
9. `benchmark_spec/reviews/`

如果只想知道“现在做到哪里”，优先看：

```text
docs/EXECUTION_STATUS.md
inventory/case_registry.csv
inventory/source_registry.csv
```

如果只想知道“为什么这样设计”，优先看：

```text
docs/PROJECT_PLAN.md
benchmark_spec/benchmark_spec_v0.md
benchmark_spec/decision_log.md
```

---

## 12. 当前推进建议

当前最合理的推进方式是：

1. 继续收口 consistency / portability 池，而不是继续盲目扩 longtail。
2. 对成功 case 做 case-local evidence commit → registry writeback → dashboard update。
3. 对失败 case 先进入 backlog，除非是明显 wrapper / witness / narrow SQL-compatibility 修复。
4. 在主要池子形成稳定 tri-engine draft set 后，再统一做 taxonomy calibration 与 paper-table characterization。
5. 不要把 review-prep packet 写成 admission 结论。

---

## 13. 一句话总结

本仓库的目标不是收集最多 SQL，而是构建一个可复验、可解释、跨引擎的一致性感知 SQL rewrite benchmark。

当前最重要的纪律是：

> **case package 是最小单位；registry 是 live facts；review packet 是审查历史；dashboard 是解释层；不要混层。**
