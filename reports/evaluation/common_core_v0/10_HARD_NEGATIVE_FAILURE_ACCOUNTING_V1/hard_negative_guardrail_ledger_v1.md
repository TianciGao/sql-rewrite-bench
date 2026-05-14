# Hard-negative Guardrail Ledger v1

## Purpose

这个文件回答什么问题：把 Common-core v0 case-package hard-negative controls 变成 paper-facing per-case/per-engine ledger，并明确它评估的是 package negative controls，不是 method-generated candidates。

## Denominator

- planned cells: `120`
- tested cells: `111`
- blocked / not applicable cells: `9`
- engine scope: `same_engine_pg_mysql_spark` package negative controls

## Overall result

- rejected negative rows: `111`
- false accepts: `0`
- normalized rejection modes: `{'executable_semantic_mismatch': 111, 'not_applicable': 9}`

## Per-pool summary

| pool | planned | tested | blocked/not_applicable | rejected | false_accept |
| --- | --- | --- | --- | --- | --- |
| PERF | 48 | 48 | 0 | 48 | 0 |
| CONS | 27 | 27 | 0 | 27 | 0 |
| PORT | 27 | 18 | 9 | 18 | 0 |
| LONGTAIL | 18 | 18 | 0 | 18 | 0 |

## What counts as executable semantic rejection

- `executable_semantic_mismatch` means source and negative rewrite both executed, the retained checker ran, and the negative row was rejected because results did not match.
- `execution_failure_rejection` would mean the negative rewrite failed execution and was therefore rejected, but the retained packet has zero such tested rows.
- `not_applicable` rows stay in the planned denominator and must not be silently dropped.

## What this supports

- Package hard-negative control validation for Section 8.6.2.
- A denominator-aware statement that tested hard negatives were rejected without false accepts, when supported by retained artifacts.
- Per-pool visibility into tested versus blocked cells.

## What this does not support

- This does not evaluate method-generated candidate failures.
- This does not prove general SQL equivalence.
- This does not audit accepted generated candidates for hidden false accepts.

## Safe prose snippet for the paper

This table evaluates package hard-negative controls, not method-generated candidates. In the retained Common-core v0 packet, 111 tested hard negatives are executable semantic mismatches rejected by the checker, with 9 planned cells remaining explicitly not applicable and 0 retained false accepts. This evidence strengthens denominator-aware guardrail reporting, but it does not prove general SQL equivalence.
