# Calcite HEP MySQL/Spark Execution/Validity Canary 02 Triage

This is a read-only triage for the retained
`calcite_hep_mysql_spark_execution_canary_02` result. It is correctness /
validity canary evidence only. It is not timing evidence, not speedup
evidence, and not leaderboard evidence.

## Headline Status

- planned rows = `6`
- executed rows = `6`
- execution_failed rows = `0`
- match_exact rows = `4`
- mismatch rows = `2`

## Row Lists

`match_exact` rows:

- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

`mismatch` rows:

- `PERF_0006:mysql`
- `PERF_0006:spark`

## Counts

By engine:

- `mysql`: executed `3`, match_exact `2`, mismatch `1`
- `spark`: executed `3`, match_exact `2`, mismatch `1`

By case:

- `PERF_0006`: executed `2`, match_exact `0`, mismatch `2`
- `PERF_0007`: executed `2`, match_exact `2`, mismatch `0`
- `CONS_0005`: executed `2`, match_exact `2`, mismatch `0`

## Row-Level Status

All six rows have:

- `execution_status = executed`

Row-level `consistency_status`:

- `PERF_0006:mysql = mismatch`
- `PERF_0006:spark = mismatch`
- `PERF_0007:mysql = match_exact`
- `PERF_0007:spark = match_exact`
- `CONS_0005:mysql = match_exact`
- `CONS_0005:spark = match_exact`

## Artifact Presence

For all `6 / 6` rows:

- `source.tsv` exists
- `generated.tsv` exists
- `result_check.json` exists
- row metadata exists

The retained workspaces also preserve copied source SQL, generated SQL, schema,
and witness files for both MySQL and Spark rows.

## Mismatch Details: `PERF_0006:mysql` and `PERF_0006:spark`

The mismatches are not just output formatting.

Retained source output for one row includes:

- `avg_disc = 0.075000`

Retained generated output for the same row includes:

- `avg_disc = 0`

The generated rewrite also collapses:

- `15.000000 -> 15`
- `150.000000 -> 150`

Those formatting differences alone would not be sufficient to classify a
semantic mismatch. The decisive issue is:

- `0.075000 -> 0`

That is aggregate rewrite precision / decimal scale loss.

Best current root-cause classification:

- `aggregate_rewrite_precision_decimal_scale_loss`

The retained rewrite SQL uses `DECIMAL(15,0)` in AVG-like aggregate rewrites,
which truncates decimal scale and changes the query result semantics.

## Executable But Incorrect Boundary

The generated SQL for both `PERF_0006:mysql` and `PERF_0006:spark` was
executable, but not consistency-valid.

So the correct interpretation is:

- executable generated SQL exists
- correctness is not established for those rows
- the failure is semantic mismatch, not execution failure

## Logs

No retained row shows an execution failure traceback.

Observed stderr notes:

- MySQL rows show only the usual command-line password warning
- Spark rows show no error text in the retained stderr logs for the mismatched
  rows

That supports the classification:

- execution succeeded
- comparison failed because outputs differ

## Boundary

This result is:

- execution / validity canary evidence
- not timing evidence
- not speedup evidence
- not leaderboard evidence

It does not justify changing
[method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
yet.

Existing Calcite HEP PG-only canonical evidence remains unchanged.

## Recommendation

Do **not** compute timing for mismatched rows.

Recommended next step:

- `B. optionally run timing only for the 4 match_exact rows under an explicit match_exact_4 denominator`

That denominator should be explicit and bounded, for example:

- `calcite_hep_mysql_spark_canary_02_match_exact_4`

A separate canary result card is also reasonable now, but the safer technical
next step for measured performance evidence is timing only on the valid subset.
