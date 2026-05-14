# SQL-RewriteBench

SQL-RewriteBench 是一个面向 **语句级 SQL 重写（statement-level SQL rewrite）** 的 benchmark 与 artifact 工作区。它的目标是建立一套能被复验、能解释失败、能区分任务角色的 SQL rewrite 评测协议。

概括：

> 传统 workload benchmark 多问“SQL 跑得快不快”；SQL-RewriteBench 先问“这次 SQL 改写是否可执行、是否语义一致、是否真的发生了有意义的改写、失败能否被诊断、跨引擎是否仍然成立”，然后才解释速度。

---

## 1. 项目当前定位

当前仓库应理解为一个 **paper-facing benchmark artifact**，而不是最终全量 release，也不是 final ranked leaderboard。

它已经具备：

- case-package 契约：source SQL、positive rewrite、hard negative、schema/data context、checker path、plan/failure artifacts、provenance、taxonomy tags；
- 角色感知评估：control、same-engine rewrite、portability transfer、observability support、verifier support 分开报告；
- 分母感知指标：planned、generated/ready、executed、exact、timed 明确区分；
- Common-core v0 evidence packet：40 个 case，Track A 同引擎展开为 120 rows；
- Table 12 静态再生成脚本和 reviewer artifact-mode smoke 复现入口。

当前不能声称：

- final global leaderboard；
- full PORT9 / full registry portability closure；
- SpeedupTransferRate 已计算；
- denominator-wide NodeAlignmentCoverage 已完成；
- SQLSolver / VeriEQL 是 rewrite baseline；
- 所有 prior methods 都已达到 120-row denominator。

---

## 2. Common-core v0 分母

当前论文结果使用的 Common-core v0 分母为：

```text
40 cases × 3 same-engine targets = 120 rows
engines = PostgreSQL / MySQL / Spark
```

四个 pool 的冻结组成如下：

| Pool | Cases | Same-engine rows | 主要压力 | 论文作用 |
|---|---:|---:|---|---|
| PERF | 16 | 48 | 分析型 SQL、性能敏感 rewrite、predicate / aggregation / join pressure | correctness-gated speedup、性能退化、方法对照 |
| CONS | 9 | 27 | NULL、聚合、重复、多重性、hard negative、semantic boundary | correctness、false accept risk、checker guard |
| PORT | 9 | 27 | 方言差异、函数/类型/日期/引用风险 | cross-engine execution / consistency |
| LONGTAIL | 6 | 18 | 真实风格、复杂结构、长尾 SQL | robustness、failure diagnosis、结构覆盖 |
| Total | 40 | 120 | 全部 | Track A 主分母 |

这个分母不是生产 SQL 的频率样本，而是一个 **受控覆盖面（controlled coverage surface）**。它的作用是暴露 rewrite-specific failure modes，而不是模拟真实 workload 中每类 SQL 出现的概率。

Common-core v0 的 40 个 case：

```text
PERF:
  PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019,
  PERF_0024, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054,
  PERF_0056, PERF_0062, PERF_0077, PERF_0082

CONS:
  CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012,
  CONS_0024, CONS_0036, CONS_0037

PORT:
  PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013,
  PORT_0022, PORT_0024, PORT_0025

LONGTAIL:
  LONGTAIL_0011, LONGTAIL_0012, LONGTAIL_0013,
  LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024
```

边界：这个列表只冻结 case denominator，不意味着每个方法都对 120 rows 具有完整生成、执行、一致性和计时覆盖。

---

## 3. 为什么不是排行榜

SQL-RewriteBench 的结果表不是把所有方法压成一个全局分数。原因是不同方法和 route 的任务角色、分母、引擎范围、输出契约和 timing eligibility 不同。

例如：

- `Direct LLM original` 是 tri-engine same-engine rewrite route；
- `Direct LLM + Repair-1` 是 execution-feedback route，timing 是 mixed-source，不能和 original route 合并；
- `SQLGlot optimize` 是 deterministic optimize route；
- `SQLGlot no-op` 是 parse/emit 或 low-transform control route，不代表 optimizer 能力；
- `Calcite HEP` 是 fail-closed rule-based correctness / timing packet；
- `R-Bot` 是 mixed 120 generation + PG15 bounded timing evidence；
- `LLM-R2` / `LearnedRewrite` 是 bounded prior-method appendix evidence；
- `SQLGlot Transpile` / `LLM Translate` 属于 Track C portability，不进入 Track A same-engine speedup table；
- `SQLSolver` / `VeriEQL` 是 verifier support，不生成 rewrite，不能进入 speedup leaderboard。

