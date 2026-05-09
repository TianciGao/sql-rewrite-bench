# Calcite HEP 120 Fail-Closed Synthesis v1
Calcite HEP can be synthesized against the intended `common_core_v0_40_same_engine_120` denominator as a **fail-closed correctness ledger** using only retained artifacts. In that ledger, rows that fail generation, parser acceptance, HEP rewrite, setup, execution, or exact-match validation remain in the denominator and contribute `0` to exact-match coverage.
## Headline Answer
- Intended denominator: `120 = 40 cases × 3 engines`
- Retained PG evidence: `40/40` PG rows have retained route artifacts, with `21/40` fail-closed exact matches
- Retained non-PG evidence: `80/80` MySQL/Spark rows have retained route artifacts, with `54/80` fail-closed exact matches
- Combined fail-closed exact-match ledger: `75/120 = 62.50%`

## Denominator-Aware Status
- PostgreSQL route evidence comes from the retained PG40 Calcite HEP generation and execution packets, plus the bounded recovery canary for three previously unrecovered PG `LONGTAIL` rows.
- MySQL/Spark evidence comes from the retained non-PG rewrite expansion (`80` rows), execution expansion (`60` rewrite-success rows), and the bounded recovery canary that recovered four MySQL rows and one Spark row.
- This is **not** full timing evidence, **not** speedup evidence, and **not** leaderboard-comparable evidence.

## PostgreSQL Evidence
- denominator used by retained PG route: `common_core_v0_40_pg40`
- generation_success: `32`
- generation_failed_parse: `7`
- generation_failed_unsupported_sql: `1`
- executed: `23`
- execution_failed: `9`
- match_exact: `21`
- mismatch: `2`
PG match_exact rows:
- CONS_0005:pg, CONS_0007:pg, CONS_0009:pg, CONS_0010:pg, CONS_0011:pg, CONS_0012:pg, CONS_0024:pg, PERF_0006:pg, PERF_0007:pg, PERF_0008:pg, PERF_0013:pg, PERF_0017:pg, PERF_0019:pg, PERF_0024:pg, PERF_0033:pg, PERF_0034:pg, PERF_0052:pg, PERF_0054:pg, PERF_0056:pg, PERF_0077:pg, PERF_0082:pg
PG mismatch rows:
- PERF_0035:pg, PERF_0062:pg
PG execution_failed rows:
- CONS_0036:pg, CONS_0037:pg, LONGTAIL_0011:pg, LONGTAIL_0012:pg, LONGTAIL_0013:pg, LONGTAIL_0022:pg, LONGTAIL_0023:pg, LONGTAIL_0024:pg, PORT_0024:pg
PG generation_failed rows:
- PORT_0003:pg, PORT_0004:pg, PORT_0005:pg, PORT_0008:pg, PORT_0012:pg, PORT_0013:pg, PORT_0022:pg, PORT_0025:pg

## MySQL/Spark Evidence
- denominator used by retained non-PG route: `calcite_hep_mysql_spark_common_core_v0_80`
- rewrite_success: `65`
- parser_failed: `14`
- hep_rewrite_failed: `2`
- executed: `64`
- setup_failed: `0`
- match_exact: `54`
- mismatch: `10`
Non-PG rewrite_success rows are execution-eligible; parser_failed and hep_rewrite_failed remain explicit denominator rows and count as non-exact in the fail-closed ledger.
Non-PG parser_failed rows:
- PORT_0003:mysql, PORT_0003:spark, PORT_0004:mysql, PORT_0004:spark, PORT_0005:mysql, PORT_0005:spark, PORT_0008:mysql, PORT_0008:spark, PORT_0012:mysql, PORT_0012:spark, PORT_0022:mysql, PORT_0022:spark, PORT_0025:mysql, PORT_0025:spark
Non-PG hep_rewrite_failed rows:
- PORT_0013:mysql, PORT_0013:spark
Non-PG setup_failed rows:
- none retained after recovery canary `08_01`
Non-PG mismatch rows:
- PERF_0006:mysql, PERF_0006:spark, PERF_0035:mysql, PERF_0035:spark, PERF_0062:mysql, PERF_0062:spark, LONGTAIL_0012:mysql, LONGTAIL_0012:spark, LONGTAIL_0013:mysql, LONGTAIL_0013:spark
Recovered exact rows from recovery canary `08_01`:
- PERF_0008:mysql, PERF_0013:mysql, PERF_0017:mysql, PERF_0019:mysql, PERF_0077:spark

## Recovery Canary Update

`After a bounded recovery canary targeting low-risk Calcite HEP harness and wrapper defects, the fail-closed exact-match ledger improved from 70/120 to 75/120. Five rows recovered exact-match validity evidence. The recovered rows reflect implementation-level route repair rather than relaxation of exact-match semantics or denominator scope. The remaining three audited rows now reach target-dialect PostgreSQL SQL generation but fail during execution. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

## Fail-Closed Scoring
| Slice | Exact rows | Denominator | Fail-closed exact rate |
|---|---:|---:|---:|
| PG | 21 | 40 | 52.50% |
| MySQL/Spark | 54 | 80 | 67.50% |
| Combined | 75 | 120 | 62.50% |

## Denominator IDs For Paper Table Inclusion
If Calcite HEP is surfaced in a paper method table before any canonical table update, the retained artifacts support a **proposed denominator-aware evidence row** with:
- `generation_or_route_denominator_id = common_core_v0_40_same_engine_120`
- `execution_or_ready_denominator_id = fail_closed_exact_match_ledger_on_common_core_v0_40_same_engine_120`
- `timing_denominator_id = NA_not_computed`
- `engine_scope = tri_engine_same_engine_fail_closed_mixed_evidence`
- `leaderboard_comparable = no`

## What The Paper May Claim
- Calcite HEP can be included in the paper as a **denominator-aware evidence row only after a paper-readiness check**.
- The current MySQL/Spark expansion provides bounded non-PG execution-validity evidence.
- The bounded recovery canary provides additional implementation-level route repair evidence without changing denominator policy.
- Retained artifacts support a `120`-row fail-closed correctness ledger with `75/120` exact matches when non-exact outcomes remain in-denominator.

## What The Paper Must Not Claim
- Do not present this synthesis as full timing evidence.
- Do not present this synthesis as speedup evidence.
- Do not present this synthesis as leaderboard-comparable evidence.
- Do not imply that the non-PG expansion or recovery canary closes the full tri-engine route for timing or performance comparison.
- Do not describe the retained ledger as `120`-row completion.

## What Remains Missing
- A denominator-aware paper-readiness check specific to this proposed synthesized Calcite HEP row after the recovery canary update.
- Any full 120-row timing packet.
- Any normalized leaderboard policy that would make this mixed PG + bounded non-PG row rank-comparable.
