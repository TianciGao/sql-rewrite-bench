# Backfill Policy v1

This packet runs checker/result comparison only on retained `source.sql` and retained SQLGlot generated SQL.

Routes:
- `sqlglot_transpile_same_dialect_noop`
- `sqlglot_optimize_same_dialect`

Backfill scopes:
- `noop_reconstructed_72`
- `optimize_reconstructed_56`
- `optimize_port_execution_only_9`

No SQLGlot generation was rerun. No timing was run.
