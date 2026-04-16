# 首次 Pilot 结果

## 文件作用
本文件记录了当前 SQL 重写 benchmark 仓库的**第一版面向论文的 pre-pilot 结果切片**。

其目的，是对当前已经稳定下来的证据进行总结，并为论文写作提供第一块结果内容。
它**并不**声称已经完成完整的 pilot 规模建设。

---

## 1. 当前解读

当前仓库已经支持一个受控的第一轮评估切片。
在现阶段：

- 跟踪中的 case 总数：**12**
- 第一结果切片中的 case 数：**8**
- 稳定 anchor：**4**
- 已接纳的 external common-core case：**2**
- 已通过三引擎验证的 staged draft：**2**

当前纳入第一切片的 case 为：

**PERF_0001, PERF_0002, LONGTAIL_0001, CONS_0001, CONS_0003, CONS_0004, PORT_0001, PORT_0002**

这里应将其理解为一个**pre-pilot 的稳定报告切片**，而不是完整 benchmark 已经完成的声明。

---

## 2. 表 1 —— Case 成熟度总结

| summary_group | count | case_ids | include_in_first_slice | notes |
| --- | --- | --- | --- | --- |
| stable_pilot_anchor | 4 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | yes | 四个 pool 上各有一个稳定 anchor |
| admitted_external_common_core | 2 | PERF_0002;PORT_0002 | yes | 当前已接纳的 external common-core cases |
| staged_tri_engine_validated_draft | 2 | CONS_0003;CONS_0004 | yes | 已完成三引擎验证，但仍为 not_yet_admitted |
| staged_partial_engine_closure_draft | 4 | PERF_0003;PERF_0004;LONGTAIL_0002;CONS_0002 | no | 引擎闭环仍不完整，或该 line 有意保持为 partial |
| total_repository_cases | 12 | PERF_0001;PERF_0002;PERF_0003;PERF_0004;LONGTAIL_0001;LONGTAIL_0002;CONS_0001;CONS_0002;CONS_0003;CONS_0004;PORT_0001;PORT_0002 | n/a | 当前被跟踪的 case 全集 |
| first_slice_total | 8 | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001;PERF_0002;PORT_0002;CONS_0003;CONS_0004 | yes | 当前的 pre-pilot 评估切片 |

### 解读
当前仓库已经呈现出一种非扁平的成熟度结构：
- 四个稳定的 pilot anchor，
- 已接纳的 external common-core cases，
- 以及处于不同闭环程度的 staged drafts。

这说明，即使在尚未扩展到完整 pilot 规模之前，该 benchmark 也已经具备支持其结构成熟度主张的基础。

---

## 3. 表 2 —— Case 级成熟度矩阵

| case_id | pool | source_family | current_maturity | validated_engines | admitted_or_staged | include_in_first_slice | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | smoke/pipeline anchor |
| PERF_0002 | performance | TPC-DS | admitted_external_common_core | postgres;mysql;spark | admitted | yes | 当前最强的 external performance case |
| PERF_0003 | performance | JOB | pg_only_staged_performance_draft | postgres | staged | no | JOB line 当前被冻结为 partial realized supplement |
| PERF_0004 | performance | JOB | pg_validated_staged_performance_draft | postgres | staged | no | JOB line 当前被冻结为 partial realized supplement |
| LONGTAIL_0001 | longtail | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | 结构丰富的 longtail anchor |
| LONGTAIL_0002 | longtail | SQLStorm | pg_validated_staged_longtail_draft | postgres | staged | no | 仍缺少引擎闭环 |
| CONS_0001 | consistency | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | correctness anchor |
| CONS_0002 | consistency | Calcite | pg_validated_staged_consistency_draft | postgres | staged | no | 仍缺少更广泛的引擎验证 |
| CONS_0003 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes | 已通过三引擎验证，但仍为 not_yet_admitted |
| CONS_0004 | consistency | VeriEQL | tri_engine_validated_staged_consistency_draft | postgres;mysql;spark | staged | yes | 已通过三引擎验证，但仍为 not_yet_admitted |
| PORT_0001 | portability | manual_seed | stable_pilot_anchor | postgres;mysql;spark | anchor | yes | 干净的 portability anchor |
| PORT_0002 | portability | PARROT | admitted_external_common_core | postgres;mysql;spark | admitted | yes | 当前最强的 external portability case |

### 解读
当前第一切片的纳入边界是有意保守设定的。
只有那些成熟度和引擎证据足够稳定的 case，才会被纳入其中。

---

## 4. 表 3 —— Source 到 Case 的 materialization 映射表

