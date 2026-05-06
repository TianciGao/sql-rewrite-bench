# RewriteBench

RewriteBench 是一个面向 **SQL rewriting** 的 benchmark 工作区。它的目标不是提出新的 SQL 改写算法，而是建立一套更可靠的评测方法：把“能执行、结果正确、真的发生了改写、是否变快、能否跨引擎迁移”分开测清楚。

一句话概括：

> 传统 workload benchmark 主要问“SQL 跑得快不快”；RewriteBench 问“这次 SQL 改写到底可靠吗？”

当前项目已经进入 **paper-draft evidence packet** 阶段：已有一批可写进论文结果章节的实测证据，但它还不是最终 benchmark release，也不是 final leaderboard。

---

## 1. 为什么做这个项目

SQL rewrite 的评测不能只看平均速度。一个 rewrite 可能：

- 能执行，但结果错了；
- 结果正确，但其实几乎没改原 SQL；
- 在一个小 seed 上很好，但扩展到更多 case 就失败；
- 在 PostgreSQL 能跑，但到 MySQL / Spark 就执行失败；
- 看起来是同一个工具，但不同 route 的风险完全不同。

因此，RewriteBench 把一次 SQL 改写定义为一个可复验的 **case package**，而不是一条孤立 SQL 字符串。

一个 case package 通常包含：

- source SQL；
- positive rewrite；
- hard negative；
- schema / witness data；
- result checker；
- source / rewrite plan artifacts；
- provenance；
- taxonomy tags；
- reporting / claim boundary metadata。

---

## 2. 当前最重要的实验发现

当前最稳的结果不是“某个方法最快”，而是下面六条发现。

### Finding 1：普通 workload / 小 seed 会高估 rewrite-route robustness

`SQLGlot optimize` 在 seed common-core 上是 `9/9`，但扩展到 Batch 2A / 3A / 3B 后持续失败。

这说明：只用小样本或普通 workload，会把方法看得过于乐观；换成 rewrite-specific case package 后，隐藏的能力边界会暴露。

### Finding 2：同一个工具不能按工具名混报

`SQLGlot optimize` 和 `SQLGlot no-opt` 表现完全不同。前者暴露 optimizer-stage capability boundary；后者较稳定，但 speedup 近似中性。

这说明：不能粗略写“SQLGlot 好/坏”。同一个工具内部，不同 route 的风险和意义完全不同。

### Finding 3：checker-consistent rewrite 不等于 speedup

Human positive、SQLGlot no-opt、Direct LLM、Calcite HEP、R-Bot、LearnedRewrite、LLM-R2 都显示：正确或可执行的 rewrite 并不自动带来稳定性能收益。

这说明：RewriteBench 必须先问“结果对不对”，再问“有没有真的变快”。

### Finding 4：必须区分 nontrivial rewrite 和 no-op fallback

LearnedRewrite 在 bounded subset 上 `10/10` checker-consistent，但 `8/10` 是 source-like / no-op。

这说明：一个方法返回几乎没变的 SQL，也可能很容易通过 checker。RewriteBench 会把“正确但没怎么改”和“真正有意义的改写”区分开。

### Finding 5：portability failure 常发生在 checker 之前

MySQL / Spark bounded 子切片显示，很多跨引擎失败不是结果不一致，而是 source / rewrite 在目标引擎上已经无法执行。

这说明：Track C 不能只看最后的 result consistency。很多 portability failure 发生得更早。

### Finding 6：verifier 是 support，不是 rewrite baseline

SQLSolver / VeriEQL 的价值是支持等价性或反例分析，但它们不输出 rewrite，不能进入 speedup leaderboard。

这说明：verifier 应放在 support 表，不应和 rewrite 方法混在同一个速度榜里。

---

## 3. 当前 evidence packet

当前实验结果应理解为 **paper-draft evidence packet**，不是最终发布版本。

README 只提供项目级概览。更细的 live facts 以 `inventory/source_registry.csv`、`inventory/case_registry.csv` 和 `docs/_scratch/BASELINE_EVIDENCE_MATRIX_CURRENT_v1.md` 为准。

