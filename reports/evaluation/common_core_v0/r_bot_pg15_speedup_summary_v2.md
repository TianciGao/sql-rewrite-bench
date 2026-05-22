# R-Bot PG15 Speedup Summary v2

## Scope

This summary materializes speedup evidence only for the retained R-Bot
PostgreSQL expansion subset with:

- `generation_denominator_id = common_core_v0_40_pg40`
- `execution_denominator_id = generated_pg15_from_pg40_expansion_only`
- `timing_denominator_id = generated_pg15_from_pg40_expansion_match_exact_only`

Boundary:

- this is PG15-only speedup evidence
- this is not full PG40 timing
- this is not full `120`-row timing
- this is not tri-engine evidence
- this is not leaderboard evidence

## Denominator Table

| Layer | Denominator ID | Planned Rows | Observed Rows |
|---|---|---:|---:|
| Generation | `common_core_v0_40_pg40` | 40 | `generated=15`, `failed=25`, `blocked=0`, `unsupported=0` |
| Execution | `generated_pg15_from_pg40_expansion_only` | 15 | `executed=15`, `match_exact=15`, `mismatch=0`, `execution_failed=0` |
| Timing | `generated_pg15_from_pg40_expansion_match_exact_only` | 15 | `timing_success=15`, `timing_failed=0` |

## Metric Table

| Metric | Value |
|---|---:|
| `GM_Speedup` over PG15 only | `0.921825` |
| `RegressionRate@20%` over PG15 only | `3 / 15 = 20.00%` |
| `min_speedup_ratio` | `0.629355` |
| `median_speedup_ratio` | `0.982075` |
| `max_speedup_ratio` | `1.295615` |

## Per-Row Speedup Ratios

- `PERF_0006:pg`: `0.992102`
- `PERF_0007:pg`: `0.804643`
- `PERF_0008:pg`: `0.982075`
- `PERF_0013:pg`: `0.880716`
- `PERF_0017:pg`: `0.998361`
- `PERF_0024:pg`: `1.000012`
- `PERF_0052:pg`: `0.773005`
- `PERF_0054:pg`: `0.941534`
- `PERF_0062:pg`: `0.785168`
- `CONS_0005:pg`: `0.927252`
- `CONS_0007:pg`: `0.629355`
- `CONS_0009:pg`: `1.295615`
- `CONS_0010:pg`: `0.988108`
- `CONS_0012:pg`: `0.992199`
- `CONS_0036:pg`: `1.010042`

## Material Regression Rows

Using the retained PG15 expansion triage convention `speedup_ratio < 0.8`:

- `CONS_0007`
- `PERF_0052`
- `PERF_0062`

## Caveats

- PG generation coverage improved from `7 / 40` retained PG generated rows in
  the earlier PG7 evidence path to `15 / 40` generated rows in the PG expansion
  run.
- The `25` failed generation rows remain explicit denominator rows and were not
  silently dropped.
- Timing is available only for the `15` rows that were both generated and
  `match_exact` in execution.
- These figures must not be presented as full PG40 timing, full `120`-row
  same-engine timing, tri-engine evidence, or leaderboard evidence.

## Relation To Prior PG7 Evidence

Relative to [r_bot_pg7_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg7_speedup_summary_v1.md):

- prior PG7 timing subset size: `7`
- prior PG7-only `GM_Speedup`: `0.947444`
- current PG15 timing subset size: `15`
- current PG15-only `GM_Speedup`: `0.921825`

This is useful as same-method subset-to-subset context only. It is not a
leaderboard comparison because the timing denominators differ.
