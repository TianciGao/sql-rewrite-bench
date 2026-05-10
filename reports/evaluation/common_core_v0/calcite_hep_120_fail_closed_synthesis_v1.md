# Calcite HEP 120 Fail-Closed Synthesis v1

Calcite HEP can be synthesized against the intended
`common_core_v0_40_same_engine_120` denominator as a fail-closed correctness
ledger using only retained artifacts. In that ledger, rows that fail
generation, parser acceptance, HEP rewrite, setup, execution, or exact-match
validation remain in the denominator and contribute `0` to exact-match
coverage.

## Headline Answer

- Intended denominator: `120 = 40 cases × 3 engines`
- Retained PG evidence: `40/40` PG rows have retained route artifacts, with
  `31/40` fail-closed exact matches
- Retained non-PG evidence: `80/80` MySQL/Spark rows have retained route
  artifacts, with `62/80` fail-closed exact matches
- Combined fail-closed exact-match ledger: `93/120 = 77.50%`
- Post-93 frontier status: retained audit found `0` low-risk and `0` medium-risk
  recovery candidates, so `93/120` is the current paper-safe ceiling for this
  route

## Denominator-Aware Status

- PostgreSQL route evidence comes from the retained PG40 Calcite HEP generation
  and execution packets, plus bounded PG recovery canaries.
- MySQL/Spark evidence comes from the retained non-PG rewrite expansion
  (`80` rows), execution expansion, and bounded non-PG recovery canaries.
- This is not timing evidence, not speedup evidence, and not
  leaderboard-comparable evidence.

## PostgreSQL Evidence

- denominator used by retained PG route: `common_core_v0_40_pg40`
- generation_success: `32`
- generation_failed_parse: `7`
- generation_failed_unsupported_sql: `1`
- executed: `31`
- execution_failed: `1`
- match_exact: `31`
- mismatch: `0`

PG match_exact rows:
- CONS_0005:pg, CONS_0007:pg, CONS_0009:pg, CONS_0010:pg, CONS_0011:pg,
  CONS_0012:pg, CONS_0024:pg, CONS_0036:pg, CONS_0037:pg, PERF_0006:pg,
  PERF_0007:pg, PERF_0008:pg, PERF_0013:pg, PERF_0017:pg, PERF_0019:pg,
  PERF_0024:pg, PERF_0033:pg, PERF_0034:pg, PERF_0035:pg, PERF_0052:pg,
  PERF_0054:pg, PERF_0056:pg, PERF_0062:pg, PERF_0077:pg, PERF_0082:pg,
  LONGTAIL_0011:pg, LONGTAIL_0012:pg, LONGTAIL_0013:pg, LONGTAIL_0022:pg,
  LONGTAIL_0023:pg, LONGTAIL_0024:pg

PG execution_failed rows:
- PORT_0024:pg

PG generation_failed rows:
- PORT_0003:pg, PORT_0004:pg, PORT_0005:pg, PORT_0008:pg, PORT_0012:pg,
  PORT_0013:pg, PORT_0022:pg, PORT_0025:pg

## MySQL/Spark Evidence

- denominator used by retained non-PG route:
  `calcite_hep_mysql_spark_common_core_v0_80`
- rewrite_success: `64`
- parser_failed: `14`
- hep_rewrite_failed: `2`
- executed: `64`
- generated_execution_failed: `0`
- setup_failed: `0`
- match_exact: `62`
- mismatch: `2`

Non-PG parser_failed rows:
- PORT_0003:mysql, PORT_0003:spark, PORT_0004:mysql, PORT_0004:spark,
  PORT_0005:mysql, PORT_0005:spark, PORT_0008:mysql, PORT_0008:spark,
  PORT_0012:mysql, PORT_0012:spark, PORT_0022:mysql, PORT_0022:spark,
  PORT_0025:mysql, PORT_0025:spark

Non-PG hep_rewrite_failed rows:
- PORT_0013:mysql, PORT_0013:spark

Non-PG mismatch rows:
- PERF_0006:mysql, PERF_0006:spark

## Recovery Canary Updates

Round-1 recovery lifted the fail-closed ledger from `70/120` to `75/120` with
five recovered exact rows:
- PERF_0008:mysql, PERF_0013:mysql, PERF_0017:mysql, PERF_0019:mysql,
  PERF_0077:spark

