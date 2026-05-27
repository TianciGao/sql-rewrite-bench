# EXPANDED_PORT_RESULTS_CLOSEOUT_v0

## 1. Status

This is expanded PORT results closeout v0.

It consolidates the current RQ3 / PORT evidence after the seed PORT packet and the Batch 2C PORT expansion.

## 2. Executive Summary

Current consolidated PORT evidence should now be read in four explicit layers.

1. PG-side PORT evidence:
   - denominator: `6` PORT cases
   - SQLGlot Transpile remains PG-side only and partial
   - LLM Translate remains PG-side only on the bounded slice
   - claim boundary: PostgreSQL-side portability evidence only, not cross-engine closure
2. Cross-engine feasibility preflight:
   - denominator: `6` PORT cases
   - `mysql_ready_count=3`
   - `spark_ready_count=3`
   - `both_engine_ready_count=3`
   - recommended bounded execution subset: `PORT_0022`, `PORT_0024`, `PORT_0025`
   - blocked before execution:
     - `PORT_0004`: witness-file contract not normalized
     - `PORT_0012`: datetime_formatting / dialect_functions
     - `PORT_0013`: boolean_aggregation
   - claim boundary: `preflight_only_not_cross_engine_closure`
3. Bounded MySQL+Spark execution attempt:
   - denominator: `3` approved cases x `2` engines
   - approved cases: `PORT_0022`, `PORT_0024`, `PORT_0025`
   - MySQL execution occurred: yes
   - Spark execution occurred: yes
   - PostgreSQL execution occurred: no
   - model calls: no
   - SQLGlot: no
   - claim boundary: `bounded_3_case_mysql_spark_execution_not_full_port_closure`
4. Actual bounded result:
   - `mysql_execution_success_count=1`
   - `mysql_consistency_success_count=1`
   - `spark_execution_success_count=1`
   - `spark_consistency_success_count=1`
   - `both_engine_execution_success_count=1`
   - `both_engine_consistency_success_count=1`
   - only `PORT_0024` closed on both engines
   - `PORT_0024` required the existing normalized numeric policy
   - `PORT_0022` and `PORT_0025` remain execution-blocked before checker comparison

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

## 3. PORT Denominator / Packets

| packet | cases | current role |
| --- | --- | --- |
| seed PORT packet | `PORT_0004`, `PORT_0012`, `PORT_0022` | bounded seed PG route / consistency packet |
| Batch 2C packet | `PORT_0013`, `PORT_0024`, `PORT_0025` | bounded PG route-matrix and policy-consistency expansion |
| diagnostic / excluded | `PORT_0016` | diagnostic-only under current policy |
| backfill needed | `PORT_0003`, `PORT_0006` | require witness / checker backfill before execution |

Current clean-denominator note:

- the clean denominator policy still remains centered on `PORT_0004 / PORT_0022`
- `PORT_0012` remains a holdout failure-analysis / stress case
- Batch 2C adds bounded PostgreSQL-side route evidence, not automatic denominator expansion

## 4. Table A: PG Route Matrix Summary

| packet | case_id | SQLGlot PG status | SQLGlot failure category | Direct LLM PG status | Direct LLM token usage | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| seed | `PORT_0004` | success | none | success | `440` | both routes executed on PostgreSQL |
| seed | `PORT_0012` | failed | `InvalidDatetimeFormat` | success | `455` in seed matrix, `480` in targeted canary | clear stress-case contrast: SQLGlot fails while Direct LLM executes |
| seed | `PORT_0022` | success | none | success | `422` | both routes executed on PostgreSQL |
| Batch 2C | `PORT_0013` | failed | `UndefinedFunction` | success | `442` | SQLGlot same-dialect transpile produced PG-invalid boolean aggregation |
| Batch 2C | `PORT_0024` | success | none | success | `388` | both routes execute; checker closes under normalized TSV policy |
| Batch 2C | `PORT_0025` | success | none | success | `448` | both routes execute and close cleanly |

Combined route summary:

- SQLGlot PG success / failure: `4 / 2`
- Direct LLM PG success / failure: `6 / 0`
- combined Direct LLM token usage across seed matrix + Batch 2C: `2595`

## 5. Table B: PG-Side Policy / Reference Consistency

| packet | case_id | SQLGlot consistency status | Direct LLM consistency status | checker / normalization policy | interpretation |
| --- | --- | --- | --- | --- | --- |
| seed | `PORT_0004` | inconsistent | consistent | exact TSV only | SQLGlot differs from reference; Direct LLM matches exactly |
| seed | `PORT_0012` | blocked because SQLGlot PG execution failed | consistent against PG-normalized reference | report-local PostgreSQL-normalized reference | route failure and reference-layer PG compatibility are separate issues |
| seed | `PORT_0022` | inconsistent | exact mismatch but normalized consistent | exact TSV plus diagnostic normalization note | SQLGlot appears value-divergent; Direct LLM mismatch is numeric-formatting-only |
| Batch 2C | `PORT_0013` | not checked because PG execution failed | consistent | exact TSV report-local | SQLGlot route fails before checker; Direct LLM closes under exact policy |
| Batch 2C | `PORT_0024` | normalized-policy consistent | normalized-policy consistent | normalized TSV report-local | raw exact mismatch collapses under the allowed normalization rule |
| Batch 2C | `PORT_0025` | exact consistent | exact consistent | exact TSV report-local | both routes close cleanly under exact policy |

