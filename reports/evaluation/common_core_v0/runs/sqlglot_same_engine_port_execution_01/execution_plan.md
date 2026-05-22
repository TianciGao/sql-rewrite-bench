**Execution Plan**
This package prepares the PORT-specific SQLGlot same-engine execution slice for Common-core v0. It keeps every portability case explicit, but executes only rows that are both generation-successful and supported by the PORT native-source accounting constraints.

Scope:
- cases: `9` PORT denominator cases
- engines: `pg`, `mysql`, `spark`
- routes: `sqlglot_optimize_same_dialect`, `sqlglot_transpile_same_dialect_noop`
- total matrix rows: `54`
- ready-to-execute rows: `9`
- explicit unsupported rows: `36`
- explicit no-op rows: `9`
- explicit generation-failed rows: `0`

Execution rules:
- run only rows with `execution_row_status=ready_to_execute`
- preserve `skipped_unsupported` rows explicitly in `run_results.json`
- preserve `not_executed_generation_failed` rows explicitly in `run_results.json`
- preserve `noop_generated` rows explicitly in `run_results.json`
- do not compute timing
- do not compute speedup or leaderboard metrics
- use the corrected runner logic from `sqlglot_same_engine_execution_canary_01`
- run from the real repository root with no `tmp_repo`

PORT-specific support rule:
- execute only on the engine where controls show `native_source` support for that PORT case
- keep all other engine rows explicit as unsupported rather than silently dropping them
- keep PORT caveats explicit in notes because these cases remain portability-stress rows with normalization and interpretation constraints

Ready rows by engine:
- `pg`: `4`
- `mysql`: `5`
- `spark`: `0`

