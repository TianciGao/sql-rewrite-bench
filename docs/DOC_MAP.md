# DOC_MAP

## 1. 当前主线文档
以下文件应被视为当前主线：
- `docs/PROJECT_PLAN.md`：总体目标、研究主张、四池结构、目标源全集、v1 范围
- `benchmark_spec/decision_log.md`：冻结决策和阶段性回写
- `docs/CURRENT_PHASE_CLOSEOUT_CHECKLIST.md`：当前阶段的最小收口定义
- `docs/STATE_ALIGNMENT_MATRIX.md`：目标 / 实际 / 漂移 的汇总矩阵
- `docs/EXTERNAL_DRAFT_CASE_STATUS.md`：external case 状态层
- `inventory/target_source_status_snapshot.csv`：目标源全集 vs 当前真实状态

## 2. 当前辅助文档
- `docs/ANCHOR_CASE_SUMMARY.md`：锚点层总结
- `docs/INVENTORY_TEMPLATE.md`：inventory 结构模板
- `paper/notes_status_alignment_closeout.md`：阶段性状态记录

## 3. 历史快照 / 不应再被视为当前 source of truth 的文件
- `docs/archive/benchmark_spec_v0.md`
- `docs/archive/case_schema_v0.1.yaml`

这些文件可以保留，但应被明确标记为：
- 历史快照
- 早期执行边界草稿
- 不再单独代表当前主线状态

## 4. 需要避免的混读
### 混读类型 A
把 `PROJECT_PLAN.md` 的目标源全集，误读成“已完成 acquisition / inspection 的来源清单”。

### 混读类型 B
把 case 层的 four-pool 归档规则，误用到 source 层。

### 混读类型 C
把 Week-1 bootstrap 状态，误等同于整个 benchmark 项目的当前阶段。

## 5. 当前建议阅读顺序
1. `benchmark_spec/decision_log.md`
2. `docs/PROJECT_PLAN.md`
3. `docs/CURRENT_PHASE_CLOSEOUT_CHECKLIST.md`
4. `docs/STATE_ALIGNMENT_MATRIX.md`
5. `docs/EXTERNAL_DRAFT_CASE_STATUS.md`
6. `inventory/target_source_status_snapshot.csv`
