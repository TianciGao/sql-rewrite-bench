# SPEEDUP_TRANSFER_RATE_READINESS_PREFLIGHT_v1

## 1. Executive summary

结论：`SpeedupTransferRate` 目前**尚未 ready**，不能计算。

这个结论仅针对当前已确认闭环的 **PORT 有界 6-case route packet**：

- `PORT_0004`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

边界说明：

- 这里只确认了该 6-case packet 的 PG-side route 闭环与跨引擎执行/一致性闭环。
- 这**不是**完整 `27` 个 `PORT` registry case 的 closure 结论。
- 本次仅做 readiness preflight，**没有计算** `SpeedupTransferRate`。

## 2. Current confirmed closure

当前已确认：

- PG-side route closure：`6/6`
- cross-engine execution/consistency closure：`6/6`
- cases：`PORT_0004, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025`

这说明：

- SQLGlot Transpile / LLM Translate 在该 bounded packet 上已经具备执行与结果一致性闭环证据；
- 但这仍然不等于已经具备 target-engine benefit / speedup transfer 证据。

## 3. Metric readiness definition

在当前仓库语境下，要计算 `SpeedupTransferRate`，至少需要以下证据同时成立：

1. 固定且可说明的 route-family denominator。
   - `SQLGlot Transpile` 单独算，或
   - `LLM Translate` 单独算，或
   - 两者分别成表；只有在证据完全同构时才考虑 pooled。

2. 每个 case 在每个 target engine 上都要有可识别的 source timing / baseline timing。

3. 同一 target engine 上要有与 source 成对的 candidate / rewrite timing。

4. timing 必须能支撑 paired source-vs-candidate benefit 判断，而不仅仅是单次执行成功。

5. candidate 必须已通过一致性门槛，才能进入 transfer 指标分母。

6. 需要有足够 machine-readable 的 timing arrays、median/mean 摘要或等价结构，能稳定算出每 case 的 transfer outcome。

## 4. Existing evidence inventory

当前扫描结果显示，6 个 case 都已经发现：

- target-engine 结果 TSV
- case-local `runs/mysql/result_check.json`
- case-local `runs/spark/result_check.json`
- route-family 可识别的 PG-side artifacts

但当前没有发现能够直接支撑 `SpeedupTransferRate` 的同分母 target-engine timing 证据：

- 未发现明确的 MySQL source timing arrays
- 未发现明确的 MySQL candidate timing arrays
- 未发现明确的 Spark source timing arrays
- 未发现明确的 Spark candidate timing arrays
- 未发现按 `SQLGlot Transpile` / `LLM Translate` 拆分、且可直接映射到 6-case packet 的 target-engine benefit 汇总

补充说明：

- `reports/formal_port/result_checks/...` 和 `reports/formal_expansion/port_batch2c/result_checks/...` 中可见 route-family-specific `result_check` 证据；
- 部分 PG-side route result checks 含 `runtime_ms` 字段；
- 这些更接近 PG-side route execution metadata，不是 MySQL/Spark 上的 paired speedup / benefit measurement。

## 5. Readiness table

| case_id | execution_consistency_closed | mysql_source_timing_present | mysql_candidate_timing_present | spark_source_timing_present | spark_candidate_timing_present | route_family_identifiable | speedup_transfer_ready | blocker |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `PORT_0004` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |
| `PORT_0012` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |
| `PORT_0013` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |
| `PORT_0022` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |
| `PORT_0024` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |
| `PORT_0025` | `true` | `false` | `false` | `false` | `false` | `true` | `false` | 缺少 MySQL/Spark 成对 timing / benefit 证据 |

## 6. Route-family denominator decision

当前更安全的 denominator 选择是：

- `SQLGlot Transpile` 单独一行
- `LLM Translate` 单独一行

不建议现在直接 pooled，原因是：

- route-family evidence 分散在不同 report tree 中；
- 当前可确认的是 execution/consistency closure，而不是完全同构的 target-engine timing evidence；
- 在 benefit measurement 尚未建立前，提前 pooling 会放大解释风险。

## 7. Non-inference boundary

这里明确不做以下推断：

- result consistency **不是** speedup transfer
- PG-side speedup **不是** target-engine speedup
- cross-engine execution success **不是** benefit transfer
- target-engine result TSV **不是** speedup evidence
- 只有 target-engine 上成对的 source/candidate timing or benefit evidence，才能支撑 `SpeedupTransferRate`

## 8. Final recommendation

下一步只建议一项：

- 为同一个 bounded 6-case PORT route packet，按 route family 分开，先做 **target-engine benefit measurement preflight**

建议理由：

- execution/consistency closure 已经完成 `6/6`
- 当前真正缺口已经从“能不能跑通”转为“有没有 aligned target-engine benefit evidence”
- 只有先把 benefit measurement denominator、artifact contract、route-family separation 说清，后续 `SpeedupTransferRate` 才有可计算基础