| source_family | source_role | current_source_status | materialized_cases | active_pool_alignment | current_line_interpretation | first_slice_usage | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| manual_seed | internal_seed_family | active | PERF_0001;LONGTAIL_0001;CONS_0001;PORT_0001 | performance;longtail;consistency;portability | 内部 anchor source family | yes | 不是正式的第五个 pool |
| TPC-H | performance_base | staged_partial_inspection | none | performance | 目标 source，但当前尚未 materialize 为活跃 case line | no | 资源已存在，但尚未转化为当前活跃 case line |
| TPC-DS | performance_base | staged_and_inspected | PERF_0002 | performance | 当前最强的 external performance line | yes | 已存在被接纳的 external common-core case |
| SQLStorm | longtail_base | staged_and_inspected | LONGTAIL_0002 | longtail | 主 longtail source，但 case line 仍处于 staged 状态 | no | 当前未纳入第一切片，原因是引擎闭环仍有缺口 |
| Stack | longtail_realism_substrate | dumps_only_realism_substrate | none | longtail | 仅作为 realism substrate | no | 在当前版本中，并不是直接的 SQL query 语料 |
| Calcite | consistency_base | staged_and_inspected | CONS_0002 | consistency | 基础 consistency seed line | no | 当前 case 仍只是 PG-only staged draft |
| VeriEQL | consistency_supplement | accepted_and_materialized | CONS_0003;CONS_0004 | consistency | 当前最强的 consistency supplement line | yes | 两个 staged draft 现在都已具备三引擎闭环 |
| PARROT | portability_base | staged_and_inspected | PORT_0002 | portability | 当前最强的 external portability line | yes | 已存在被接纳的 external common-core case |
| JOB | performance_supplement | partial_realized_frozen | PERF_0003;PERF_0004 | performance | 仅作为 partial realized supplement | no | 当前阶段不再继续深化 |
| DSB | performance_realism_candidate | unresolved_not_started | none | performance | 在 source 决策层仍未解决 | no | 尚未开始 acquisition 或 inspection |
| SQLEquiQuest | alternative_consistency_candidate | not_selected | none | consistency | 当前分支中未启用 | no | VeriEQL 是当前被选中的 supplement source |

### 解读
这个 benchmark 不是通过把所有 SQL 平铺并集在一起来构建的。
相反，不同的 source family 在当前承担着不同角色：

- anchors，
- 已接纳的 external case lines，
- staged draft lines，
- realism substrate lines，
- 以及尚未解决、仅停留在目标层的 lines。

---

## 5. 表 4 —— 引擎验证总结

| case_id | pool | current_maturity | postgres_validated | mysql_validated | spark_validated | result_artifacts_present | plan_artifacts_present | current_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0001 | performance | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | smoke/pipeline anchor |
| PERF_0002 | performance | admitted_external_common_core | yes | yes | yes | yes | yes | admitted | 当前最强的 external performance case |
| LONGTAIL_0001 | longtail | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | 结构丰富的 longtail anchor |
| CONS_0001 | consistency | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | correctness anchor |
| CONS_0003 | consistency | tri_engine_validated_staged_consistency_draft | yes | yes | yes | yes | yes | staged | 已通过三引擎验证，但仍为 not_yet_admitted |
| CONS_0004 | consistency | tri_engine_validated_staged_consistency_draft | yes | yes | yes | yes | yes | staged | 已通过三引擎验证，但仍为 not_yet_admitted |
| PORT_0001 | portability | stable_pilot_anchor | yes | yes | yes | yes | yes | anchor | 干净的 portability anchor |
| PORT_0002 | portability | admitted_external_common_core | yes | yes | yes | yes | yes | admitted | 当前最强的 external portability case |

### 解读
第一切片被有意限制在那些引擎证据足够强的 case 上。
特别是，当前第一切片已经包括：

- 三引擎 anchor，
- 已接纳的 external 三引擎 case，
- 以及已完成三引擎验证的 staged consistency drafts。

这使得仓库在早期阶段就已经对 correctness-aware 和 cross-engine evaluation 提供了有意义的支撑。

### 指标总结

在当前 first-slice 子集上，所有已报告的早期指标在切片层面均为 1.000。
具体来说，当前 pre-pilot 切片实现了：

- `ExecutableRate = 1.000`（8 / 8）
- `ResultConsistencyRate = 1.000`（8 / 8）
- `NegativeRejectionRate = 1.000`（8 / 8）
- `CrossEngineExecutableRate = 1.000`（8 / 8）
- `CrossEngineConsistencyRate = 1.000`（8 / 8）
- `PlanArtifactCoverage = 1.000`（8 / 8）

这些数值应以保守方式解读。
它们并不表示 benchmark 已经完成；相反，它们反映的是：第一切片是有意限制在当前最稳定的 case 上的。

---

## 6. 当前最强结论

在当前仓库阶段，最强的、可面向论文表达的结论包括：

1. 该 benchmark 已经具有一个有意义的**四池结构**。
2. 仓库已经区分出 **anchor / admitted / staged** 三类 line。
3. 一个稳定的**三引擎证据切片**已经存在。
4. consistency line 中已经包含了**已通过三引擎验证的 staged drafts**，这表明 correctness 已经成为 benchmark 的一等维度。

---

## 7. 当前不应声称的内容

当前结果**不应**被解读为以下内容的证据：

- 已完成完整的 pilot 规模建设，
- 已完成完整的 source universe 闭环，
- 已完成大规模 baseline comparison，
- 已完成广泛 workload curating，
- 或 benchmark 已具备大规模扩展就绪性。

这些仍然是后续阶段的目标。

---

## 8. 直接下一步

在这个结果快照之后，下一步应当把这些表格作为以下内容的基础：

- 第一版 evaluation 子章节草稿，
- 第一版 benchmark characterization 子章节，
- 以及第一版附录式成熟度总结模块。

只有在那之后，团队才应决定下一阶段优先推进哪一项：

- 选择性的 source activation，
- 受控的 benchmark 扩展，
- 或 baseline-comparison 准备。