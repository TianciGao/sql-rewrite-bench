# Expected Artifacts

## Package Files

- `execution_plan.md`
- `execution_command_matrix.csv`
- `run_manual_r_bot_pg15_execution.sh`
- `README.md`

## Human-Run Outputs

When the execution script is run manually, it should write:

- `run_results.json`
- `records.tmp.jsonl`
- per-row stdout/stderr logs under `logs/`
- per-row workspaces under `workspaces/`

## Per-Row Workspace Outputs

For each of the `15` rows, the script should retain:

- `source.sql`
- `generated.sql`
- `ddl_pg.sql`
- `pg_witness_data.sql`
- `source.tsv`
- `generated.tsv`
- `result_check.json`

## Boundary

These artifacts are execution/validity evidence only for
`generated_pg15_from_pg40_expansion_only`.

They do not create timing, speedup, or leaderboard evidence. They also do not
reinterpret the `25` failed PG generation rows as execution omissions, and they
do not replace the retained PG7 execution package.
