# Expected Artifacts

## Package Files

- `execution_plan.md`
- `execution_command_matrix.csv`
- `run_manual_r_bot_pg7_execution.sh`
- `README.md`

## Human-Run Outputs

When the execution script is run manually, it should write:

- `run_results.json`
- `records.tmp.jsonl`
- per-row stdout/stderr logs under `logs/`
- per-row workspaces under `workspaces/`

## Per-Row Workspace Outputs

For each of the `7` rows, the script should retain:

- `source.sql`
- `generated.sql`
- `ddl_pg.sql`
- `pg_witness_data.sql`
- `source.tsv`
- `generated.tsv`
- `result_check.json`

## Boundary

These artifacts are execution/validity evidence only for `generated_pg7_only`.

They do not create timing, speedup, or leaderboard evidence, and they do not
upgrade the execution package into `120`-row coverage.