因此，本文的主表应读作：

> **denominator-aware method evidence ledger**

而不是：

> final leaderboard

只有当方法共享同一 denominator、同一 task track、同一 engine scope、同一 route policy、同一 checker、同一 failure accounting、同一 timing denominator 或明确的 full-denominator timing policy 时，才可以做 ranked leaderboard。当前阶段不满足这一条件。

---

## 4. 当前核心实验结果

### 4.1 Table 12：Common-core v0 denominator-aware method evidence ledger

Table 12 是当前最重要的总表。它把不同 scope 的方法/route 放在同一张 evidence ledger 里，但不排序、不命名 winner。

| 方法 / route | Scope | Planned | Generated / Ready | Executed | Exact | Timed | GM | Regression@20 | Placement |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| Direct LLM original | tri-engine same-engine | 120 | 120 generated；115 ready | 99 | 94 | 94 | 1.0436 | 3.19% | main same-engine evidence |
| Direct LLM + Repair-1 | tri-engine feedback route | 120 | 120 generated；5 preflight-blocked | 97 | 96 | 96 | 1.0431 | 4.17% | route-level evidence；mixed-source timing |
| SQLGlot optimize | tri-engine route | 120 | 120 attempted；75 generated | 65 | 63 | 63 | 0.9907 | 1.59% | revised exact63 route |
| SQLGlot no-op | tri-engine route | 120 | 120 attempted；78 generated | 72 | 72 | 72 | 1.0001 | 1.39% | no-op / low-transform route |
| Calcite HEP fail-closed | tri-engine fail-closed route | 120 | retained route artifacts | 95 | 93 | 93 | 0.9959 | 7.53% | correctness-gated timing packet |
| R-Bot | mixed scope | formal 120 generation | PG-scoped subsets | 15 PG-only | 15 PG-only | 15 | 0.9218 | 20.00% | bounded / mixed appendix |
| LLM-R2 original | PG-only bounded | 9 | 9 | 3 exact + 6 execution failed | 3 | 0 | NA | NA | bounded appendix |
| LLM-R2 recovered | PG9 recovery audit | 9 | 9 | 6 | 6 | 0 | NA | NA | PG6 exact recovered subset |
| LearnedRewrite | PG10 bounded | 10 | 10 | NA_not_retained | 10 checker-consistent | NA | NA | NA | bounded appendix；8 source-like/no-op |

### 4.2 论文支撑的主要结论

当前 evidence packet 支撑以下结论：

1. **SQL rewrite 评测必须保留 planned → generated → executed → exact → timed 分母链。** 只看生成成功或执行成功子集会高估方法质量。
2. **Hard-negative guardrail 是必要的。** 当前 120 planned hard-negative cells 中，111 tested，9 not applicable；111 个 tested cells 均为 executable semantic mismatch 且全部被 checker 拒绝，false accepts = 0。
3. **正确性是速度解释的前提，但不是速度收益的保证。** 多个 exact timed slices 接近中性或仍存在 regression。
4. **No-op / source-like 输出必须单独暴露。** 正确但几乎未改写的 SQL 不能计入有效 rewrite utility。
5. **跨引擎 execution / consistency closure 不等于 SpeedupTransferRate。** 当前 bounded PORT6 只能支持有限语义可移植性证据；迁移加速仍缺少 paired target-engine timing。
6. **Verifier 是 support evidence，不是 rewrite-generation baseline。** SQLSolver / VeriEQL 不输出优化后的 SQL，不能参与 speedup ranking。

---

## 5. 仓库结构

推荐从以下目录理解仓库：

```text
cases/                                  # case packages
reports/evaluation/common_core_v0/       # Common-core v0 retained evidence and regenerated tables
reports/evaluation/common_core_v0/scripts/ # paper-table renderers
scripts/                                # reviewer-facing reproduction entrypoints
inventory/                              # source / case registry
benchmark_spec/                         # benchmark rules, decision log, review records
docs/                                   # project plan, execution status, documentation
```

当前 reviewer-facing 复现最关键的脚本是：