| 证据块 | 当前范围 | 当前状态 | 论文口径 |
|---|---:|---|---|
| common-core same-engine evidence | 46 cases | controls、SQLGlot routes、Batch 2A / 3A / 3B 形成核心 evidence | 可作为 paper-facing 主干，但不是 final admission |
| Direct LLM expanded PERF | 34 PERF cases, PG-only | `34/34` execution + checker consistency；GM speedup 约 `1.003` | bounded LLM 对照 |
| Calcite HEP | target 10/10, PG-only | `10/10` checker + speedup；GM speedup 约 `0.944`；witness-scale | bounded deterministic baseline，不作 final leaderboard |
| R-Bot / LearnedRewrite / LLM-R2 | shared 10-case subset | 已有 correctness-gated PG-only speedup slice | 写行为差异，不做最终排名 |
| PORT PG-side | 6 cases | SQLGlot Transpile `6/6`；LLM Translate `6/6` | bounded PG-side portability evidence |
| PORT cross-engine bounded subset | 6-case route packet | `4/6` cross-engine closed：`PORT_0004`、`PORT_0022`、`PORT_0024`、`PORT_0025`；pending：`PORT_0012`、`PORT_0013` | bounded cross-engine execution evidence，不是 full PORT closure |
| SQLSolver / VeriEQL support | SQLSolver 4 pairs；VeriEQL 1-case canary | support evidence exists | 单独 support 表，不进速度榜 |

---

## 4. 最初计划的 baseline 分层

RewriteBench 的 baseline 不是一张混合大榜，而是分成四类。

### 表 A：控制组 / 参照组

| 方法 | 用途 | 是否进主排行榜 |
|---|---|---|
| Native / Original SQL | 原 SQL，不改写，作为所有 speedup 的分母 | 否 |
| Human positive rewrite | 人工正确 rewrite，作为 reference / sanity check | 否，最多作为参考行 |
| Hard negative guard | 测 checker 能否拒绝错误 rewrite | 否，只进 correctness 表 |

这三项必须跑，但它们不是“别人算法”。

### 表 B：same-engine rewrite

| 方法 | 当前论文定位 | 备注 |
|---|---|---|
| SQLGlot optimize | 工具型规则 baseline | 暴露最强 capability-boundary finding |
| SQLGlot no-opt | separate baseline candidate | 不替代 optimize；更稳但 near-neutral |
| Calcite HEP rules | bounded deterministic baseline | 已有 10/10 PG-only evidence |
| LearnedRewrite | bounded prior-method evidence | 重点暴露 no-op / source-like fallback |
| R-Bot / LLM4Rewrite | bounded prior-method evidence | 暴露 semantic drift / path failure 风险 |
| LLM-R2 | bounded prior-method evidence | 暴露 adapter / extraction / logical-plan fragility |
| Direct LLM rewrite | LLM 对照 | 不是 prior algorithm，是简单 LLM baseline |

主指标包括：

```text
ExecutableRate
ResultConsistencyRate
GM_Speedup
RegressionRate@20%
Win/Tie/Loss
```

性能只在 **result-consistent** 的 rewrite 上算。项目原则是：一致性优先于速度；结果不一致，即使更快，也不能算有效正例。

### 表 C：portability / cross-dialect

| 方法 | 用途 | 是否进 portability 表 |
|---|---|---|
| SQLGlot Transpile | 工具型跨方言 baseline | 是 |
| LLM Translate | 简单 LLM translation baseline | 是 |
| adapted rewrite methods | 若能适配跨方言任务，可作为扩展 | 视实现而定 |

这里不要只看 parser success，要看：

```text
CrossEngineExecutableRate
CrossEngineConsistencyRate
SpeedupTransferRate
```

当前 PORT 路线的状态是：

- bounded PG-side route subset = `6`
- bounded cross-engine closed subset = `4/6`
- closed = `PORT_0004`, `PORT_0022`, `PORT_0024`, `PORT_0025`
- pending = `PORT_0012`, `PORT_0013`
- `SpeedupTransferRate = not_computed`

因此这里仍然不能宣称 full cross-engine closure，也不能宣称 transfer metric readiness。

### 表 D：verifier / support

