# Expected Artifacts

When the human operator runs this bounded no-op control packet, it should
retain:

- `run_results.json`
- `run_event_long.csv`

Because the safe retained-evidence batch size is intentionally `0`, this packet
does not plan row workspaces, generated SQL, or execution logs.

Expected package-level outcomes:

- `previous_fail_closed_exact_ledger = 90/120`
- `planned_rows = 0`
- `recovered_exact_count = 0`
- `new_fail_closed_exact_ledger = 90/120`
- `maximum_possible_ledger_after_this_autopilot = 90/120`
- `current_benchmark_metric_evidence = false`
- `timing_denominator_id = NA_not_computed`
- `leaderboard_comparable = no`
