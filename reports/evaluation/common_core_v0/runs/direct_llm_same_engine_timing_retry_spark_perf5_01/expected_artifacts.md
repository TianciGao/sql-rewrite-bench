# Expected Artifacts

This retry package is expected to produce the following artifacts when the human-run script is executed:

## Package-Level Outputs

- `run_results.json`
- `logs/env_check.stdout.log`
- `logs/env_check.stderr.log`

## Per-Row Outputs

For each of the five retry rows:

- `logs/<case_id>__spark__direct_llm_same_engine_rewrite.stdout.log`
- `logs/<case_id>__spark__direct_llm_same_engine_rewrite.stderr.log`
- `workspaces/<case_id>/spark/direct_llm_same_engine_rewrite/`
- `timings/<case_id>/spark/direct_llm_same_engine_rewrite.json`

## Recorded Timing Fields

Each per-row timing JSON is expected to record:

- `source_runtime_ms`
- `generated_runtime_ms`
- `median_source_ms`
- `median_generated_ms`
- `speedup_ratio`
- `status`
- `notes`

## Non-Goals

This retry package must not create:

- final `GM_Speedup`
- final `RegressionRate@20%`
- `same_engine_leaderboard.csv`
