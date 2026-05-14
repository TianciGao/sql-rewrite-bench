# SQL-RewriteBench

> 面向 **语句级 SQL 重写（statement-level SQL rewrite）** 的 benchmark 与 artifact 工作区。  
> 本项目评估方法最终输出的完整 SQL 语句，而不是内部 AST、优化器规则轨迹或单纯的 parser success。

SQL-RewriteBench 提供一套可复验的 SQL rewrite 评测协议：在统一的 case package 契约下，记录候选 SQL 是否生成、是否可执行、是否语义一致、是否发生了有意义的改写、是否带来性能收益，以及失败是否可以被定位。

当前分支面向 **SQL-RewriteBench 先行版发布（preview release）**，包含 Common-core v0 case packages、保留实验结果、主要结果表、复现脚本和 artifact 索引，适合审稿复验、团队交接和公开发布前验证。

---

## 目录

- [1. 先行版内容](#1-先行版内容)
- [2. Common-core v0 分母](#2-common-core-v0-分母)
- [3. Common-core 之外的 case packages](#3-common-core-之外的-case-packages)
- [4. 评测协议](#4-评测协议)
- [5. 主要结果：Table 12](#5-主要结果table-12)
- [6. 当前实验结论](#6-当前实验结论)
- [7. 仓库结构](#7-仓库结构)
- [8. 快速复现：artifact smoke](#8-快速复现artifact-smoke)
- [9. 完整复现通道](#9-完整复现通道)
- [10. 复现验收标准](#10-复现验收标准)
- [11. 关键文件](#11-关键文件)
- [12. Case package 契约](#12-case-package-契约)
- [13. 4+1 taxonomy](#13-41-taxonomy)
- [14. 先行版范围](#14-先行版范围)
- [15. 新用户阅读顺序](#15-新用户阅读顺序)
- [16. 维护规则](#16-维护规则)
- [17. 摘要](#17-摘要)

---

## 1. 先行版内容

| 模块 | 内容 |
|---|---|
| Common-core v0 | 40 个 case packages |
| Track A 同引擎展开 | PostgreSQL / MySQL / Spark，共 120 个 same-engine rows |
| 非主分母 case 索引 | 150 个 Common-core 之外的 case packages，按 staged、backlog/deferred/not-assessed、admitted/frozen/anchor reference 分类记录 |
| Case-package 契约 | source SQL、positive rewrite、hard negative、schema/data context、checker path、plan/failure artifacts、provenance、taxonomy tags |
| 角色感知结果 | control、same-engine rewrite、portability transfer、observability support、verifier support 分开记录 |
| 分母感知指标 | planned、generated/ready、executed、exact、timed 分开统计 |
| 主要结果表 | Common-core v0 method evidence ledger |
| 复现入口 | 静态再生成脚本、speedup summary 再生成脚本、reviewer artifact-mode smoke 脚本 |

本先行版聚焦 Common-core v0 的可复验发布，不覆盖全部未来扩展集。SpeedupTransferRate、完整 PORT9 迁移速度评估、完整 denominator-wide NodeAlignmentCoverage 和跨引擎计划归因保留为后续扩展。

---

## 2. Common-core v0 分母

Common-core v0 是当前主要实验与复现的固定分母：

```text
40 cases × 3 same-engine targets = 120 rows
engines = PostgreSQL / MySQL / Spark
```

### 2.1 Pool 组成

| Pool | Cases | Same-engine rows | 主要压力 | 作用 |
|---|---:|---:|---|---|
| PERF | 16 | 48 | 分析型 SQL、性能敏感 rewrite、predicate / aggregation / join pressure | correctness-gated speedup、性能退化、方法对照 |
| CONS | 9 | 27 | NULL、聚合、重复、多重性、hard negative、semantic boundary | correctness、false accept risk、checker guard |
| PORT | 9 | 27 | 方言差异、函数/类型/日期/引用风险 | cross-engine execution / consistency |
| LONGTAIL | 6 | 18 | 真实风格、复杂结构、长尾 SQL | robustness、failure diagnosis、结构覆盖 |
| **Total** | **40** | **120** | 全部 | Common-core v0 主分母 |

Common-core v0 是一个受控覆盖面（controlled coverage surface）。它用于覆盖 SQL rewrite 中容易出错的结构、语义边界、可移植性风险和计划可观测性场景，而不是模拟生产环境 SQL 的频率分布。

### 2.2 Common-core v0 case IDs

<details open>
<summary><strong>PERF：16 个</strong></summary>

```text
PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019,
PERF_0024, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054,
PERF_0056, PERF_0062, PERF_0077, PERF_0082
```

</details>

<details open>
<summary><strong>CONS：9 个</strong></summary>

```text
CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012,
CONS_0024, CONS_0036, CONS_0037
```

</details>

<details open>
<summary><strong>PORT：9 个</strong></summary>

```text
PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013,
PORT_0022, PORT_0024, PORT_0025
```

</details>

<details open>
<summary><strong>LONGTAIL：6 个</strong></summary>

```text
LONGTAIL_0011, LONGTAIL_0012, LONGTAIL_0013,
LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024
```

</details>

---

## 3. Common-core 之外的 case packages

除 Common-core v0 的 40 个主分母 case 外，仓库当前还记录了 150 个非 Common-core v0 主分母 case packages。这些 case 用于后续覆盖扩展、证据补全、失败分析、审查材料和未来版本演进；它们不默认进入 Table 12 的 120-row same-engine 主分母。

### 3.1 分类汇总

| 状态 | 数量 | 说明 |
|---|---:|---|
| staged / not-yet-admitted drafts | 66 | 已有不同程度的 case package 或证据，但未进入 Common-core v0 主分母 |
| backlog / deferred / not-assessed | 78 | 保留为后续覆盖、补证据或重新审查材料 |
| admitted / frozen / anchor references outside CC-v0 | 6 | 历史锚点或已接纳参考包，但不属于当前 Common-core v0 40-case denominator |
| registry-marked extended | 0 | 当前 registry 没有额外标记为 extended 的非主分母 case |
| active candidate | 0 | 当前 registry 没有额外标记为 active Common-core candidate 的非主分母 case |

### 3.2 按 pool 汇总

| Pool | staged | backlog / deferred / not-assessed | admitted / frozen / anchor | total outside CC-v0 |
|---|---:|---:|---:|---:|
| PERF | 38 | 45 | 2 | 85 |
| CONS | 11 | 19 | 1 | 31 |
| PORT | 16 | 0 | 2 | 18 |
| LONGTAIL | 1 | 14 | 1 | 16 |
| **Total** | **66** | **78** | **6** | **150** |

### 3.3 Staged / not-yet-admitted drafts

这些 case 已有不同程度的 case package、验证材料或工程证据，但当前不属于 Common-core v0 主分母。

<details open>
<summary><strong>PERF：38 个</strong></summary>

```text
PERF_0003, PERF_0004, PERF_0005, PERF_0009, PERF_0010, PERF_0011,
PERF_0012, PERF_0014, PERF_0015, PERF_0016, PERF_0018, PERF_0020,
PERF_0021, PERF_0022, PERF_0023, PERF_0025, PERF_0026, PERF_0036,
PERF_0038, PERF_0043, PERF_0044, PERF_0047, PERF_0050, PERF_0053,
PERF_0063, PERF_0065, PERF_0066, PERF_0076, PERF_0084, PERF_0086,
PERF_0090, PERF_0091, PERF_0095, PERF_0096, PERF_0101, PERF_0103,
PERF_0104, PERF_0106
```

</details>

<details open>
<summary><strong>CONS：11 个</strong></summary>

```text
CONS_0002, CONS_0003, CONS_0004, CONS_0006, CONS_0017, CONS_0023,
CONS_0029, CONS_0031, CONS_0032, CONS_0034, CONS_0040
```

</details>

<details open>
<summary><strong>PORT：16 个</strong></summary>

```text
PORT_0006, PORT_0009, PORT_0010, PORT_0011, PORT_0014, PORT_0015,
PORT_0016, PORT_0017, PORT_0018, PORT_0019, PORT_0020, PORT_0021,
PORT_0023, PORT_0026, PORT_0027, PORT_0028
```

</details>

<details open>
<summary><strong>LONGTAIL：1 个</strong></summary>

```text
LONGTAIL_0002
```

</details>

### 3.4 Backlog / deferred / not-assessed packages

这些 case 保留为后续覆盖、补证据或重新审查材料。它们当前不进入 Common-core v0 主分母。

<details open>
<summary><strong>PERF：45 个</strong></summary>

```text
PERF_0027, PERF_0028, PERF_0029, PERF_0030, PERF_0031, PERF_0032,
PERF_0037, PERF_0039, PERF_0040, PERF_0041, PERF_0042, PERF_0045,
PERF_0046, PERF_0048, PERF_0049, PERF_0051, PERF_0055, PERF_0057,
PERF_0058, PERF_0059, PERF_0060, PERF_0061, PERF_0064, PERF_0067,
PERF_0068, PERF_0069, PERF_0070, PERF_0071, PERF_0072, PERF_0073,
PERF_0074, PERF_0075, PERF_0078, PERF_0080, PERF_0081, PERF_0083,
PERF_0085, PERF_0093, PERF_0094, PERF_0097, PERF_0102, PERF_0105,
PERF_0107, PERF_0108, PERF_0109
```

</details>

<details open>
<summary><strong>CONS：19 个</strong></summary>

```text
CONS_0008, CONS_0013, CONS_0014, CONS_0015, CONS_0016, CONS_0018,
CONS_0019, CONS_0020, CONS_0021, CONS_0022, CONS_0025, CONS_0026,
CONS_0027, CONS_0028, CONS_0030, CONS_0033, CONS_0035, CONS_0038,
CONS_0039
```

</details>

<details open>
<summary><strong>LONGTAIL：14 个</strong></summary>

```text
LONGTAIL_0003, LONGTAIL_0004, LONGTAIL_0005, LONGTAIL_0007,
LONGTAIL_0008, LONGTAIL_0009, LONGTAIL_0010, LONGTAIL_0014,
LONGTAIL_0015, LONGTAIL_0016, LONGTAIL_0018, LONGTAIL_0019,
LONGTAIL_0020, LONGTAIL_0021
```

</details>

<details open>
<summary><strong>PORT：0 个</strong></summary>

```text
none
```

</details>

### 3.5 Admitted / frozen / anchor references outside Common-core v0

这些是历史锚点或已接纳参考包，但不属于当前 Common-core v0 40-case denominator。

```text
PERF_0001, PERF_0002, CONS_0001, PORT_0001, PORT_0002, LONGTAIL_0001
```

### 3.6 Extended / candidate / unclear

当前 registry 中没有额外标记为 extended 的非主分母 case，也没有额外标记为 active Common-core candidate 的非主分母 case。

```text
extended: none
candidate: none
unclear: none
```

本节是对 `inventory/case_registry.csv` 的发布版索引整理。若本节与后续 registry 更新出现差异，以 `inventory/case_registry.csv` 为 live case fact source。Common-core / extended 的具体划分规则由 `benchmark_spec/common_core_extended_rules_v0.md` 维护，批次级审查记录见 `benchmark_spec/reviews/`。

---

## 4. 评测协议

SQL-RewriteBench 的评测单位是 case package，而不是单条 SQL 字符串。一个 case package 至少应能回答：

1. source SQL 在目标引擎上如何执行；
2. positive rewrite 是否保持语义；
3. hard negative 是否被 checker 拒绝；
4. 方法输出的候选 SQL 是否生成、执行、语义一致；
5. exact 且 timed 的候选是否带来性能收益；
6. 失败是否能通过 error、checker、plan 或 provenance artifact 定位。

### 4.1 结果角色

| 角色 | 说明 | 典型内容 |
|---|---|---|
| Control | 校准 source、positive、negative 和 checker | Native / Human positive / Hard negative |
| Same-engine rewrite | 同一引擎内生成候选 SQL 并检查正确性和性能 | Direct LLM、SQLGlot、Calcite HEP 等 |
| Portability transfer | 跨方言 / 跨引擎适配 | SQLGlot Transpile、LLM Translate |
| Observability support | 解释失败、退化和计划变化 | plan artifacts、failure buckets、selected frontier |
| Verifier support | 提供等价性或反例支撑 | SQLSolver、VeriEQL |

### 4.2 分母链

核心指标按分母链记录：

```text
planned → generated / ready → executed → exact → timed
```

性能只在 exact 且 timing-success 的行上解释。GM speedup、median、win/tie/loss 和 Regression@20 都绑定到各自的 timing denominator。

---

## 5. 主要结果：Table 12

Table 12 是 Common-core v0 的主要结果表。它汇总当前保留的 same-engine、bounded prior-method 和 route-level evidence，并保留每一行的 scope、分母和 timing 资格。

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

### 5.1 再生成 Table 12

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

---

## 6. 当前实验结论

当前 Common-core v0 evidence packet 支撑以下结论：

1. **SQL rewrite 评测需要保留完整分母链。** 只看生成成功或执行成功子集，会高估方法质量。
2. **Hard-negative guardrail 能检验 checker 是否过宽。** 当前 120 planned hard-negative cells 中，111 tested，9 not applicable；111 个 tested cells 均为 executable semantic mismatch，并全部被 checker 拒绝，false accepts = 0。
3. **正确性是速度解释的前提，但正确并不自动带来性能收益。** 多个 exact timed slices 接近中性，部分路线仍存在 regression。
4. **No-op / source-like 输出需要单独记录。** 正确但几乎未改写的 SQL 不应被当作有效优化收益。
5. **跨引擎执行与一致性需要分层报告。** 当前 bounded PORT6 支持有限语义可移植性证据，但缺少 paired target-engine timing，因此 SpeedupTransferRate 暂不计算。
6. **Verifier 工具属于 support evidence。** SQLSolver / VeriEQL 可用于增强 correctness support，但不作为 rewrite-generation baseline。

---

## 7. 仓库结构

推荐从以下目录理解仓库：

```text
cases/                                      # case packages
reports/evaluation/common_core_v0/          # Common-core v0 retained evidence and regenerated tables
reports/evaluation/common_core_v0/scripts/  # paper-table renderers
scripts/                                    # reviewer-facing reproduction entrypoints
inventory/                                  # source / case registry
benchmark_spec/                             # rules, decision log, review records
docs/                                       # project plan, execution status, documentation
```

当前复现最关键的脚本是：

```text
scripts/reproduce_common_core_v0.sh
reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py
```

---

## 8. 快速复现：artifact smoke

审稿人或新用户可以先运行 artifact mode。该模式只检查保留的 evidence 目录和静态表格再生成，不运行数据库、不发起 LLM 调用、不运行 verifier，也不采集新的 EXPLAIN 或 timing。

```bash
bash scripts/reproduce_common_core_v0.sh --mode artifact
```

期望看到：

```text
PASS table12_renderer_check: Table 12 regenerated successfully
PASS static_recompute_mismatches_empty: 0 conflict or missing-input rows
PASS table12_diff_summary: cells_compared=90; exact_match=55; expected_NA_match=8; artifact_boundary_match=27; conflicts=0; missing_input=0
Reviewer reproduction artifact-mode passed.
```

---

## 9. 完整复现通道

完整复现通道分为三层：

1. 重跑 deterministic runners；
2. 重新用公式计算 speedup summary；
3. 重新生成 Table 12。

### 9.1 deterministic preflight

先检查 runner 注册和本地工具是否存在：

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

### 9.2 重跑 deterministic runners

这些命令会根据 step 运行本地 deterministic pipeline。部分 step 可能访问数据库、执行 EXPLAIN 或读取 retained timing inputs。运行前请确认 PostgreSQL / MySQL / Spark、本地数据和环境变量已配置。

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

可以按需要组合多个 step：

```bash
bash scripts/reproduce_common_core_v0.sh \
  --mode deterministic \
  --execute \
  --continue-on-error \
  --steps hard-negative,sqlglot,calcite,pg-plan,direct-llm-timing-retained,rbot-pg15-timing
```

### 9.3 speedup summary 数据流

Table 12 中的 `Timed / GM / Regression@20` 通过公式脚本再生成。数据流如下：

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

重新计算 speedup summary：

```bash
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check
```

主要输入：

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

### 9.4 重新生成 Table 12

```bash
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```

查看结果：

```bash
sed -n '1,120p' \
  reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/table12_method_evidence_ledger_regenerated_v1.md
```

### 9.5 推荐顺序

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

## 10. 复现验收标准

### 10.1 Table 12 renderer

通过条件：

```text
rows rendered: 9
cells compared: 90
conflicts: 0
```

完整 diff summary 通常为：

```text
exact matches: 55
rounded matches: 0
expected NA matches: 8
artifact boundary matches: 27
conflicts: 0
missing_input: 0
```

### 10.2 Artifact mode

通过条件：

```text
Reviewer reproduction artifact-mode passed.
```

并确认：

```text
PASS static_recompute_mismatches_empty
PASS expected_na_boundaries_present
PASS table12_diff_summary
```

### 10.3 deterministic table12 preflight

通过条件：

```text
preflight_pass table12: runner and required local tools found
```

---

## 11. 关键文件

### 11.1 Table 12 provenance 与 regeneration

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

### 11.2 Speedup summary regeneration

```text
reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/
  method_timing_case_level_v1.csv
  speedup_slice_summary_v1.csv

reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/
  speedup_slice_summary_regenerated_v1.csv
  speedup_slice_summary_regeneration_diff_v1.csv
  speedup_slice_summary_regeneration_readme_v1.md
```

### 11.3 Static recompute audit

```text
reports/evaluation/common_core_v0/16_STATIC_RECOMPUTE_AUDIT_V1/
  static_recompute_results_v1.csv
  static_recompute_mismatches_v1.csv
  static_recompute_readiness_update_v1.csv
  static_recompute_summary_v1.md
  static_recompute_readme_v1.md
```

### 11.4 Reviewer reproduction outputs

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

运行复现后，这些 log/status 文件可能出现本机 diff。提交前请确认是否需要保留。

---

## 12. Case package 契约

一个较完整的 case package 通常包含：

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

legacy case 可能尚未完全符合该结构。具体状态以 case-local artifacts、registry 和 review notes 为准。

---

## 13. 4+1 taxonomy

Common-core v0 使用 4 个 coverage axes 加 1 个 rewrite-opportunity 横切层：

| 层 | 作用 |
|---|---|
| SQL feature | SQL 结构与语义构造，例如 CTE、correlated subquery、outer join、window、date/time function |
| Plan operator | 执行计划中的 canonical operator family，例如 scan、filter、join、aggregate、sort、limit |
| Workload realism | 来源和查询风格，例如 benchmark-derived analytical SQL、realistic query style、long-tail structure |
| Portability risk | 跨方言 / 跨引擎风险，例如 identifier quoting、datetime semantics、type semantics、limit/fetch gap |
| Rewrite opportunity | case 为什么值得重写，例如 predicate pushdown、aggregation rewrite、subquery decorrelation、function normalization |

Taxonomy 用于 benchmark characterization 和 failure slicing，不用于方法排序，也不代表真实 workload 频率。

---

## 14. 先行版范围

当前先行版的范围如下：

- Table 12 是当前主要结果表；
- 所有 speedup 均在 exact + timing-success rows 上解释；
- Direct LLM + Repair-1 的 timing 是 mixed-source；
- SQLGlot no-op 是 low-transform / infrastructure route；
- Calcite HEP 的 93-row timing packet 是 correctness-gated packet；
- R-Bot 是 mixed-scope / PG15 bounded appendix evidence；
- LLM-R2 与 LearnedRewrite 是 bounded prior-method evidence；
- SQLGlot Transpile 与 LLM Translate 属于 Track C portability；
- SQLSolver 与 VeriEQL 属于 verifier support；
- SpeedupTransferRate 暂不计算；
- 当前可观测性结果为 selected-frontier observability，不是完整 denominator-wide NodeAlignmentCoverage。

---

## 15. 新用户阅读顺序

第一次接触本仓库，建议阅读：

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

只复现主要结果时，优先看：

```text
scripts/reproduce_common_core_v0.sh
reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py
reports/evaluation/common_core_v0/18_TABLE12_REGENERATION_V1/
reports/evaluation/common_core_v0/19_SPEEDUP_SUMMARY_REGENERATION_V1/
```

---

## 16. 维护规则

更新 artifact 或复现包时，请遵守以下规则：

1. 不把新实验、协议变更、registry 事实变更混入 reproduction packaging commit。
2. 不用 `git add .` 提交大量 `runs/`、timing logs、EXPLAIN workspaces。
3. 更新 paper-facing table renderer 时，同步保留 diff、readme 和 provenance。
4. 更新 speedup 值时，说明输入 timing rows、公式脚本和 regeneration diff。
5. 更新 Table 12 前后，至少运行：

```bash
python -B reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py --check
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
bash scripts/reproduce_common_core_v0.sh --mode artifact
```

6. 更新 deterministic runner 时，至少运行：

```bash
bash scripts/reproduce_common_core_v0.sh --mode deterministic --dry-run
bash scripts/reproduce_common_core_v0.sh --mode deterministic --preflight
```

提交前检查 staged 内容：

```bash
git diff --cached --name-only | grep '^reports/evaluation/common_core_v0/runs/' \
  && echo "BAD: runs files staged" \
  || echo "OK: no runs files staged"

git diff --cached --name-only | grep -E '^(inventory/|benchmark_spec/|docs/EXECUTION_STATUS.md)$' \
  && echo "BAD: source-of-truth file staged" \
  || echo "OK: no registry/protocol/status files staged"
```

---

## 17. 摘要

SQL-RewriteBench 以 case package 为最小单位，以 correctness 为门槛，以 failure visibility 和 denominator-aware evidence ledger 为核心，提供一个可复验、可诊断、可扩展的 SQL rewrite benchmark。

当前先行版的主要复现命令是：

```bash
bash scripts/reproduce_common_core_v0.sh --mode artifact
python -B reports/evaluation/common_core_v0/scripts/render_table12_method_evidence_ledger_v1.py --check
```
