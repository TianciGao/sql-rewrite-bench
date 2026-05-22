# PORT Bounded Route Closure v1

## Purpose

这个文件回答什么问题：把 Section 8.8.2 的 retained PORT closure evidence 明确限制在 bounded PORT6，而不是 full PORT9 或 full PORT registry。

## Bounded denominator

- Denominator scope is `bounded_PORT6` only.
- Track C portability evidence remains separate from Track A same-engine rewrite.

## Route closure table

| case_id | route_family | method_id | target_engine | executed | consistent | closure_status | denominator_scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bounded_PORT6_summary | sqlglot_transpile_portability_route | sqlglot | mysql_and_spark_from_pg_side_packet | 1/6 | 1/6 | bounded_partial_execution_consistency | bounded_PORT6 |
| bounded_PORT6_summary | llm_translate_portability_route | direct_llm | pg_mysql_spark_bounded_port_packet | 6/6 | 6/6 | bounded_port6_execution_consistency_closed | bounded_PORT6 |
| bounded_PORT6_summary | bounded_port_route_packet_context | NA_not_method_row | pg_mysql_spark | summary_context | summary_context | bounded_port6_context_only | bounded_PORT6 |

## What is closed

- The retained bounded packet supports bounded PORT6 execution / consistency closure lines.
- `LLM Translate` retains a bounded `6/6` execution / consistency closure line in the freeze layer.
- `SQLGlot Transpile` retains bounded portability-route evidence only, with retained executable / consistent subset counts of `1/6` rather than a full PORT closure claim.

## What is not closed

- Not full PORT9 closure.
- Not full PORT registry closure.
- Not transfer-speed readiness.

## Safe prose snippet for the paper

Current evidence supports bounded PORT6 execution / consistency closure. It does not support full PORT9 closure or full PORT registry closure. It also does not support transfer-speed conclusions.
