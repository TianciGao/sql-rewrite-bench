# Expected Artifacts

## Package Files

- `generation_plan.md`
- `generation_command_matrix.csv`
- `run_manual_r_bot_generation.sh`
- `README.md`

## Retained Formal Output Root

When the human-run generation script is executed, the retained formal outputs
must be written under:

- `reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01/`

## Row-Level Output Families

For each denominator row, the script is designed to write or preserve:

- generated SQL
- prompt text
- raw response text
- selected-rules trace
- retrieval trace
- token/cost/provider metadata
- environment snapshot
- row-level run metadata

## Package-Level Outputs

The script is designed to write:

- `run_event_long.csv`
- `generation_summary.csv`
- `run_results.json`

## Representation Rule

Blocked, unsupported, and failed rows must remain explicit.
Rows must not be dropped from denominator-aware outputs.

## Boundary

This generation package does not by itself produce benchmark metrics.
Execution, validity, timing, speedup, and leaderboard artifacts remain
downstream.
