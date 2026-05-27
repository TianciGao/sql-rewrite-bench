# COMMON_CORE_V0_EVALUATION_PROTOCOL

## Role

This document defines the enforcement contract for Common-core v0 evaluation reporting.

It does not run experiments.
It does not authorize benchmark execution.
It does not change case admission status.

The frozen evaluation denominator is the `40`-case set recorded in:

- `benchmark_spec/reviews/COMMON_CORE_V0_FINAL_FREEZE_REVIEW.md`
- `reports/curation/common_core_v0_final_denominator.csv`

## Core Rule

All Common-core v0 leaderboard evaluation must be denominator-first.

- `denominator_id` must equal `common_core_v0_40`
- every evaluated case must belong to the frozen `40`-case denominator
- unknown case IDs are invalid
- failed, timed-out, unsupported, or invalid cases must remain visible in denominator-aware reporting

## Canonical Raw Table

`run_event_long` is the canonical raw result table.

All downstream summaries must be derivable from raw rows that preserve:

- case identity
- route identity
- engine identity
- method identity
- git revision identity
- denominator identity
- success / failure / exclusion status

## Governance Fields

At enforcement time, each raw row must resolve the following governance fields:

- `run_id`
- `method_id`
- `route_id`
- `engine`
- `git_commit`
- `denominator_id`

Current schema compatibility rules:

- `engine` may be satisfied by `engine` or temporary alias `engine_target`
- `route_id` may be satisfied by `route_id` or temporary alias `task_track`
- `git_commit` may be row-local or provided once in the run manifest
- `denominator_id` may be row-local or provided once in the run manifest

These aliases are compatibility shims for the current schema scaffolding, not long-term exemptions.

## Leaderboard Boundary

Leaderboard tables are derived summaries.

- `same_engine_leaderboard` is for same-engine leaderboard slices only
- `port_translation_summary` is separate and must not be mixed into same-engine leaderboard reporting
- `verifier_support_summary` is separate and must not be represented as a leaderboard method
- `plan_observability_summary` is separate and must not be treated as a speedup leaderboard

## Speedup Boundary

`GM_Speedup` is computed only on speedup-eligible valid rewrites.

Therefore:

- `speedup_ratio` may appear only when `is_speedup_eligible = yes/true`
- rows that are invalid, mismatched, failed, timed out, unsupported, or otherwise excluded must carry `speedup_exclusion_reason`
- coverage-aware denominator counts must still be reported even when speedup is excluded

## Prohibited Claims

No evaluation artifact in this package may propose or claim:

- `admitted_common_core`
- merged `extended` and `common-core` scoring
- `SpeedupTransferRate` from PORT normalization-caveat rows by default

## Validation Scope

The enforcement scaffolding validates:

1. manifest-level denominator and method-role claims
2. raw-table schema and case membership
3. same-engine leaderboard separation from PORT translation routes
4. denominator-aware attempted-case accounting
5. speedup eligibility and exclusion bookkeeping

It is intentionally designed to work before real results exist.