Round-2 recovery lifted the ledger from `75/120` to `80/120` with five more
recovered exact rows:
- LONGTAIL_0022:pg, LONGTAIL_0023:pg, LONGTAIL_0024:pg, LONGTAIL_0012:mysql,
  LONGTAIL_0012:spark

Round-3 recovery and the bounded Round-3c MySQL numeric-scale canary lifted the
ledger from `80/120` to `86/120` with six more recovered exact rows:
- CONS_0036:pg, CONS_0037:pg, LONGTAIL_0011:pg, LONGTAIL_0012:pg,
  PERF_0062:mysql, LONGTAIL_0013:mysql

Round-4b recovery lifted the ledger from `86/120` to `90/120` with four more
recovered exact rows:
- PERF_0062:pg, PERF_0062:spark, LONGTAIL_0013:pg, LONGTAIL_0013:spark

The bounded `PERF_0035` recovery canary lifted the ledger from `90/120` to
`93/120` with three more recovered exact rows:
- PERF_0035:pg, PERF_0035:mysql, PERF_0035:spark

The post-93 frontier audit found no additional low-risk or medium-risk
recovery candidates under the unchanged route, denominator, and checker:

- remaining gaps are dominated by semantic mismatches
- parser or deep-feature support gaps
- methodology-boundary `PORT` rows

This establishes `93/120` as the current paper-safe ceiling for this Calcite
HEP route.

Required paper-safe statement:

`After a bounded PERF_0035 recovery canary targeting a proven internal helper-column projection artifact and numeric-scale rendering defects, the fail-closed exact-match ledger improved from 90/120 to 93/120. Three additional rows recovered exact-match validity evidence. The recovered rows reflect package-local final projection repair under unchanged exact-match semantics, unchanged checker policy, and unchanged denominator scope. This remains bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

Post-93 paper-safe ceiling statement:

`Calcite HEP reaches a fail-closed exact-match ledger of 93/120 on the common_core_v0_40_same_engine_120 denominator. A post-93 frontier audit found no additional low-risk or medium-risk recovery candidates under the unchanged route, denominator, and checker. The remaining gaps are dominated by semantic mismatches, parser/deep-feature support gaps, or methodology-boundary PORT rows. Therefore 93/120 is the current paper-safe ceiling for this Calcite HEP route. This is bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

## Fail-Closed Scoring

| Slice | Exact rows | Denominator | Fail-closed exact rate |
|---|---:|---:|---:|
| PG | 31 | 40 | 77.50% |
| MySQL/Spark | 62 | 80 | 77.50% |
| Combined | 93 | 120 | 77.50% |

## Denominator IDs For Paper Table Inclusion

If Calcite HEP is surfaced in a paper method table before any canonical table
update, the retained artifacts support a proposed denominator-aware evidence row
with:

- `generation_or_route_denominator_id = common_core_v0_40_same_engine_120`
- `execution_or_ready_denominator_id = fail_closed_exact_match_ledger_on_common_core_v0_40_same_engine_120`
- `timing_denominator_id = NA_not_computed`
- `engine_scope = tri_engine_same_engine_fail_closed_mixed_evidence`
- `leaderboard_comparable = no`

## What The Paper May Claim

- Calcite HEP can be included in the paper as a denominator-aware evidence row
  only after a paper-readiness check.
- The current MySQL/Spark route contributes bounded non-PG execution-validity
  evidence.
- The bounded recovery canaries provide implementation-level route repair
  evidence without changing denominator policy.
- Retained artifacts support a `120`-row fail-closed correctness ledger with
  `93/120` exact matches when non-exact outcomes remain in-denominator.
- The retained post-93 frontier audit supports treating `93/120` as the
  current paper-safe ceiling for this route.

## What The Paper Must Not Claim

- Do not present this synthesis as timing evidence.
- Do not present this synthesis as speedup evidence.
- Do not present this synthesis as leaderboard-comparable evidence.
- Do not imply that the bounded non-PG expansion or recovery canaries close the
  full tri-engine route for performance comparison.
- Do not describe the retained ledger as `120`-row completion.
- Do not imply that `95/120` is currently reachable without route drift,
  checker relaxation, denominator change, or deeper unsupported feature work.

## What Remains Missing

- A denominator-aware paper-readiness check specific to this proposed
  synthesized Calcite HEP row after the full retained recovery chain.
- Any full `120`-row timing packet.
- Any normalized leaderboard policy that would make this mixed PG + bounded
  non-PG row rank-comparable.
- Any new retained implementation-level evidence that would justify moving past
  the current `93/120` ceiling.
