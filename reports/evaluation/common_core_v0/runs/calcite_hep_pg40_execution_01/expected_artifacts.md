# Expected Artifacts

## Required

- `execution_plan.md`
- `execution_command_matrix.csv`
- `run_manual_calcite_hep_pg40_execution.sh`
- `README.md`
- `run_results.json`

## Logs

- `logs/<case>__pg__calcite_hep_pg_rewrite.stdout.log`
- `logs/<case>__pg__calcite_hep_pg_rewrite.stderr.log`

## Per-row Outputs

Under `workspaces/<case_id>/pg/`:

- `source.tsv`
- `generated.tsv`
- `result_check.json`

## Run-level Summary

`run_results.json` should record:

- planned rows
- rows ready to execute
- rows preserved as `not_executed_generation_failed`
- counts by observed execution status
- counts by consistency status
- full row records

## Not Produced By This Package

- no timing outputs
- no speedup outputs
- no leaderboard outputs
