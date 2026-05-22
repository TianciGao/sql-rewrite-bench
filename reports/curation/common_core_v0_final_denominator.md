# Common-core v0 Final Denominator

## Executive Summary

This file records the frozen Common-core v0 evaluation denominator.

The denominator contains exactly `40` cases:

- `PERF = 16`
- `CONS = 9`
- `PORT = 9`
- `LONGTAIL = 6`

This freeze does not run experiments, does not compute leaderboard metrics, does not claim `SpeedupTransferRate`, and does not merge `extended` cases into `common-core`.

## Machine-readable Table

The machine-readable denominator is stored in:

- [common_core_v0_final_denominator.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/curation/common_core_v0_final_denominator.csv)

All subsequent Common-core v0 leaderboard experiments must use this denominator.

## Source-balance Summary

- `TPC-H`: `7`
- `TPC-DS`: `7`
- `JOB/IMDB`: `2`
- `Calcite`: `7`
- `VeriEQL`: `2`
- `PARROT`: `9`
- `SQLStorm`: `3`
- `Stack Queries`: `3`

## Carry-forward Caveats

- `PERF_0077` and `PERF_0082` remain bounded `JOB/IMDB` real-schema bridge denominator cases.
- `CONS_0024` remains the denominator replacement for `CONS_0001`.
- `PORT_0012`, `PORT_0013`, `PORT_0022`, and `PORT_0025` remain normalization-caveat cases and must not be used to overclaim `SpeedupTransferRate`.
- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` remain SQLStorm denominator cases with review-history caveats, but they stay in the frozen denominator.

## Reporting Boundary

Support / verifier tables and PORT translation tables remain separately reported from leaderboard summaries.
