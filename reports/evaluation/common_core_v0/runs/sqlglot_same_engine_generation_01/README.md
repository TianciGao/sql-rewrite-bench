# SQLGlot Same-Engine Generation-Only Canary

This package records a generation-only SQLGlot canary over the full Common-core v0 denominator.

Boundaries:
- no database execution
- no SQL execution against PostgreSQL, MySQL, or Spark
- no timing
- no result-consistency claim
- no executable-rate, speedup, or regression metric claim
- no same-engine leaderboard file

Artifacts:
- `run_manifest.json`
- `generation_event_long.csv`
- `generation_summary.csv`
- `generated/<case_id>/<engine>/<route_id>.sql` for successful generation outputs

Interpretation:
- `generation_success` means SQLGlot parsed and generated SQL text for the requested engine/route
- `generation_failed` means parse or generation failed before any execution step
- `is_noop_output=yes` means the generated SQL normalizes to the same SQL as the parsed source for that engine dialect
- PORT caveats remain explicit in row notes and do not imply executability on engines where controls-native-source support was skipped/unsupported