| 方法 | 用途 | 是否进速度榜 |
|---|---|---|
| SQLSolver | 等价性验证支持率 | 否 |
| VeriEQL | bounded / equivalence support | 否 |

这里只报：

```text
VerifierSupportRate
ProveRate
RefuteRate
UnknownRate
TimeoutRate
```

它们不是 rewrite 算法，不要和 rewrite methods 放在同一个速度榜里。

---

## 5. 当前完成度（内部 / provisional）

| 维度 | 当前成熟度 | 判断 |
|---|---|---|
| Benchmark 设计 / 协议 / case package / taxonomy 框架 | high | 核心结构成立，剩余是 polish 与统一口径 |
| paper-draft evidence packet | high | 已有 same-engine、PORT、prior-method、support 多类 evidence |
| same-engine PG bounded experiments | medium-high | 主要 routes 已跑；但不是 final leaderboard |
| prior-method bounded evidence | medium | R-Bot / LearnedRewrite / LLM-R2 有 speedup；仍是 bounded subset |
| portability / cross-engine | medium | PG-side route packet已闭合 `6/6`，但 cross-engine 只闭合 `4/6` |
| verifier / support | medium-low | SQLSolver 4-pair、VeriEQL canary；支持表不完整 |
| plan observability / attribution | medium-low | plan artifacts 有；attribution 没有 |
| 论文写作 | medium | 框架有，结果章节 / 摘要 / 结论需要按新实验重写 |
| VLDB EA&B 投稿准备整体 | medium | 已有论文级 finding，但不是 submission-ready |
| release-grade artifact | medium-low | artifact 分散，需要统一 artifact map 与复现说明 |

---

## 6. 当前不能夸大的地方

可以说：

- 当前实验已经形成 route-aware、correctness-gated、portability-layered 的 bounded evidence packet。
- RewriteBench 揭示了 seed-only / workload-only evaluation 容易隐藏的 route failure、no-op fallback、semantic drift、adapter fragility 和 portability execution blockers。
- 正确 rewrite 不自动等于 speedup；speedup 必须在 checker-consistent rewrite 上计算。
- SQLSolver / VeriEQL 是 support evidence，不是 rewrite speed baseline。
- Calcite HEP 目前是 `10/10` PG-only checker+speedup measured baseline，但仍是 witness-scale、same-engine、non-leaderboard evidence。
- PORT 当前是 bounded route packet：PG-side `6/6` 已闭合，cross-engine `4/6` 已闭合，但不是 full PORT closure。

不能说：

- 完成了 final leaderboard；
- 完成了 full prior-method coverage；
- 完成了 full cross-engine closure；
- 已经计算 SpeedupTransferRate；
- 已经完成 full PORT closure；
- 已经拿到 production-scale speedup 结论；
- 完成了完整 verifier support 表；
- 完成了完整 plan attribution。

---

## 7. 仓库范围

当前固定在三个执行目标上：

- PostgreSQL
- MySQL
- Spark SQL

v1 / pilot 阶段不做：

- 新增数据库引擎家族；
- engine / dialect hold-out split；
- compositional OOD split；
- UDF / stored procedure / trigger benchmark；
- 无约束 workload curation。

---

## 8. 四个 formal pools

仓库维护四个 formal pools：

1. `performance`
2. `longtail`
3. `consistency`
4. `portability`

它们的作用分别是：

| Pool | 作用 |
|---|---|
| performance | 经典分析型性能主线，主要用于 correctness-gated speedup 和工具/方法对照 |
| longtail | 覆盖模板 benchmark 不常见的复杂结构和真实风格 SQL |
| consistency | 把 semantic correctness、positive / negative、witness checker 作为正式任务 |
| portability | 测跨方言 / 跨引擎 rewrite 的可执行性、一致性与迁移风险 |

---

## 9. Case package 基本结构

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
    checker.yaml
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
    result_check.json
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

不是所有 legacy case 都已经完全符合这个结构。older anchor / staged packages 应以 registry、case-local artifacts 和 current review notes 为准。

---

## 10. Taxonomy

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

基本原则：