```text
scripts/reproduce_common_core_v0.sh
reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py
```

---

## 6. 快速复现：不跑数据库、不跑 LLM 的 artifact smoke

如果只是审稿人或新同学想确认 Table 12 和 retained artifact 是否一致，先跑 artifact mode：

```bash
bash scripts/reproduce_common_core_v0.sh --mode artifact
```

该模式会检查 retained evidence 目录，重新运行 Table 12 static renderer，并确认 static recompute mismatch 中没有 conflict / missing-input rows。

它不会运行：

```text
DB engines
LLM / model calls
verifier tools
PORT9
EXPLAIN collection
new timing collection
```

期望看到类似输出：

```text
PASS table12_renderer_check: Table 12 regenerated successfully
PASS static_recompute_mismatches_empty: 0 conflict or missing-input rows
PASS table12_diff_summary: cells_compared=90; exact_match=55; expected_NA_match=8; artifact_boundary_match=27; conflicts=0; missing_input=0
Reviewer reproduction artifact-mode passed.
```

---

## 7. 快速复现：Table 12 直接再生成

只看 Table 12 renderer：

```bash
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

期望输出：

```text
rows rendered: 9
cells compared: 90
exact matches: 55
rounded matches: 0
expected NA matches: 8
artifact boundary matches: 27
conflicts: 0
```

查看生成后的 Markdown 表：

```bash
sed -n '1,120p' \
  reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
```

生成文件：

```text
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.csv
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_diff_v1.csv
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_readme_v1.md
```

---

## 8. 完整复现通道：deterministic runners → speedup summary → Table 12

本节是当前最完整的 reviewer / maintainer 复现路线。它分成三层：

1. 重新执行 deterministic runners；
2. 重新用公式计算 speedup summary；
3. 重新生成 Table 12。

### 8.1 先做 deterministic preflight

不执行 runner，只检查命令注册和本地工具是否存在：

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight
```

只检查 Table 12 step：

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run --steps table12
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight --steps table12
```

期望看到：

```text
preflight_pass table12: runner and required local tools found
```

### 8.2 重跑 deterministic runners

> 注意：这些命令可能运行数据库、EXPLAIN、timing 或本地 retained timing runners。运行前请确认 PostgreSQL / MySQL / Spark 环境、数据和权限已配置。默认不应触发 LLM/API 调用；LLM 新调用应使用单独的、显式的 LLM mode 或人工流程。

```bash
# 1. hard-negative guardrail
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps hard-negative

# 2. SQLGlot same-engine routes
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps sqlglot

# 3. Calcite HEP fail-closed route
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps calcite

# 4. selected PostgreSQL plan observability frontier
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps pg-plan

# 5. Direct LLM retained timing route
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps direct-llm-timing-retained

# 6. R-Bot PG15 retained timing route
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps rbot-pg15-timing
```

如需不中断地跑一组 steps，可以视脚本支持情况使用：

```bash
bash scripts/reproduce_common_core_v0.sh \
  --mode deterministic \
  --execute \
  --continue-on-error \
  --steps hard-negative,sqlglot,calcite,pg-plan,direct-llm-timing-retained,rbot-pg15-timing
```

### 8.3 重新生成 speedup summary

Table 12 的 `Timed / GM / Regression@20` 不应手工填。它的核心数据流是：

```text
method_timing_case_level_v1.csv / timing_event_long.csv
        ↓
render_speedup_slice_summary_v1.py
        ↓
speedup_slice_summary_regenerated_v1.csv
        ↓
render_table12_method_evidence_ledger_v1.py
        ↓