## 6. Failure Pattern Summary

- SQLGlot `PORT_0012` `InvalidDatetimeFormat`
  - quoted identifier vs string literal confusion
  - datetime / timestamp formatting
  - dialect normalization failure
  - portability translation failure
- SQLGlot `PORT_0013` `UndefinedFunction`
  - `SUM(boolean)`
  - type / function normalization gap for PostgreSQL
- SQLGlot value mismatches from the seed diagnostic
  - `PORT_0004`: reference `50.0` vs candidate `NULL`
  - `PORT_0022`: reference `0.25` vs candidate `0.0`
- Direct LLM numeric-formatting normalization cases
  - `PORT_0022` in the seed packet
  - `PORT_0024` in Batch 2C
- reference normalization
  - `PORT_0012` required a report-local PG-normalized reference variant because the original positive reference used PostgreSQL-incompatible constructs such as `AS DOUBLE` and `YEAR(...)`

## 7. Cross-Engine Feasibility Preflight

- denominator: `6` PORT cases
- `mysql_ready_count=3`
- `spark_ready_count=3`
- `both_engine_ready_count=3`
- recommended bounded execution subset:
  - `PORT_0022`
  - `PORT_0024`
  - `PORT_0025`
- blocked before execution:
  - `PORT_0004`: witness-file contract not normalized
  - `PORT_0012`: datetime_formatting / dialect_functions
  - `PORT_0013`: boolean_aggregation
- claim boundary: `preflight_only_not_cross_engine_closure`

Interpretation:

- this layer is a read-only readiness screen across the `6`-case packet
- readiness does not establish cross-engine closure

## 8. Bounded MySQL+Spark Execution Attempt

- denominator: `3` approved cases x `2` engines
- approved cases:
  - `PORT_0022`
  - `PORT_0024`
  - `PORT_0025`
- MySQL execution occurred: yes
- Spark execution occurred: yes
- PostgreSQL execution occurred: no
- model calls: no
- SQLGlot: no
- claim boundary: `bounded_3_case_mysql_spark_execution_not_full_port_closure`

Accepted paper wording:

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

## 9. Actual Bounded Cross-Engine Result

- `mysql_execution_success_count=1`
- `mysql_consistency_success_count=1`
- `spark_execution_success_count=1`
- `spark_consistency_success_count=1`
- `both_engine_execution_success_count=1`
- `both_engine_consistency_success_count=1`
- only `PORT_0024` closed on both engines
- `PORT_0024` required the existing normalized numeric policy
- `PORT_0022` and `PORT_0025` remain execution-blocked before checker comparison

Failure classification:

- `PORT_0022` / MySQL:
  - `rewrite_execution_failed` because MySQL rejected the positive rewrite near `CAST(... AS TIMESTAMP)`
- `PORT_0022` / Spark:
  - `source_execution_failed` because Spark rejected source-side `CAST(... AS DATETIME)`
- `PORT_0025` / MySQL:
  - `rewrite_execution_failed` because MySQL rejected the positive rewrite near `CAST(... AS TIMESTAMP)`
- `PORT_0025` / Spark:
  - `source_execution_failed` because Spark rejected source-side `CAST(... AS DATETIME)`
- these are execution blockers, not checker mismatches

## 10. Boundaries / Non-Claims

- PG-side route evidence is PostgreSQL-side portability evidence only, not cross-engine closure
- cross-engine feasibility is `preflight_only_not_cross_engine_closure`
- bounded execution evidence is `bounded_3_case_mysql_spark_execution_not_full_port_closure`
- not full cross-engine matrix
- not full PORT closure
- not final portability closure
- not MySQL and Spark portability proven
- not final cross-engine evidence for the PORT packet
- not final translation correctness
- not final PORT leaderboard
- not `6`-case PORT closure
- not all approved cases closed
- not automatic denominator expansion
- some reference normalization is report-local
- no registry writeback
- no formal review update

## 11. Remaining Work

- `PORT_0003` / `PORT_0006` backfill
- `PORT_0016` diagnostic policy
- normalized checker policy across all PORT
- full translation correctness protocol
- final denominator expansion decision

## 12. Recommended Next Action

- carry the `6`-case PG-side packet, the `6`-case preflight boundary, and the bounded `3`-case MySQL+Spark execution result as separate paper-facing evidence layers without merging them into a single closure claim

## 13. Verification / Non-Modification Note

- only this closeout doc was modified
- no SQL / database / model / SQLGlot / checker execution
- no reports were force-added
- no registry / `docs/EXECUTION_STATUS.md` / formal review changes
- taxonomy calibration notes were untouched
