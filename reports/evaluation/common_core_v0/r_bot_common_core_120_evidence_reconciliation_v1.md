# R-Bot Common-core 120 Evidence Reconciliation v1

This document reconciles retained R-Bot artifacts for the Common-core v0
same-engine campaign. It is a reconciliation of existing evidence, not a new
run.

## Scope

- no SQL generation was performed for this packet
- no DB execution was performed for this packet
- no timing or speedup work was performed for this packet
- this packet does not update `method_comparison_summary_v2`

## Fixed interpretation

R-Bot must not be described as `not attempted on 120`.

Retained artifacts show:

1. a formal `120`-row same-engine generation attempt exists
2. a later PG40 generation expansion exists
3. final execution and timing evidence is PG15 subset-scoped
4. a bounded MySQL/Spark canary exists and failed to generate final SQL

This is therefore mixed-scope retained evidence, not full tri-engine `120`
execution/timing evidence.

## Layered Evidence Table

| Layer | Artifact | Denominator | Engine Scope | Retained Outcome | Caveat |
|---|---|---|---|---|---|
| formal `120` generation attempt | `runs/r_bot_common_core_v0_40_same_engine_generation_01` | `common_core_v0_40_same_engine_120` | `pg,mysql,spark` | `planned=120`, `generated=7`, `generation_failed=2`, `blocked=31`, `unsupported=80` | generation evidence only |
| PG40 generation expansion | `runs/r_bot_pg40_generation_expansion_02` | `common_core_v0_40_pg40` | `pg_only` | `planned=40`, `generated=15`, `generation_failed=25`, `blocked=0`, `unsupported=0` | PostgreSQL-only expansion; still generation-only |
| PG15 execution expansion | `runs/r_bot_pg15_execution_expansion_02` | `generated_pg15_from_pg40_expansion_only` | `pg_only` | `executed=15`, `match_exact=15`, `mismatch=0`, `execution_failed=0` | only the generated PG15 subset enters execution |
| PG15 timing expansion | `runs/r_bot_pg15_timing_expansion_02` | `generated_pg15_from_pg40_expansion_match_exact_only` | `pg_only` | `timing_success=15`, `GM_Speedup=0.921825`, `RegressionRate@20%=0.2000` | not full PG40 timing and not full `120` timing |
| MySQL/Spark canary | `runs/r_bot_mysql_spark_generation_canary_01` | `r_bot_mysql_spark_generation_canary_01` | `mysql,spark` | `planned=6`, `generated=0`, `generation_failed=6`, `preflight_blocked=0` | non-PG route reaches generation but emits no extractable final SQL |

## Recovered Values

### A. Formal 120 generation attempt

- `denominator_id = common_core_v0_40_same_engine_120`
- `planned_rows = 120`
- `generated_rows = 7`
- `generation_failed_rows = 2`
- `preflight_blocked_rows = UNKNOWN_NOT_RECOVERED`
  - retained artifacts expose `blocked = 31` but do not label those rows as
    `preflight_blocked`
- `unsupported_rows = 80`
- `engines_covered = pg,mysql,spark`
- row accounting notes:
  - `31` PG rows remain explicit as blocked by the recovered committed PG
    runner whitelist
  - `80` MySQL/Spark rows remain explicit as unsupported in the current
    recovered committed PG-only runner path
  - this layer is generation-only and does not create execution, timing, or
    leaderboard evidence

### B. PG40 generation expansion

- `denominator_id = common_core_v0_40_pg40`
- `planned_rows = 40`
- `generated_rows = 15`
- `generation_failed_rows = 25`
- `unsupported_rows = 0`
- `preflight_blocked_rows = UNKNOWN_NOT_RECOVERED`
  - retained artifacts expose `blocked = 0` but do not label the count as
    `preflight_blocked`

### C. PG15 execution expansion

- `execution_denominator_id = generated_pg15_from_pg40_expansion_only`
- `executed_rows = 15`
- `exact_match_rows = 15`
- `mismatch_rows = 0`
- `execution_failed_rows = 0`
- `exact_among_executed = 15/15`

### D. PG15 timing expansion

- `timing_denominator_id = generated_pg15_from_pg40_expansion_match_exact_only`
- `timing_success_rows = 15`
- `gm_speedup = 0.921825`
- `regression_rate_20pct = 0.2000`
- timing caveat:
  - timing is PG15 subset-only
  - timing does not imply evidence for all PG40 rows
  - timing does not imply evidence for the full
    `common_core_v0_40_same_engine_120` denominator

### E. MySQL/Spark canary

- `planned_rows = 6`
- `generated_rows = 0`
- `generation_failed_rows = 6`
- `unsupported_rows = 0`
- `preflight_blocked_rows = 0`
- `engines_covered = mysql,spark`
- canary caveat:
  - preflight reached `ok` for both engines
  - the canary still produced no extractable final `output_sql`
  - this remains generation-only boundary evidence, not correctness or timing
    evidence

## Why previous preflight-only wording needs caveat

The earlier Stage-1 R-Bot preflight scaffold remains useful for dependency
recovery planning, but it is not the whole retained R-Bot story.

This reconciliation supersedes a too-narrow preflight-only interpretation by
showing that retained artifacts already include:

- a formal `120`-row generation attempt
- a PG40 generation expansion
- a PG15 exact-match execution subset
- a PG15 timing subset
- a bounded MySQL/Spark generation canary

## Final classification

- `method_id = r_bot`
- `route_status = attempted_120_generation_with_pg_subset_execution_timing`
- `leaderboard_comparable = no`
- `paper_table_placement = bounded_or_mixed_scope_method_evidence / appendix`

## Final paper-safe statement

`R-Bot has retained Common-core v0 same-engine evidence showing a formal 120-row generation attempt, a PostgreSQL-only PG40 generation expansion to 15 generated rows, exact-match execution on the generated PG15 subset, and PG15-only timing on that exact-match subset. It does not have full tri-engine 120-row execution or timing evidence. The bounded MySQL/Spark canary reached generation but failed to emit extractable final SQL for all 6 attempted rows, and those failures remain explicit. R-Bot is therefore mixed-scope denominator-aware evidence, not leaderboard-comparable full-120 same-engine evidence.`

## Explicit non-claims

- this packet does not claim full `120`-row execution evidence
- this packet does not claim full `120`-row timing evidence
- this packet does not claim tri-engine correctness evidence
- this packet does not claim tri-engine performance evidence
- this packet does not promote R-Bot into leaderboard-comparable status
- this packet does not overwrite `method_comparison_summary_v2`

## Source artifacts used

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/generation_summary.csv`
- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/generation_triage.md`
- `reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg40_generation_expansion_02/generation_expansion_triage.md`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_execution_expansion_02/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_execution_expansion_02/execution_triage.csv`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/timing_triage.csv`
- `reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/generation_canary_triage.md`
- `reports/evaluation/common_core_v0/r_bot_pg_expansion_result_card_v2.md`
- `reports/evaluation/common_core_v0/r_bot_pg_expansion_result_card_v2.csv`
- `reports/evaluation/common_core_v0/r_bot_pg15_speedup_summary_v2.md`
- `reports/evaluation/common_core_v0/r_bot_pg15_speedup_summary_v2.csv`
- `reports/evaluation/common_core_v0/r_bot_mysql_spark_feasibility_audit_v1.md`
- `reports/evaluation/common_core_v0/r_bot_upstream_runner_alignment_audit_v1.md`
