# M1 Gap Report

## 文件定位
本文件用于完成 M1 closeout 所需的 formal gap report。
它不新增 benchmark source，不扩 benchmark case，只总结当前 source universe 与 actual progress 之间的差异，并冻结下一轮优先补齐项。

## 1. 当前已具备的 source-layer 基础
当前已经进入可用 source 层的主要来源包括：

- TPC-H
- TPC-DS
- SQLStorm
- Calcite
- PARROT
- VeriEQL
- Manual Seed Cases

其中：
- TPC-DS 已 materialize 为 `PERF_0002`
- SQLStorm 已 materialize 为 `LONGTAIL_0002`
- Calcite 已 materialize 为 `CONS_0002`
- PARROT 已 materialize 为 `PORT_0002`
- VeriEQL 已 materialize 为 `CONS_0003` / `CONS_0004`

## 2. 当前最主要的缺口

### Gap A: target source universe 和 actual progress 仍不一致
最初目标源全集包括：
- TPC-H
- TPC-DS
- DSB
- JOB
- SQLStorm
- Stack
- Calcite
- SQLEquiQuest or VeriEQL
- PARROT
- Manual Seed Cases

但当前真实完成度并不一致：
- VeriEQL 已被选中并投入使用
- JOB 只部分 probe / partial realized
- Stack 仍未明确 direct SQL query corpus
- DSB 仍是 target source，未启动 acquisition / inspection
- SQLEquiQuest 当前不是 active branch

### Gap B: source-layer 已推进，但 case-layer closure 不平衡
当前各 source 对应的 case closure 强度不一致：
- `PERF_0002` / `PORT_0002` 已 admitted external common-core
- `LONGTAIL_0002` / `CONS_0002` 仍是 staged drafts
- `CONS_0003` / `CONS_0004` 已到 PG+MySQL validated staged drafts
- JOB line only partially realized through `PERF_0003` / `PERF_0004`

### Gap C: Spark closure remains the main consistency-side technical gap
- `CONS_0003` 缺 Spark closure
- `CONS_0004` 缺 Spark closure
- current recommendation is not immediate deepening, but explicit freezing as staged until the next deliberate consistency pass

### Gap D: long-tail realism source still has a structural unresolved point
Stack 当前拿到的是 dumps / substrate，而不是 direct SQL query corpus。
因此 long-tail realism source 线并未真正闭合。

### Gap E: DSB remains a declared target source but not an active source
DSB 仍在目标源全集里，但目前没有 acquisition、inspection 或 seed extraction 实体进展。

## 3. 下一轮优先补齐项（冻结排序）

### Priority 1
明确 Stack 是否能形成 direct SQL query corpus。
如果不能，就必须显式保留为 realism substrate，而不能再被口头当成“已具备 query source”。

### Priority 2
对 JOB 做一次明确的人类决策：
- continue deepen
or
- freeze as partial realized performance supplement

### Priority 3
对 DSB 做一次明确的人类决策：
- start acquisition / inspection
or
- remain target-only source in current version

## 4. 当前明确不做的事
当前阶段不做以下事项：

- 不新增 benchmark workloads
- 不新增 benchmark cases
- 不启动广义 workload curation
- 不开始 baseline 主实验
- 不把 `CONS_0003` / `CONS_0004` 立即推进 admission
- 不把 Stack 误写成已经具备 direct SQL query corpus
- 不把 DSB 误写成已完成 acquisition / inspection

## 5. M1 closeout judgment
在当前仓库状态下：

- source/case/admission 文档同步已基本完成
- target-source snapshot 已生成
- first formal coverage map 已生成
- formal gap report 现已生成

因此，M1 的 source-layer closeout 可以视为基本完成。
后续工作应转入：
- explicit human decision on unresolved target sources
- controlled Week-2 / pre-curation preparation
而不是直接进入 broad benchmark expansion.
