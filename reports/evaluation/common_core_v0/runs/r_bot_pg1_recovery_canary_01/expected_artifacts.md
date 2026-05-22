# Expected Artifacts

The human-run canary script writes:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/logs/*.log`

If later actual generation succeeds, it should also write:

- `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql`

If upstream `/tmp` artifacts are present after an actual run, the package also tries to preserve:

- selected rules
- retrieval trace
- token/cost log
- method stdout/stderr

Expected blocked classes:

- `blocked_runner_missing_*`
- `blocked_retrieval_stack_missing_*`
- `blocked_policy_missing_*`
- `actual_run_not_permitted_without_RBOT_CANARY_ALLOW_ACTUAL_RUN=1`

This package does not create:

- timing artifacts
- speedup artifacts
- leaderboard artifacts
