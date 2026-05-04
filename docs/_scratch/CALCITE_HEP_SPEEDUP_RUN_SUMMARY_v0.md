# CALCITE_HEP_SPEEDUP_RUN_SUMMARY_v0

## Status

This note records the bounded 4-case Calcite HEP speedup run for:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit boundary:

- PostgreSQL-only
- bounded 4-case subset only
- speedup-scored
- not final Calcite HEP baseline
- no registry/admission/formal review update

## Commands Run

1. `python -m py_compile scripts/cli.py`
2. `python -m scripts.cli formal-calcite-hep-speedup-run`
3. `export PGPASSWORD='123456'`
4. `source scripts/env_postgres.sh`
5. `python -m scripts.cli formal-calcite-hep-speedup-run --case-id PERF_0006 --execute`
6. `python -m json.tool reports/formal_expansion/calcite_hep_speedup_run_v0.json >/dev/null`
7. `python -m scripts.cli formal-calcite-hep-speedup-run --execute`
8. `python -m json.tool reports/formal_expansion/calcite_hep_speedup_run_v0.json >/dev/null`

Operational note:

- PostgreSQL execution required rerunning the execute commands outside the sandbox to reach the validated Windows-host PostgreSQL path from WSL.

## Canary Result

Bounded canary on `PERF_0006`:

- `executed_count:` `1`
- `success_count:` `1`
- `failed_count:` `0`
- `valid_speedup_case_count:` `1`
- `row_count_match_count:` `1/1`
- `GM_Speedup:` `0.9497362691824345`
- `W/T/L:` `0/0/1`
- `RegressionRate@20%:` `0.0`

Canary interpretation:

- the speedup runner executed source and Calcite candidate SQL successfully under `perf_0006_validation, public`
- checker-backed gating held before scoring
- the candidate was slightly slower than source, but not by the 20% regression threshold

## Full 4-Case Result

Final bounded 4-case speedup result:

- `case_count:` `4`
- `executed_count:` `4`
- `success_count:` `4`
- `failed_count:` `0`
- `valid_speedup_case_count:` `4`
- `row_count_match_count:` `4/4`
- `row_count_mismatch_count:` `0/4`
- `GM_Speedup:` `0.9588741913559858`
- `W/T/L:` `0/3/1`
- `RegressionRate@20%:` `0.0`
- `failure_categories:` none

Per-case medians and outcome:

| case_id | source median ms | candidate median ms | speedup_ratio | W/T/L | row-count match |
| --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `0.284036` | `0.298741` | `0.9507767598019691` | `tie` | yes |
| `PERF_0008` | `0.346369` | `0.347438` | `0.9969231920515313` | `tie` | yes |
| `PERF_0033` | `0.288131` | `0.307096` | `0.9382440670018497` | `loss` | yes |
| `PERF_0054` | `0.214504` | `0.225655` | `0.950583855886198` | `tie` | yes |

Observed pattern:

- no case cleared the `>1.05` win threshold
- three cases landed inside the tie band
- one case (`PERF_0033`) was a loss
- no case crossed the `1.2x` regression threshold

## Interpretation

What this proves:

- Calcite HEP is now speedup-scored on the bounded 4-case PostgreSQL checker-backed subset
- all four scored cases preserved row-count agreement during runtime repeats
- the runtime effect is near-neutral to mildly negative on this subset

What this does not prove:

- this is not a final Calcite HEP baseline result
- this is not a broader leaderboard result
- this does not justify any registry, admission, or formal review state change

## Failed Cases

Final failed cases:

- none

## Next Action

The bounded 4-case speedup run is now complete.

The correct next interpretation boundary is:

- record this as a bounded PostgreSQL-only subset result
- do not overstate it as a final Calcite HEP baseline
