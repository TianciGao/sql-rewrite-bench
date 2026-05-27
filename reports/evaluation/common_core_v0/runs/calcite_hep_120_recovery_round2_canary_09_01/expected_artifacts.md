# Expected Artifacts

## Package-level

- `run_results.json`
- `run_event_long.csv`

## Per row

- `generated/<CASE>/<engine>/calcite_hep_recovery_round2_rewrite.sql`
- `workspaces/<CASE>/<engine>/source.sql`
- `workspaces/<CASE>/<engine>/generated.sql`
- `workspaces/<CASE>/<engine>/ddl_<engine>.sql`
- `workspaces/<CASE>/<engine>/<engine>_witness_data.sql`
- `workspaces/<CASE>/<engine>/source.tsv`
- `workspaces/<CASE>/<engine>/generated.tsv`
- `workspaces/<CASE>/<engine>/result_check.json`
- `logs/<CASE>/<engine>/source.stdout.log`
- `logs/<CASE>/<engine>/source.stderr.log`
- `logs/<CASE>/<engine>/generated.stdout.log`
- `logs/<CASE>/<engine>/generated.stderr.log`
- `metadata/<CASE>/<engine>/row_metadata.json`

## Package-local implementation artifacts

- `wrapper_src/CalciteHepRecoveryRound2Canary.java`

## Notes

- Spark warehouse files are temporary runtime artifacts under `/tmp` and must
  not be retained in the git-tracked package.
- Rewrite-only success or executability without `match_exact` does not increase
  the fail-closed ledger.
