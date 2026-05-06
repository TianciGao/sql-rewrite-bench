# TARGET_ENGINE_BENEFIT_MEASUREMENT_READINESS_PREFLIGHT_v1

## 1. Executive summary

结论：bounded 6-case PORT route packet 的 **target-engine benefit measurement 仍然 not ready**。

当前边界仅限：

- `PORT_0004`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

以及以下 route family：

- `SQLGlot Transpile`
- `LLM Translate`

明确边界：

- 这不是完整 `27` 个 `PORT` registry case 的结论。
- 当前只确认了 bounded packet 的 execution/consistency closure，不代表已经具备 target-engine benefit measurement 条件。
- `SpeedupTransferRate` 仍然**没有计算**。

## 2. Required evidence definition

在当前 bounded packet 上，要进入 target-engine benefit measurement，至少需要以下证据：

1. 每个 target engine 上都有可复用的 source SQL / baseline artifact。
2. 每个 route family 在每个 target engine 上都有可复用的 candidate artifact。
3. candidate 已通过一致性门槛，能合法进入 benefit denominator。
4. source 侧有 timing array 或 repeated runtime summary。
5. candidate 侧有 timing array 或 repeated runtime summary。
6. source 与 candidate 能在同一 engine、同一 case、同一路由口径下做 paired benefit 对比。
7. route family 必须分开：
   - `SQLGlot Transpile`
   - `LLM Translate`
8. engine 也必须分开：
   - `mysql`
   - `spark`

换句话说，execution success、result TSV、case-local `result_check.json` 都只是前置条件，不是 benefit measurement 本身。

## 3. Readiness matrix

说明：

- `source_artifact_present` / `candidate_artifact_present` 仅表示当前是否发现了可复用的 target-engine result artifact。
- 对于部分 case，即便 generic source/candidate TSV 都存在，也没有看到 route-family-specific target-engine timing evidence。
- 因此本表中 `measurement_ready` 全部仍为 `false`。

| case_id | route_family | target_engine | source_artifact_present | candidate_artifact_present | consistency_closed | source_timing_present | candidate_timing_present | paired_benefit_inputs_ready | measurement_ready | blocker | suggested_next_step |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `PORT_0004` | `SQLGlot Transpile` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 `source.tsv`，无同引擎 candidate artifact，也无 timing | 明确该 cell 是否需要 route-family-specific MySQL candidate 路径与 timing harness |
| `PORT_0004` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 明确该 cell 是否需要 route-family-specific Spark source 路径与 timing harness |
| `PORT_0004` | `LLM Translate` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 `source.tsv`，无同引擎 candidate artifact，也无 timing | 明确该 cell 是否需要 route-family-specific MySQL candidate 路径与 timing harness |
| `PORT_0004` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 明确该 cell 是否需要 route-family-specific Spark source 路径与 timing harness |
| `PORT_0012` | `SQLGlot Transpile` | `mysql` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 补齐 route-family-specific MySQL source artifact contract 与 timing harness |
| `PORT_0012` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 补齐 route-family-specific Spark source artifact contract 与 timing harness |
| `PORT_0012` | `LLM Translate` | `mysql` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 补齐 route-family-specific MySQL source artifact contract 与 timing harness |
| `PORT_0012` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 补齐 route-family-specific Spark source artifact contract 与 timing harness |
| `PORT_0013` | `SQLGlot Transpile` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 `source.tsv`，无同引擎 candidate artifact，也无 timing | 明确 route-family-specific MySQL candidate 物化与 timing harness |
| `PORT_0013` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 明确 route-family-specific Spark source 物化与 timing harness |
| `PORT_0013` | `LLM Translate` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | `false` | MySQL 仅见 `source.tsv`，无同引擎 candidate artifact，也无 timing | 明确 route-family-specific MySQL candidate 物化与 timing harness |
| `PORT_0013` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | `false` | Spark 仅见 candidate TSV，无同引擎 source artifact，也无 timing | 明确 route-family-specific Spark source 物化与 timing harness |
| `PORT_0022` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 SQLGlot×MySQL 建立 source/candidate repeated runtime contract |
| `PORT_0022` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 SQLGlot×Spark 建立 source/candidate repeated runtime contract |
| `PORT_0022` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 LLM Translate×MySQL 建立 source/candidate repeated runtime contract |
| `PORT_0022` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 LLM Translate×Spark 建立 source/candidate repeated runtime contract |
| `PORT_0024` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic MySQL source/candidate TSV 已有，但无 timing arrays；且 route-family-specific target binding未建立 | 为 SQLGlot×MySQL 明确 artifact binding 与 repeated runtime contract |
| `PORT_0024` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic Spark source/candidate TSV 已有，但无 timing arrays；且 route-family-specific target binding未建立 | 为 SQLGlot×Spark 明确 artifact binding 与 repeated runtime contract |
| `PORT_0024` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic MySQL source/candidate TSV 已有，但无 timing arrays；且 route-family-specific target binding未建立 | 为 LLM Translate×MySQL 明确 artifact binding 与 repeated runtime contract |
| `PORT_0024` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic Spark source/candidate TSV 已有，但无 timing arrays；且 route-family-specific target binding未建立 | 为 LLM Translate×Spark 明确 artifact binding 与 repeated runtime contract |
| `PORT_0025` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 SQLGlot×MySQL 建立 source/candidate repeated runtime contract |
| `PORT_0025` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 SQLGlot×Spark 建立 source/candidate repeated runtime contract |
| `PORT_0025` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 LLM Translate×MySQL 建立 source/candidate repeated runtime contract |
| `PORT_0025` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | `false` | generic source/candidate TSV 已有，但无 route-family-specific target timing evidence | 为 LLM Translate×Spark 建立 source/candidate repeated runtime contract |

## 4. Route-family denominator check

当前更安全的判断是：

- `SQLGlot Transpile` 与 `LLM Translate` 只能先作为 **separate denominator rows** 讨论。
- 现在**不适合 pooled**。

原因：

- PG-side route family 可识别，但 target-engine artifacts 目前大多还是 case-local generic closure artifacts；
- 还没有看到按 `SQLGlot Transpile` / `LLM Translate` 分开组织的 MySQL/Spark timing evidence；
- 因此即便 execution/consistency 已闭环，transfer/beneift denominator 仍未真正对齐。

## 5. Non-inference boundary

这里明确不做以下推断：

- consistency closure 不是 speedup
- PG-side speedup 不是 MySQL/Spark speedup
- result TSV 不是 timing arrays
- execution success 不是 benefit transfer

更具体地说：

- case-local `result_check.json` 只能证明 candidate 可进入“可测量候选集合”
- case-local `source.tsv` / `rewrite_pos_01.tsv` 只能证明结果物化存在
- 只有 target-engine 上成对的 source/candidate repeated runtime evidence，才能进入 benefit measurement

## 6. Final recommendation

下一步只建议一项：

- **prepare a narrow measurement-harness gap prompt**

原因：

- 当前真正缺口不是 execution closure，而是 measurement harness 输入不全；
- 部分 case-engine cell 连 source/candidate 成对 artifact 都不完整；
- 其余 cell 即便 artifact 成对，也缺 route-family-specific target-engine timing arrays 或 repeated runtime summaries；
- 因此现在更需要一个窄范围 harness-gap prompt，而不是直接发起 benefit measurement execution prompt。