- `sql_feature` 与 `rewrite_opportunity` 是核心层；
- `plan_operator` 需要真实 plan artifacts 支撑；
- `workload_realism` 基于 source provenance 与 query shape；
- `portability` 只在有明确 SQL 风险面或跨引擎证据时标注；
- ChatGPT / Codex 可以辅助整理，但不能独立改变 taxonomy 原则或最终科学判断。

---

## 11. 仓库分层与 source of truth

本项目严格区分五层：

| 层级 | 主要文件 | 作用 |
|---|---|---|
| 长期方向 | `docs/PROJECT_PLAN.md` | 研究目标、长期框架、四池策略、指标框架 |
| 当前状态解释 | `docs/EXECUTION_STATUS.md` | 当前阶段、active focus、代表性快照、当前 blockers |
| 冻结决策 | `benchmark_spec/decision_log.md` | 已冻结的范围、规则、关键项目决策 |
| 实时事实 | `inventory/source_registry.csv`, `inventory/case_registry.csv` | source / case 的 live facts |
| 批次审查历史 | `benchmark_spec/reviews/*.md` | 某一批 case 的 review-prep / review-history |

重要规则：

- case 级实时状态以 `inventory/case_registry.csv` 为准；
- source 级实时状态以 `inventory/source_registry.csv` 为准；
- `docs/EXECUTION_STATUS.md` 是 dashboard / interpretation layer，不是完整 registry；
- `benchmark_spec/reviews/*.md` 是 review-history / review-prep，不是 live fact table；
- `docs/PROJECT_PLAN.md` 不记录日常执行进度。

---

## 12. 常用工作流

### 12.1 启动环境

```bash
cd ~/code/sql-rewrite-bench
source .venv/bin/activate

export PGPASSWORD='<local-password>'
source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh
```

### 12.2 环境检查

```bash
python -m scripts.cli env-check
python -m scripts.cli pg-check
python -m scripts.cli mysql-check
python -m scripts.cli spark-check
```

### 12.3 Case validation / plan collection

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

runner 通常只负责执行并写 result / plan artifacts，不应自动更新 registry 或提交 commit。

---

## 13. Registry-first 规则

如果 case 状态发生变化，例如：

- 新增 witness validation；
- 新增 plan artifacts；
- package status 变化；
- admission / review status 变化；
- next_gap 变化。

更新顺序应为：

1. 先提交 case-local evidence / files；
2. 再更新 `inventory/case_registry.csv`；
3. 如影响当前解释，再更新 `docs/EXECUTION_STATUS.md`；
4. 如形成批次级审查材料，再更新 `benchmark_spec/reviews/*.md`。

不要只更新 narrative 文件而不更新 registry。

---

## 14. Codex / LLM 使用边界

Codex 在本项目中主要承担工程与批处理自动化：

- case package scaffolding；
- validation wrapper generation；
- batch runner generation；
- registry consistency checks；
- artifact existence checks；
- JSON / YAML validation；
- review-prep packet drafting。

Codex 不应自行决定：

- benchmark 协议；
- taxonomy 原则；
- primary metrics；
- ground-truth 等价性；
- admission / promotion / common-core movement；
- 新 workload 是否纳入。

对于任何 Codex 任务，建议先做只读审计，再执行边界明确的小任务。

---

## 15. 新同学推荐阅读顺序

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

## 16. 下一步建议

当前不建议继续盲目扩实验。现在更重要的是：

1. 先推进 `PORT_0012` / `PORT_0013` 的 MySQL/Spark closure preflight 与执行准备；
2. 在 PORT 状态继续变化后回写 baseline evidence matrix；
3. 再统一结果口径，命名为 `paper-draft v1.2 evidence packet`；
4. 重写论文 Results；
5. 更新摘要、结论和 limitations；
6. 生成 artifact map，让每张 paper table 能追溯到具体 scratch/report 文件。

---

## 17. 一句话总结

RewriteBench 的目标不是收集最多 SQL，也不是证明某个方法最快。

它的目标是构建一个可复验、可解释、跨引擎、以一致性为第一门槛的 SQL rewrite benchmark。

当前最重要的纪律是：

> **case package 是最小单位；registry 是 live facts；review packet 是审查历史；dashboard 是解释层；不要混层。**
