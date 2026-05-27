# FORMAL_COMMON_CORE_PLAN_OPERATOR_DELTA_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the formal common-core plan operator-delta summary state.

This note is based only on the existing operator-delta preflight report.

## 2. Input Report

- `reports/formal_common_core/plan_operator_delta_preflight_v0.json`
- `reports/formal_common_core/plan_operator_delta_summary_v0.json`

## 3. Pair Summary

### 3.1 source-positive

- `pair_count=9`
- `ready_pair_count=9`
- `top_node_changed_count=2`
- `top_node_changed_rate=0.2222222222222222`
- `node_count_delta_min=0`
- `node_count_delta_max=6`
- `node_count_delta_mean=0.8888888888888888`
- `cases_with_added_node_types=[CONS_0007, CONS_0012]`
- `cases_with_removed_node_types=[CONS_0012]`
- `most_common_added_node_types=[["Aggregate", 2], ["Hash", 2], ["Hash Join", 2]]`
- `most_common_removed_node_types=[["Limit", 1]]`

Representative examples:

- `CONS_0007`: top node changed `Seq Scan -> Hash Join`; `node_count_delta=6`; added `Aggregate`, `Hash`, `Hash Join`
- `CONS_0012`: top node changed `Seq Scan -> Hash Join`; `node_count_delta=2`; added `Aggregate`, `Hash`, `Hash Join`; removed `Limit`
- `PERF_0006`: top node unchanged `Sort`; `node_count_delta=0`

### 3.2 source-negative

- `pair_count=9`
- `ready_pair_count=9`
- `top_node_changed_count=2`
- `top_node_changed_rate=0.2222222222222222`
- `node_count_delta_min=0`
- `node_count_delta_max=3`
- `node_count_delta_mean=0.5555555555555556`
- `cases_with_added_node_types=[CONS_0007, CONS_0012]`
- `cases_with_removed_node_types=[CONS_0012]`
- `most_common_added_node_types=[["Aggregate", 2], ["Hash", 2], ["Hash Join", 2]]`
- `most_common_removed_node_types=[["Limit", 1]]`

Representative examples:

- `CONS_0007`: top node changed `Seq Scan -> Hash Join`; `node_count_delta=3`; added `Aggregate`, `Hash`, `Hash Join`
- `CONS_0012`: top node changed `Seq Scan -> Hash Join`; `node_count_delta=2`; added `Aggregate`, `Hash`, `Hash Join`; removed `Limit`
- `PERF_0006`: top node unchanged `Sort`; `node_count_delta=0`

### 3.3 source-SQLGlot

- `pair_count=9`
- `ready_pair_count=9`
- `top_node_changed_count=0`
- `top_node_changed_rate=0.0`
- `node_count_delta_min=0`
- `node_count_delta_max=0`
- `node_count_delta_mean=0.0`
- `cases_with_added_node_types=[]`
- `cases_with_removed_node_types=[]`
- `most_common_added_node_types=[]`
- `most_common_removed_node_types=[]`

Representative examples:

- `CONS_0007`: top node unchanged `Seq Scan`; `node_count_delta=0`
- `CONS_0012`: top node unchanged `Seq Scan`; `node_count_delta=0`
- `PERF_0006`: top node unchanged `Sort`; `node_count_delta=0`

### 3.4 source-LLM

- `pair_count=9`
- `ready_pair_count=9`
- `top_node_changed_count=1`
- `top_node_changed_rate=0.1111111111111111`
- `node_count_delta_min=0`
- `node_count_delta_max=2`
- `node_count_delta_mean=0.2222222222222222`
- `cases_with_added_node_types=[CONS_0007]`
- `cases_with_removed_node_types=[]`
- `most_common_added_node_types=[["Hash", 1], ["Hash Join", 1]]`
- `most_common_removed_node_types=[]`

Representative examples:

- `CONS_0007`: top node changed `Seq Scan -> Hash Join`; `node_count_delta=2`; added `Hash`, `Hash Join`
- `CONS_0012`: top node unchanged `Seq Scan`; `node_count_delta=0`
- `PERF_0006`: top node unchanged `Sort`; `node_count_delta=0`

## 4. Cross-Pair Observation

- all four pair types are `9 / 9` ready
- the strongest structural movement appears in `source-positive` and `source-negative`, concentrated in `CONS_0007` and `CONS_0012`
- `source-SQLGlot` is structurally unchanged across all `9 / 9` cases under this lightweight operator-delta view
- `source-LLM` shows one visible top-node change, in `CONS_0007`

## 5. Boundary

- operator-delta observation only
- not attribution
- not speedup
- not performance explanation
- no SQL was executed
- no EXPLAIN was run
- no new plans were collected

## 6. Recommended Next Step

- use this summary as input for a separate attribution-design step, rather than treating operator deltas as performance conclusions
