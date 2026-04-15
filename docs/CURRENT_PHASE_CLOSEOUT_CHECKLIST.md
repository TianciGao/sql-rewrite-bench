# CURRENT_PHASE_CLOSEOUT_CHECKLIST

## 当前文件的定位
这不是历史纪要，而是“当前阶段最小收口检查表”。
当前目标不是继续扩 benchmark，而是把阶段口径、source 层状态、case 层状态和文档同步回正轨。

## 当前阶段的统一定义
### 当前阶段名称
State alignment / M1 closeout preparation

### 当前阶段的正确理解
- Week-1 / local bootstrap 已完成
- Batch-1 source-layer 已基本完成
- Batch-2 只局部推进
- 当前主要任务是：文档同步、source/case 状态回写、coverage-map / gap-report 收口准备
- 当前仍 **未进入大规模 workload curation / benchmark expansion**

## 已确认完成
- PostgreSQL smoke passed
- MySQL smoke passed
- Spark smoke passed
- `PERF_0001` tri-engine consistency closure passed
- first plan artifacts collected
- initial commit completed
- four anchor cases established
- `PERF_0002` admitted as first external common-core case
- `PORT_0002` admitted as second external common-core case
- VeriEQL accepted as Batch-2 consistency supplement source
- `CONS_0003` / `CONS_0004` materialized from VeriEQL line
- `CONS_0003` and `CONS_0004` are now both PG+MySQL validated staged consistency drafts

## 当前必须回写到文档的事实
1. `PORT_0002` 不应再被描述为 common-core candidate
2. VeriEQL 已不再是“待二选一”的 pending source，而是已接受分支
3. `CONS_0004` 当前应保留为 PG+MySQL validated staged draft，不应被误写为 admitted
4. Manual Seed Cases 是 `manual_seed` source family，不是第五个 pool
5. Stack 目前拿到的是 dumps / substrate，而不是 direct SQL query corpus
6. DSB 仍然在目标源全集里，但不应被误写成已完成 acquisition / inspection

## 当前未闭合事项
### A. 文档同步
- [ ] 更新 `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
- [ ] 更新 `benchmark_spec/decision_log.md`
- [ ] 更新 `docs/DOC_MAP.md`
- [ ] 更新 `inventory/source_registry.csv` 或生成 aligned snapshot

### B. M1 正式收口所需
- [ ] 输出 formal coverage map
- [ ] 输出 formal gap report
- [ ] 识别并冻结下一轮优先补齐的 feature buckets

### C. Batch-2 未闭合 source 事项
- [ ] 明确 Stack 是否具备 direct SQL query corpus
- [ ] 明确 JOB 线是继续扩 probe 还是暂时冻结为 partial
- [ ] 明确 DSB 是继续保留为 target source 还是启动 acquisition

## 当前明确不做的事
- 不新增 benchmark workloads
- 不新增 benchmark cases
- 不改 benchmark protocol files 的语义边界
- 不启动广义 workload curation
- 不进入 baseline 主实验

## 当前阶段的完成条件
当前阶段可以视为完成，当且仅当：
1. phase / source / case / admission 文档已经同步
2. formal coverage map 已生成
3. formal gap report 已生成
4. source-universe 与 actual-progress 的差异已被显式记录
