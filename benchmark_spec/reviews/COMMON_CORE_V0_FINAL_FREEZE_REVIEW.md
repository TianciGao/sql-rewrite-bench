# COMMON_CORE_V0_FINAL_FREEZE_REVIEW

## Status

This document freezes the Common-core v0 candidate slate as the evaluation denominator.

It does not run experiments.
It does not compute leaderboard metrics.
It does not claim `SpeedupTransferRate`.
It does not merge `extended` cases into `common-core`.
It does not make final case admission claims.

All subsequent leaderboard experiments for Common-core v0 must use this denominator.

Support / verifier tables and PORT translation tables remain separately reported.

## Denominator Freeze

The frozen Common-core v0 denominator contains exactly `40` cases:

- `PERF = 16`
- `CONS = 9`
- `PORT = 9`
- `LONGTAIL = 6`

The denominator is recorded in:

- [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)
- [common_core_v0_final_denominator.md](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.md)

## Frozen Case List

### PERF 16

- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0034`
- `PERF_0035`
- `PERF_0052`
- `PERF_0054`
- `PERF_0056`
- `PERF_0062`
- `PERF_0077`
- `PERF_0082`

### CONS 9

- `CONS_0005`
- `CONS_0007`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0024`
- `CONS_0036`
- `CONS_0037`

### PORT 9

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

### LONGTAIL 6

- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

## Basis

This denominator freeze is based on:

- the live `inventory/case_registry.csv` review-packet rows
- the Common-core v0.3 candidate slate
- the human-gate draft conclusions
- the registry writeback proposal and current execution-status note

At freeze time, the live registry shows these `40` cases as:

- `benchmark_line = common_core_v0_candidate_review_packet`
- `dataset_line = common_core_v0_candidate`
- `admission_status = not_yet_admitted`

This is a denominator freeze for later evaluation comparability, not a formal admission conversion.

## Reporting Boundaries

The following boundaries are explicit:

- leaderboard work must use only this `40`-case denominator
- `common-core` and `extended` remain separate
- no leaderboard metric is computed in this document
- no `SpeedupTransferRate` claim is made in this document
- support / verifier reporting remains separate from leaderboard reporting
- PORT translation-table reporting remains separate from leaderboard reporting

## Carry-forward Caveats

### PERF

- `PERF_0077` and `PERF_0082` remain bounded `JOB/IMDB` real-schema bridge cases
- they are included in the denominator, but they do not justify over-weighting real-schema bridge behavior in PERF reporting

### CONS

- `CONS_0024` is the accepted denominator replacement for `CONS_0001`
- this remains a denominator choice, not final admission

### PORT

- `PORT_0012`, `PORT_0013`, `PORT_0022`, and `PORT_0025` carry normalization-caveat handling requirements
- final reporting must separate execution, consistency policy, normalization caveat, and any speedup-transfer discussion

### LONGTAIL

- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` are included as SQLStorm denominator cases
- they remain `not_yet_admitted`
- their prior registry-lag caveat remains a review-history fact, not a reason to change the frozen denominator now

## Operational Consequence

Subsequent evaluation work may proceed against this denominator on an explicit evaluation branch, but this document itself does not start that work.
