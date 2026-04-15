# EXTERNAL_DRAFT_CASE_STATUS

## 文件定位
本文件只跟踪“外部来源派生的非锚点 case”与其 admission / staged 状态。
锚点 case（`0001` 系列）不在本文件中重复维护。

## 1. 已 admission 的 external common-core
| case_id | pool | source | 当前状态 | 当前解释 |
|---|---|---|---|---|
| PERF_0002 | performance | TPC-DS query53.tpl | admitted external common-core | 当前最成熟的 performance 外部 case，不再视为 draft |
| PORT_0002 | portability | PARROT / BIRD | admitted external common-core | 当前最成熟的 portability 外部 case，不再视为 candidate |

## 2. 仍保持 staged / not_yet_admitted 的 external drafts
| case_id | pool | source | 当前状态 | 当前验证层级 | immediate next action |
|---|---|---|---|---|---|
| LONGTAIL_0002 | longtail | SQLStorm / source_12033 | staged, not_yet_admitted | PG validated draft with positive / negative pair | 保持 staged；不强推 admission |
| CONS_0002 | consistency | Calcite `new-decorr.iq` seed | staged, not_yet_admitted | PG validated draft | 保持 staged；等待是否继续 broader engine validation |
| PERF_0003 | performance | JOB 27a | staged performance draft | PG-only validation | 保持 partial，不误写为 source-universe fully complete |
| PERF_0004 | performance | JOB 30b | staged performance draft | PG validated with positive / negative pair | 保持 staged |
| CONS_0003 | consistency | VeriEQL Calcite-397/159 | staged consistency draft | PostgreSQL / MySQL / Spark validated | 保持 staged；当前不立即推进 admission |
| CONS_0004 | consistency | VeriEQL Calcite-397/362 | staged consistency draft | PostgreSQL / MySQL / Spark validated | 保持 staged；当前不立即推进 admission |

## 3. 明确写死的状态修正
### 3.1 PORT_0002
如果历史文本仍将 `PORT_0002` 写成：
- common-core candidate
- strong portability candidate
- Spark still missing

则这些描述已经过时，应统一修正为：
- admitted external common-core portability case

### 3.2 CONS_0004
如果历史文本仍暗示 `CONS_0004` 应立即继续深挖或推进 admission，应统一修正为：
- current status: PG + MySQL validated staged draft
- immediate deepening: not required now
- recommended action: keep frozen as staged until the next deliberate consistency deepening pass
- real next gap: Spark closure, not immediate admission

### 3.3 VeriEQL 分支
如果历史文本仍写“SQLEquiQuest / VeriEQL 待二选一”，则在当前仓库口径下应修正为：
- current branch chosen: VeriEQL
- SQLEquiQuest remains an optional future alternative, not the current active supplement source
