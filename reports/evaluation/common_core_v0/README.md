# Common-core v0 Evaluation Schemas

This directory contains schema templates only. It does not contain real evaluation outputs.

## Purpose

These files define the reporting shape for Common-core v0 evaluation once a later explicit evaluation run is approved.

The frozen denominator is the `40`-case Common-core v0 set recorded in:

- [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)
- [COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md](/home/tianci_gao/code/sql-rewrite-bench/benchmark_spec/reviews/COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md)

## Canonical Raw Table

`run_event_long` is the canonical raw result table.

Every executed, verified, skipped, failed, timed-out, or unsupported event should be representable there before any leaderboard or summary table is derived. Derived tables should not invent rows that cannot be traced back to `run_event_long`.

## Derived Summaries

Leaderboard-style tables are derived summaries, not raw evidence. In particular:

- `same_engine_leaderboard` is a derived same-engine summary
- `port_translation_summary` is a separate PORT translation report
- `verifier_support_summary` is a separate verifier-coverage report
- `plan_observability_summary` is a separate plan-observability report

These should not be collapsed into one mixed table because they answer different questions.

## Denominator Discipline

No failed case should be silently removed from the denominator.

Coverage-aware denominator counts must remain visible in derived summaries, including when a case fails, times out, is unsupported, or lacks a valid rewrite result. Failure and missingness should move into explicit status and failure-bucket fields rather than disappearing from reporting.

## Speedup Reporting

`GM_Speedup` is computed only on speedup-eligible valid rewrites.

That restriction does not permit hiding denominator coverage. Reports must still show coverage-aware denominators, valid-case counts, and speedup-eligible counts alongside any geometric-mean speedup figure.

## File Roles

- `evaluation_manifest.template.json`: top-level manifest template for one evaluation run
- `run_event_long.schema.csv`: canonical raw event table schema
- `method_case_summary.schema.csv`: per-case aggregation schema derived from raw events
- `same_engine_leaderboard.schema.csv`: same-engine leaderboard summary schema
- `controls_summary.schema.csv`: controls and sanity-check summary schema
- `port_translation_summary.schema.csv`: separate PORT translation summary schema
- `verifier_support_summary.schema.csv`: verifier-support coverage schema
- `plan_observability_summary.schema.csv`: plan-observability coverage schema
- `failure_bucket_summary.schema.csv`: failure classification summary schema

## Boundary

These files do not populate real results, do not execute methods, and do not authorize benchmark runs by themselves.
