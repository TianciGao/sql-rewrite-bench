# Direct LLM @40 Same-Engine Validity Summary v1

## Scope

This summary materializes denominator-aware validity evidence for:

- `denominator_id = common_core_v0_40`
- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`

Inputs used:

- [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/run_results.json)
- [execution_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/execution_triage.md)
- [execution_triage.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/execution_triage.csv)
- [generation_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generation_triage.md)
- [generation run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/run_results.json)
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_matrix.csv`
- `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv`
- `reports/curation/common_core_v0_final_denominator.csv`
- `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`

This is **Direct LLM validity/execution evidence only**. It is **not** timing evidence, speedup evidence, or leaderboard evidence.

## Headline Counts

- planned rows: `120`
- generation_success rows: `120`
- ready_to_execute rows: `115`
- preflight_blocked rows: `5`
- executed rows: `99`
- execution_failed rows: `16`
- match_exact rows: `94`
- mismatch rows: `5`

Outcome interpretation:

- `preflight_blocked` rows are package or artifact gaps and are **not** counted as LLM-generated SQL failures
- `execution_failed` rows are method or execution failures unless triage explicitly marked them as draft DDL or package limitation
- `mismatch` rows executed successfully but were not consistency-valid
- all PORT rows retain portability-stress caveats

## Rate Definitions

- `generation_success_rate`: `generation_success / planned`
- `executable_rate over planned`: `executed / planned`
- `executable_rate over ready_to_execute`: `executed / ready_to_execute`
- `result_consistency_rate`: `match_exact / denominator`
- `preflight_blocked_rate`: `preflight_blocked / planned`
- `execution_failed_rate`: `execution_failed / denominator`
- `mismatch_rate`: `mismatch / denominator`

I am also surfacing `ready_to_execute / planned` as a separate preflight-coverage statistic because it explains the blocked slice explicitly.

## Headline Rates

| metric | formula | value |
|---|---|---:|
| generation_success_rate over planned | `120 / 120` | `100.00%` |
| executable_rate over planned | `99 / 120` | `82.50%` |
| executable_rate over ready_to_execute | `99 / 115` | `86.09%` |
| preflight ready coverage over planned | `115 / 120` | `95.83%` |
| result_consistency_rate over planned | `94 / 120` | `78.33%` |
| result_consistency_rate over executed | `94 / 99` | `94.95%` |
| result_consistency_rate over ready_to_execute | `94 / 115` | `81.74%` |
| preflight_blocked_rate over planned | `5 / 120` | `4.17%` |
| execution_failed_rate over planned | `16 / 120` | `13.33%` |
| execution_failed_rate over ready_to_execute | `16 / 115` | `13.91%` |
| mismatch_rate over executed | `5 / 99` | `5.05%` |
| mismatch_rate over ready_to_execute | `5 / 115` | `4.35%` |

## Outcome-Class Summary

| outcome_class | rows | rate over planned |
|---|---:|---:|
| `match_exact` | 94 | `78.33%` |
| `mismatch` | 5 | `4.17%` |
| `execution_failed` | 16 | `13.33%` |
| `not_executed_preflight_blocked` | 5 | `4.17%` |

Execution-failed subclass split from triage:

- `14/16` execution-failed rows were triaged as `llm_generated_sql_dialect_execution_failure`
- `2/16` execution-failed rows were triaged as `draft_ddl_package_limitation`

Those `2` package-limitation rows are:

- `PERF_0077 / spark`
- `PORT_0004 / spark`

## By Pool

| pool | planned | ready_to_execute | preflight_blocked | executed | match_exact | mismatch | execution_failed | match_exact rate over planned |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| consistency | 27 | 27 | 0 | 27 | 24 | 3 | 0 | `88.89%` |
| longtail | 18 | 18 | 0 | 16 | 16 | 0 | 2 | `88.89%` |
| performance | 48 | 48 | 0 | 46 | 45 | 1 | 2 | `93.75%` |
| portability | 27 | 22 | 5 | 10 | 9 | 1 | 12 | `33.33%` |

Pool notes:

- `consistency` is the only pool with multi-engine mismatch concentration, driven entirely by `CONS_0024`
- `performance` has the strongest planned-denominator exact-match rate at `93.75%`
- `portability` is intentionally stress-heavy and should not be normalized into ordinary same-engine claims

## By Engine

| engine | planned | ready_to_execute | preflight_blocked | executed | match_exact | mismatch | execution_failed | match_exact rate over planned |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mysql | 40 | 38 | 2 | 36 | 34 | 2 | 2 | `85.00%` |
| pg | 40 | 39 | 1 | 33 | 32 | 1 | 6 | `80.00%` |
| spark | 40 | 38 | 2 | 30 | 28 | 2 | 8 | `70.00%` |

Engine notes:

- `spark` has the weakest exact-match coverage and the highest execution-failure share
- `pg` carries several dialect-sensitive failures in PORT rows
- `mysql` has the strongest engine-level exact-match rate

## Pool × Engine

| pool | engine | planned | match_exact | mismatch | execution_failed | preflight_blocked |
|---|---|---:|---:|---:|---:|---:|
| consistency | mysql | 9 | 8 | 1 | 0 | 0 |
| consistency | pg | 9 | 8 | 1 | 0 | 0 |
| consistency | spark | 9 | 8 | 1 | 0 | 0 |
| longtail | mysql | 6 | 6 | 0 | 0 | 0 |
| longtail | pg | 6 | 5 | 0 | 1 | 0 |
| longtail | spark | 6 | 5 | 0 | 1 | 0 |
| performance | mysql | 16 | 16 | 0 | 0 | 0 |
| performance | pg | 16 | 15 | 0 | 1 | 0 |
| performance | spark | 16 | 14 | 1 | 1 | 0 |
| portability | mysql | 9 | 4 | 1 | 2 | 2 |
| portability | pg | 9 | 4 | 0 | 4 | 1 |
| portability | spark | 9 | 1 | 0 | 6 | 2 |

The pool-by-engine stress concentration is clear:

- `portability / spark` is the weakest slice with `1/9` exact matches and `6/9` execution failures
- `performance / mysql` is the cleanest slice with `16/16` exact matches

## Interpretation Boundaries

This summary should be read with the following boundaries intact:

- `5` preflight-blocked rows are package gaps, not generated-SQL failures
- `16` execution-failed rows are not interchangeable with `5` mismatches
- `5` mismatches are executed rows and therefore count against validity, not executability
- PORT rows must keep portability-stress caveats explicit, especially where `controls_native_source_status=skipped` appears in the execution package
- `PORT_0013 / spark` stayed on the generation watchlist and then failed during execution

## Recommendation

This validity summary is ready to serve as the denominator-aware Direct LLM same-engine validity artifact for Common-core v0.

It should **not** yet be turned into:

- timing comparisons
- speedup reporting
- a Direct LLM versus SQLGlot leaderboard

Those layers remain incomplete for Direct LLM and would overclaim beyond the current evidence.
