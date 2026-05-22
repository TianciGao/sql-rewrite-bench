**Expected Artifacts**

Human-run script:

- `run_manual_direct_llm_timing_canary.sh`

Run-local outputs expected after manual execution:

- `logs/env_check.stdout.log`
- `logs/env_check.stderr.log`
- `logs/<case>__<engine>__<route>.stdout.log`
- `logs/<case>__<engine>__<route>.stderr.log`
- `timings/<case_id>/<engine>/direct_llm_same_engine_rewrite.json`
- `records.tmp.jsonl`
- `run_results.json`

Per-row timing JSON minimal semantics:

- `case_id`
- `engine`
- `route_id`
- `warmup_count`
- `repeat_count`
- `source_runtime_ms`
  - list of `repeat_count` values when successful
- `generated_runtime_ms`
  - list of `repeat_count` values when successful
- `median_source_ms`
- `median_generated_ms`
- `speedup_ratio`
  - usually `median_source_ms / median_generated_ms`
- `status`
  - `success` or `failure`
- `notes`

`run_results.json` minimal semantics:

- one record for `env_check`
- one record per scoped row
- command metadata
- exit code
- stdout/stderr log paths
- timing JSON path
- copied timing medians when available
- `speedup_exclusion_reason` when a row is excluded

Boundary:

- this package is timing-canary scaffolding only
- it is not a final performance summary
- it is not a final speedup summary
- it is not a final leaderboard artifact
