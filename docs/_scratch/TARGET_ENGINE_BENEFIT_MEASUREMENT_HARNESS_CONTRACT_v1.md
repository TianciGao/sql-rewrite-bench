# TARGET_ENGINE_BENEFIT_MEASUREMENT_HARNESS_CONTRACT_v1

## 1. Executive summary

本文是 **measurement harness contract**，不是 measurement run。

范围仅限 bounded 6-case PORT route packet：

- `PORT_0004`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

以及：

- route families: `SQLGlot Transpile`, `LLM Translate`
- target engines: `MySQL`, `Spark`

明确边界：

- 这不是完整 `27` 个 `PORT` registry case 的 closure 结论。
- 这不是 speedup run，也不是 benefit measurement run。
- `SpeedupTransferRate` 仍然 `not_computed`。

结论：

- 当前需要的不是直接发起 measurement execution。
- 当前先需要一份窄范围、可落地的 **target-engine benefit measurement harness contract**。

## 2. Required measurement unit

未来 harness 的原子测量单元必须固定为：

`case_id × route_family × target_engine`

对于每一个 cell，future harness 必须能稳定识别：

1. `source SQL artifact`
2. `candidate SQL artifact`
3. `source execution command` 或 runner input
4. `candidate execution command` 或 runner input
5. `consistency eligibility source`
6. `timing repeat count`
7. `warmup policy`
8. `timeout policy`
9. `timing output path`
10. `result summary output path`
11. `failure category field`

### 2.1 Future command contract

future harness 至少需要支持以下逻辑层输入，而不是依赖人工临时拼接：

- `case_id`
- `route_family`
- `target_engine`
- `source_sql_path`
- `candidate_sql_path`
- `validation schema / database context`
- `repeats`
- `warmup_count`
- `timeout_seconds`

### 2.2 Proposed runtime policy

当前更安全的 future contract 建议：

- `repeats = 5`
- `warmup_count = 1`
- `primary_statistic = median`
- `timeout_seconds_per_query = 60`

这只是未来 harness 的建议默认值，不是本次任务的执行决定。

### 2.3 Proposed output path contract

为了避免 case-local artifacts 与临时测量混杂，future harness 建议把输出写到 `/tmp`：

- raw timing output:
  - `/tmp/rewritebench_port_target_engine_benefit/<route_family_slug>/<target_engine>/<case_id>/timings.json`
- result summary output:
  - `/tmp/rewritebench_port_target_engine_benefit/<route_family_slug>/<target_engine>/<case_id>/summary.json`

其中：

- `route_family_slug ∈ {sqlglot_transpile, llm_translate}`
- `target_engine ∈ {mysql, spark}`

## 3. Required output schema

future measurement run 至少应输出如下 machine-readable schema：

```json
{
  "case_id": "PORT_0004",
  "route_family": "SQLGlot Transpile",
  "target_engine": "mysql",
  "source_sql_path": "cases/PORT/PORT_0004/source.sql or resolved engine-specific source artifact",
  "candidate_sql_path": "resolved route-family-specific candidate artifact",
  "source_timings_ms": [1.0, 0.9, 1.1, 1.0, 0.95],
  "candidate_timings_ms": [0.8, 0.82, 0.79, 0.81, 0.8],
  "source_summary_ms": {
    "median": 1.0,
    "mean": 0.99,
    "min": 0.9,
    "warmup": 1.2
  },
  "candidate_summary_ms": {
    "median": 0.8,
    "mean": 0.804,
    "min": 0.79,
    "warmup": 0.95
  },
  "speedup_ratio": 1.25,
  "consistency_closed": true,
  "measurement_status": "success",
  "failure_category": "none",
  "notes": ""
}
```

最少字段要求：

- `case_id`
- `route_family`
- `target_engine`
- `source_sql_path`
- `candidate_sql_path`
- `source_timings_ms`
- `candidate_timings_ms`
- `source_summary_ms`
- `candidate_summary_ms`
- `speedup_ratio`
- `consistency_closed`
- `measurement_status`
- `failure_category`
- `notes`

## 4. Existing harness inventory

### 4.1 What exists

当前仓库里已经存在可借鉴的 **PG-only speedup harness pattern**：

- `reports/formal_expansion/batch3a_speedup_preflight_v0.json`
  - 展示了 preflight record contract
  - 含 `route_eligibility`、`planned_runtime_output_path`、`planned_speedup_scoring_output_path`
- `reports/formal_expansion/batch2a_speedup_run_v0.json`
  - 展示了 measured run contract
  - 含 `source_runtime_ms_values`、`candidate_runtime_ms_values`、`source_median_runtime_ms`、`candidate_median_runtime_ms`、`speedup_ratio`
- `scripts/cli.py`
  - 存在多条 PG-only speedup preflight / run 命令
  - 说明仓库中已经有一套可借鉴的 runtime-output schema 思路

### 4.2 What does not exist

当前没有发现可直接复用的 target-engine harness，尤其缺以下能力：

- 没有现成的 `PORT × MySQL` source/candidate paired timing harness
- 没有现成的 `PORT × Spark` source/candidate paired timing harness
- 没有现成的 `SQLGlot Transpile × MySQL/Spark` route-family-specific target-engine timing harness
- 没有现成的 `LLM Translate × MySQL/Spark` route-family-specific target-engine timing harness
- 没有现成的 target-engine measurement output path contract

