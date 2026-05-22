# R-Bot MySQL/Spark Canary Result Card v1

## Identity

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- `artifact_scope = generation_only_canary`
- `engine_scope = mysql_and_spark_canary_only`
- `leaderboard_comparable = no`

## Concise Summary

This artifact records **generation-only canary evidence** for recovered R-Bot
MySQL/Spark attempts on `6` bounded rows:

- engines: `MySQL`, `Spark`
- cases: `PERF_0006`, `PERF_0007`, `CONS_0005`

Outcome:

- `planned rows = 6`
- `preflight_blocked = 0`
- `generated = 0`
- `failed = 6`

No SQL execution was performed. No timing or speedup was computed.

## Denominator Table

| Layer | Denominator ID | Planned Rows | Outcome |
|---|---|---:|---|
| Generation canary | `r_bot_mysql_spark_generation_canary_01` | 6 | `generated=0`, `failed=6`, `preflight_blocked=0`, `unsupported=0` |

## Interpretation

Current root-cause classification:

- `prompt/output-contract or recovered-route limitation`

Retained raw responses contain:

- rule-selection lists
- rewrite-strategy clustering text
- strategy summaries

They do **not** contain executable final rewritten SQL for the target engines.

Therefore this artifact is:

- not a correctness-rate result
- not a speedup result
- not leaderboard evidence

MySQL/Spark remain `NA_not_computed` for R-Bot in
[method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md).

## Paper-Safe Wording

Under the recovered R-Bot route, MySQL/Spark canary rows reached generation
attempts, but produced no extractable final SQL. The retained responses contain
rule-selection or rewrite-strategy text rather than executable target-engine
SQL. Therefore, MySQL/Spark execution, timing, and speedup metrics remain not
computed for R-Bot.

## Do Not Claim

- do not say this is MySQL/Spark correctness evidence
- do not say this is MySQL/Spark speedup evidence
- do not say R-Bot MySQL/Spark correctness is `0`
- do not treat this as leaderboard evidence
- do not treat this as a basis for a silent extractor patch

## Relation To Current R-Bot Paper Status

- PostgreSQL paper-facing R-Bot evidence is represented by
  [r_bot_pg_expansion_result_card_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg_expansion_result_card_v2.md)
  and
  [r_bot_pg15_speedup_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg15_speedup_summary_v2.md).
- This MySQL/Spark card is a **boundary artifact** that makes the non-PG
  conclusion visible for paper writing without turning it into a metric claim.
- Another silent harness/extractor patch is **not** recommended from the
  retained evidence.

## Source Artifacts

- [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/run_results.json)
- [run_event_long.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/run_event_long.csv)
- [generation_canary_triage.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/generation_canary_triage.md)
- [r_bot_mysql_spark_feasibility_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_mysql_spark_feasibility_audit_v1.md)
