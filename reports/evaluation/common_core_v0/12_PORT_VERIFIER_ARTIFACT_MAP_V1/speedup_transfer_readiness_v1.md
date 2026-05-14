# Speedup Transfer Readiness v1

## Purpose

这个文件回答什么问题：说明 Section 8.8 中为什么 `SpeedupTransferRate` 仍然不能计算，以及还缺什么证据。

## Readiness matrix

| case_id | route_family | method_id | target_engine | paired_benefit_ready | speedup_transfer_rate_computable | blocker |
| --- | --- | --- | --- | --- | --- | --- |
| bounded_PORT6_summary | sqlglot_transpile_portability_route | sqlglot | mysql_and_spark_from_pg_side_packet | no | no | missing_paired_target_engine_timing |
| bounded_PORT6_summary | llm_translate_portability_route | direct_llm | pg_mysql_spark_bounded_port_packet | no | no | missing_paired_target_engine_timing |
| bounded_PORT6_summary | bounded_port_route_packet_context | NA_not_method_row | pg_mysql_spark | no | no | missing_paired_target_engine_timing |

## Why SpeedupTransferRate is not computed

- No retained bounded PORT row has paired target-engine source timing plus candidate timing arrays.
- No retained bounded PORT row has an equivalent repeated runtime summary sufficient for transfer-speed computation.
- Same-engine timing slices from Track A cannot be reused as Track C transfer-speed evidence.

## Required evidence for future computation

- Paired target-engine source/candidate timing arrays for the same bounded route/case/target engine, or
- Repeated target-engine runtime summaries with equivalent comparability guarantees.

## Safe prose snippet for the paper

SpeedupTransferRate remains not computed in Common-core v0. The blocker is missing paired target-engine source/candidate timing arrays or repeated runtime summaries. Cross-engine execution/consistency closure is not the same as transfer-speed readiness.