### 4.3 Inventory conclusion

因此当前状态是：

- **schema reference exists**
- **target-engine reusable harness does not exist yet**

## 5. Gap table

解释：

- `source_sql_artifact_identified` 表示是否已经能定位未来 target-engine measurement 的 source side input
- `candidate_sql_artifact_identified` 表示是否已经能定位未来 target-engine measurement 的 candidate side input
- `existing_timing_harness_identified` 这里要求的是 **target-engine reusable harness**，不是 PG-only harness；因此当前统一记为 `false`
- `required_output_path_defined` 这里表示仓库内现有 harness contract 是否已定义；当前仍记为 `false`

| case_id | route_family | target_engine | source_sql_artifact_identified | candidate_sql_artifact_identified | consistency_evidence_identified | existing_timing_harness_identified | required_output_path_defined | ready_for_measurement_execution_prompt | blocker | harness_gap |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `PORT_0004` | `SQLGlot Transpile` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | 同引擎 candidate input 未识别，且无 timing harness | 需要 route-family-specific candidate resolution + MySQL timing harness |
| `PORT_0004` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 route-family-specific source resolution + Spark timing harness |
| `PORT_0004` | `LLM Translate` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | 同引擎 candidate input 未识别，且无 timing harness | 需要 route-family-specific candidate resolution + MySQL timing harness |
| `PORT_0004` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 route-family-specific source resolution + Spark timing harness |
| `PORT_0012` | `SQLGlot Transpile` | `mysql` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + MySQL timing harness |
| `PORT_0012` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + Spark timing harness |
| `PORT_0012` | `LLM Translate` | `mysql` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + MySQL timing harness |
| `PORT_0012` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + Spark timing harness |
| `PORT_0013` | `SQLGlot Transpile` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | 同引擎 candidate input 未识别，且无 timing harness | 需要 candidate resolution + MySQL timing harness |
| `PORT_0013` | `SQLGlot Transpile` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + Spark timing harness |
| `PORT_0013` | `LLM Translate` | `mysql` | `true` | `false` | `true` | `false` | `false` | `false` | 同引擎 candidate input 未识别，且无 timing harness | 需要 candidate resolution + MySQL timing harness |
| `PORT_0013` | `LLM Translate` | `spark` | `false` | `true` | `true` | `false` | `false` | `false` | 同引擎 source input 未识别，且无 timing harness | 需要 source resolution + Spark timing harness |
| `PORT_0022` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 SQLGlot×MySQL paired timing contract |
| `PORT_0022` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 SQLGlot×Spark paired timing contract |
| `PORT_0022` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 LLM×MySQL paired timing contract |
| `PORT_0022` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 LLM×Spark paired timing contract |
| `PORT_0024` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | artifact binding 不清，且无 timing harness | 需要 artifact binding + SQLGlot×MySQL timing contract |
| `PORT_0024` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | artifact binding 不清，且无 timing harness | 需要 artifact binding + SQLGlot×Spark timing contract |
| `PORT_0024` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | artifact binding 不清，且无 timing harness | 需要 artifact binding + LLM×MySQL timing contract |
| `PORT_0024` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | artifact binding 不清，且无 timing harness | 需要 artifact binding + LLM×Spark timing contract |
| `PORT_0025` | `SQLGlot Transpile` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 SQLGlot×MySQL paired timing contract |
| `PORT_0025` | `SQLGlot Transpile` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 SQLGlot×Spark paired timing contract |
| `PORT_0025` | `LLM Translate` | `mysql` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 LLM×MySQL paired timing contract |
| `PORT_0025` | `LLM Translate` | `spark` | `true` | `true` | `true` | `false` | `false` | `false` | 有 generic artifacts，但无 route-family-specific target timing harness | 需要 LLM×Spark paired timing contract |

## 6. Route-family separation rule

future harness 必须保持以下规则：

1. `SQLGlot Transpile` 与 `LLM Translate` 分开计量。
2. 每个 route family 都要单独产出自己的 target-engine timing outputs。
3. 没有 route-family-specific timing evidence 前，**禁止 pooling**。
4. 只有在以下条件同时成立时，才允许以后讨论 pooled denominator：
   - 两个 route family 都在同一 6-case denominator 上完成 target-engine timing
   - 输出 schema 完全同构
   - timeout / repeats / warmup policy 一致

## 7. Non-inference boundary

这里明确不做以下推断：

- result TSVs 不是 timing arrays
- consistency closure 不是 speedup
- target-engine execution success 不是 benefit transfer
- PG-side speedup 不是 MySQL/Spark speedup
- 本 contract 不计算 `SpeedupTransferRate`

## 8. Recommended next action

下一步只建议一项：

- **prepare a narrow harness implementation prompt**

原因：

- 现有仓库里只有 PG-only speedup harness pattern，可作 schema 参考；
- 当前并没有可直接调用的 PORT target-engine reusable harness；
- 因此现在还不适合直接写 measurement execution prompt，先把 harness implementation prompt 做窄、做清楚更稳。