Table 12 的 Timed / GM / Regression@20
```

重新用公式计算 speedup summary：

```bash
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check
```

主要输入包括：

```text
reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/method_timing_case_level_v1.csv
reports/evaluation/common_core_v0/runs/*/timing_event_long.csv
```

主要输出：

```text
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regenerated_v1.csv
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_diff_v1.csv
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/speedup_slice_summary_regeneration_readme_v1.md
```

期望看到：

```text
0 conflicts
0 missing inputs
```

### 8.4 重新生成完整 Table 12

```bash
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

查看 Table 12：

```bash
sed -n '1,120p' \
  reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
```

### 8.5 一键式推荐顺序

```bash
# 0. artifact smoke，不跑 DB/LLM/verifier/EXPLAIN/new timing
bash scripts/reproduce_common_core_v0.sh --mode artifact

# 1. deterministic preflight
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight

# 2. 重跑 deterministic runners
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps hard-negative
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps sqlglot
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps calcite
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps pg-plan
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps direct-llm-timing-retained
bash scripts/reproduce_common_core_v0.sh --mode deterministic --execute --steps rbot-pg15-timing

# 3. 重新用公式计算 speedup summary
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check

# 4. 重新生成完整 Table 12
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check

# 5. 查看 Table 12 输出
sed -n '1,120p' \
  reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
```

---

## 9. 复现输出如何验收

### 9.1 Table 12 renderer 验收

通过条件：

```text
rows rendered: 9
cells compared: 90
conflicts: 0
```

推荐记录更完整的 diff summary：

```text
exact matches: 55
rounded matches: 0
expected NA matches: 8
artifact boundary matches: 27
conflicts: 0
missing_input: 0
```

### 9.2 Artifact mode 验收

通过条件：

```text
Reviewer reproduction artifact-mode passed.
```

并且确认：

```text
PASS static_recompute_mismatches_empty
PASS expected_na_boundaries_present
PASS table12_diff_summary
```

### 9.3 deterministic table12 preflight 验收

通过条件：

```text
preflight_pass table12: runner and required local tools found
```

### 9.4 Git 提交前安全检查

运行复现脚本后，`REVIEWER_REPRODUCTION_V1` 下的 log/status 文件可能被刷新。提交前应确认是否需要恢复这些本机日志：

```bash
git status -sb

git restore reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1

git diff --check
```

不要误提交：

```text
reports/evaluation/common_core_v0/runs/...
大量 timing.json
大量 stdout/stderr.log
pg_plan_attribution workspaces
```

可以用下面命令检查 staged 内容：

```bash
git diff --cached --name-only | grep '^reports/evaluation/common_core_v0/runs/' \
  && echo "BAD: runs files staged" \
  || echo "OK: no runs files staged"

git diff --cached --name-only | grep -E '^(inventory/|benchmark_spec/|docs/EXECUTION_STATUS.md)$' \
  && echo "BAD: source-of-truth file staged" \
  || echo "OK: no registry/protocol/status files staged"
```

---

## 10. 关键文件说明

### 10.1 Table 12 provenance 与 regeneration

```text
reports/evaluation/common_core_v0/17_TABLE12_ULTIMATE_PROVENANCE_V1/
  table12_cell_provenance_v1.csv
  table12_artifact_dependency_graph_v1.csv
  table12_generator_script_audit_v1.csv
  table12_formula_source_map_v1.csv
  table12_provenance_summary_v1.md
  table12_provenance_readme_v1.md

reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/
  table12_method_evidence_ledger_regenerated_v1.csv
  table12_method_evidence_ledger_regenerated_v1.md
  table12_regeneration_diff_v1.csv
  table12_regeneration_readme_v1.md
```

### 10.2 Speedup summary regeneration

```text
reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/
  method_timing_case_level_v1.csv
  speedup_slice_summary_v1.csv

reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/
  speedup_slice_summary_regenerated_v1.csv
  speedup_slice_summary_regeneration_diff_v1.csv
  speedup_slice_summary_regeneration_readme_v1.md
```

### 10.3 Static recompute audit

```text
reports/evaluation/common_core_v0/16_STATIC_RECOMPUTE_AUDIT_V1/
  static_recompute_results_v1.csv
  static_recompute_mismatches_v1.csv
  static_recompute_readiness_update_v1.csv
  static_recompute_summary_v1.md
  static_recompute_readme_v1.md
```

### 10.4 Reviewer reproduction outputs

```text
reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/
  reviewer_reproduction_summary_v1.md
  reviewer_reproduction_status_v1.csv
  reviewer_reproduction_log_v1.txt
  deterministic/
    deterministic_reproduction_plan_v1.md
    deterministic_reproduction_status_v1.csv
    deterministic_reproduction_log_v1.txt
```

这些文件是复现运行的输出。它们可以帮助审稿人理解复现过程，但本机运行后可能产生 diff。提交前应确认是否真的需要更新。

---

## 11. Case package 契约

SQL-RewriteBench 的最小单位不是单条 SQL，而是 case package。一个较完整的 case package 通常包含：

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

并不是所有 legacy case 都已经完全符合这个结构。older anchor / staged packages 应以 registry、case-local artifacts 和 current review notes 为准。

---

## 12. 4+1 taxonomy

Common-core v0 使用 4 个 coverage axes 加 1 个 rewrite-opportunity 横切层：

| 层 | 作用 |
|---|---|
| SQL feature | SQL 本身的结构与语义构造，例如 CTE、correlated subquery、outer join、window、date/time function |
| Plan operator | 执行计划中的 canonical operator family，例如 scan、filter、join、aggregate、sort、limit |
| Workload realism | 来源和查询风格，例如 benchmark-derived analytical SQL、realistic query style、long-tail structure |
| Portability risk | 跨方言 / 跨引擎风险，例如 identifier quoting、datetime semantics、type semantics、limit/fetch gap |
| Rewrite opportunity | 该 case 为什么值得重写，例如 predicate pushdown、aggregation rewrite、subquery decorrelation、function normalization |

当前标签覆盖用于 benchmark characterization 和 failure slicing，不用于方法排序，也不代表真实 workload 频率。

---

## 13. 当前边界与 caveats

当前 artifact 明确保留以下边界：

- Table 12 不是排行榜；所有 rows 的 `leaderboard_comparable` 仍应理解为 no / claim-bounded。
- 所有 speedup 只在 exact + timing-success rows 上解释。
- `Direct LLM + Repair-1` 的 timing 是 mixed-source，不是 fresh independent route timing。
- `SQLGlot no-op` 是 low-transform / infrastructure route，不代表 optimizer improvement。
- `Calcite HEP` 的 93-row timing packet 是 correctness-gated packet，不是 full 120 timing policy。
- `R-Bot` 是 mixed-scope / PG15 bounded appendix evidence。
- `LLM-R2` 与 `LearnedRewrite` 仍是 bounded prior-method evidence。
- `SQLGlot Transpile` 与 `LLM Translate` 属于 Track C，不进 Track A same-engine speedup 表。
- `SQLSolver` 与 `VeriEQL` 是 verifier support，不是 rewrite baseline。
- `SpeedupTransferRate` 仍不可计算，因为缺少 paired target-engine timing。
- 当前只支持 selected-frontier observability，不支持 full denominator NodeAlignmentCoverage。

---

## 14. 新同学推荐阅读顺序

如果第一次接触本仓库，建议按下面顺序阅读：

```text
README.md
AGENTS.md
docs/DOC_MAP.md
docs/EXECUTION_STATUS.md
benchmark_spec/decision_log.md
docs/PROJECT_PLAN.md
benchmark_spec/benchmark_spec_v0.md
inventory/case_registry.csv
inventory/source_registry.csv
reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_summary_v1.md
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_regeneration_readme_v1.md
```

如果只想复现论文结果，优先看：

```text
scripts/reproduce_common_core_v0.sh
reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/
```

---

## 15. 维护规则

每次更新 artifact 或复现包时，请遵守以下规则：

1. 不要把新实验、协议变更、registry 事实变更混入 reproduction packaging commit。
2. 不要用 `git add .` 提交大量 `runs/`、timing logs、EXPLAIN workspaces。
3. 如果只更新 paper-facing table renderer，应同时提供 diff / readme / provenance。
4. 如果更新 speedup 值，应说明输入 timing rows、公式脚本、regeneration diff。
5. 如果更新 Table 12，应跑：

```bash
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
bash scripts/reproduce_common_core_v0.sh --mode artifact
```

6. 如果更新 deterministic runner，应至少跑：

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight
```

---

## 16. 一句话总结

SQL-RewriteBench 的目标不是收集最多 SQL，也不是证明某个方法最快。

它的目标是形成一个 **以 case package 为最小单位、以 correctness 为门槛、以 failure visibility 和 denominator-aware evidence ledger 为核心、能支持可观测性和跨引擎边界分析的 SQL rewrite benchmark**。

当前 Common-core v0 的最重要复现命令是：

```bash
bash scripts/reproduce_common_core_v0.sh --mode artifact
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

当前最重要的结果边界是：

> 没有单一 winner；有的是可追溯、可复验、有边界的 denominator-aware evidence。
