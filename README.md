# SQL Rewrite Benchmark

## 范围
- 引擎 / 方言：Spark SQL、PostgreSQL、MySQL
- 最小 benchmark 单元：case package
- v1 不包含 compositional OOD split
- v1 不包含 engine / dialect hold-out split

## 对仓库的理解
当前，这个仓库最合适的理解方式是一个**pre-pilot / early-pilot 阶段的 SQL rewrite benchmark 构建项目**。

它已经超出了 bootstrap 阶段，目前已经包含：
- 一个稳定的四池 benchmark 结构，
- 明确的 source-to-case 分离，
- 稳定的 anchor cases，
- 已接纳的 external common-core cases，
- 处于不同闭环程度的 staged drafts，
- 以及第一版面向论文的评估切片。

这个仓库**还不应**被理解为：
- 一个完整的 pilot 规模 benchmark 发布版本，
- 一个已经完全闭合的 source universe，
- 一个已经完成广泛 workload curating 的版本，
- 或一个完整的 baseline-comparison package。

## 当前稳定的第一切片
当前第一版评估切片包括：

- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`
- `PERF_0002`
- `PORT_0002`
- `CONS_0003`
- `CONS_0004`

选择这些 case 的原因在于，它们共同提供了：
- 四个 formal pools 的完整覆盖，
- anchor / admitted / staged 的成熟度对比，
- 以及足够稳定的多引擎验证证据。

## 当前仓库状态
当前仓库包含：

### 稳定 anchors
- `PERF_0001`
- `LONGTAIL_0001`
- `CONS_0001`
- `PORT_0001`

### 已接纳的 external common-core cases
- `PERF_0002`
- `PORT_0002`

### 已通过三引擎验证的 staged drafts
- `CONS_0003`
- `CONS_0004`

### 仍处于 staged、但未纳入第一切片的 case
- `LONGTAIL_0002`
- `CONS_0002`
- `PERF_0003`
- `PERF_0004`

## 对 source 层的理解
当前，不同 source family 承担着不同角色：

- **TPC-DS**：活跃的 external performance line
- **SQLStorm**：活跃的 long-tail source，但对应的 case line 仍处于 staged 状态
- **Calcite**：活跃的 consistency seed source，但对应的 case line 仍处于 staged 状态
- **VeriEQL**：活跃的 consistency supplement line
- **PARROT**：活跃的 external portability line
- **JOB**：部分实现的 performance supplement
- **Stack**：仅作为 realism substrate，不是直接的 SQL query corpus
- **DSB**：尚未解决 / 还未启动
- **Manual Seed Cases**：内部 anchor source family，不是第五个 pool

## 环境约定
- 主要开发环境：WSL Ubuntu
- Git 通过 SSH 使用
- PostgreSQL 运行在 Windows 宿主机上，并通过 NAT 从 WSL 访问
- MySQL 运行在 WSL 内部，用于本地验证
- Spark 以 local 模式运行在 WSL 内部
- Codex / 自动化辅助工具应在同一个 WSL shell 中启动，并带上所需环境变量

## 当前工程基线
当前仓库已经具备：
- PostgreSQL smoke 已通过
- MySQL smoke 已通过
- Spark smoke 已通过
- 三引擎 smoke / preflight CLI 检查
- machine-readable 的 result 和 plan artifacts
- 第一版正式 coverage map
- 第一版正式 gap report
- 第一版 pilot reporting tables

## 当前重点
当前的工作重点是**第一切片评估与面向论文的结果组织**，而不是广泛扩展 source。

这意味着，当前最直接的重点是：
1. 生成稳定的 pilot tables，
2. 起草第一版 results 子章节，
3. 并将当前证据整理成适合论文使用的形式。

当前的重点**不是**：
- 广泛的 workload curating，
- 大规模的 source 扩展，
- 或完整的 baseline-comparison 执行。

## 项目设计原则
- source != benchmark unit
- case package = benchmark unit
- 只有四个 formal pools：
  - performance
  - longtail
  - consistency
  - portability
- `Manual Seed Cases` 是一种 source family / curation channel，不是第五个 pool

## 推荐的当前阅读路径
如果你刚接触这个仓库，建议从以下内容开始阅读：
1. `docs/PROJECT_PLAN.md`
2. `benchmark_spec/decision_log.md`
3. `docs/M1_GAP_REPORT.md`
4. `reports/pilot/`
5. `docs/FIRST_PILOT_RESULTS.md` / `docs/FIRST_SLICE_APPENDIX.md`