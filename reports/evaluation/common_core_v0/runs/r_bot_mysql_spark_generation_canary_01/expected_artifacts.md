# Expected Artifacts

## Package outputs

Human-run package outputs should be written under:

- `reports/evaluation/common_core_v0/runs/r_bot_mysql_spark_generation_canary_01/`

Core package-level artifacts:

- `run_results.json`
- `run_event_long.csv`
- `logs/<case_id>/<engine>/generation.stdout.log`
- `logs/<case_id>/<engine>/generation.stderr.log`

## Row-level generated artifacts if generation succeeds

For each generated canary row:

- `generated/<case_id>/<engine>/generated.sql`
- `prompts/<case_id>/<engine>/prompt.txt`
- `raw_responses/<case_id>/<engine>/raw_response.txt`
- `traces/<case_id>/<engine>/selected_rules.json`
- `traces/<case_id>/<engine>/retrieval_trace.json`
- `metadata/<case_id>/<engine>/token_cost.json`
- `metadata/<case_id>/<engine>/provider_metadata.json`
- `metadata/<case_id>/<engine>/row_metadata.json`

## Fail-closed behavior

If the upstream MySQL/Spark route is still unsafe, the package should fail closed at preflight:

- `run_results.json` should record `status = preflight_failed`
- `run_event_long.csv` should still contain all `6` rows with explicit `preflight_blocked` status

This package should never silently drop rows or convert a blocked feasibility canary into a support claim.
