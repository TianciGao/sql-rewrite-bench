# R-Bot Formal Protocol

This directory holds the formal denominator-freeze and benchmark-entry planning package for `R-Bot` on Common-core v0 same-engine comparison.

Fixed target:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- planned rows = `120`

Contents:

- `r_bot_common_core_v0_40_same_engine_protocol.md`: formal route and denominator protocol
- `r_bot_common_core_v0_40_same_engine_candidate_matrix.csv`: full 120-row candidate matrix
- `r_bot_parameter_freeze_v1.json`: parameter freeze plus explicit unresolved blockers
- `r_bot_substrate_freeze_gate_v1.md`: substrate and benchmark-readiness gate
- `r_bot_artifact_contract_v1.md`: required retained artifact contract for a future formal run
- `r_bot_run_plan_v1.json`: machine-readable run plan for a later human-approved formal run

Boundary:

- no database is run here
- no SQL is executed here
- no LLM/API is called here
- no timing is computed here
- no speedup is computed here
- no leaderboard is created here

Interpretation:

- existing `PG1` recovery success is recovery evidence only
- it proves bounded feasibility
- it is not current benchmark metric evidence
- `R-Bot` enters comparison only after the formal `120`-row route closes its substrate, contamination, artifact, and runner gates
