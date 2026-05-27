# R-Bot Formal Substrate Freeze 01

This directory holds the formal substrate freeze planning package for future `R-Bot` same-engine generation on:

- `denominator_id = common_core_v0_40_same_engine_120`
- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

Contents:

- `substrate_freeze_plan.md`: human-readable freeze decisions and exact missing items
- `substrate_freeze_matrix.csv`: per-item decision matrix
- `build_or_retain_substrate_plan.json`: machine-readable build/retain plan
- `r_bot_formal_index_rebuild_plan.md`: formal index rebuild and dimension policy
- `r_bot_formal_demo_policy_v1.md`: benchmark-facing demo-selection freeze plan
- `r_bot_formal_contamination_attestation_plan.md`: contamination-attestation requirements
- `r_bot_formal_run_gate_v1.md`: closed formal run gate with exact blockers

Boundary:

- no database is run here
- no SQL is executed here
- no LLM/API is called here
- no timing or speedup is computed here
- no leaderboard is created here
- no large binary artifact is copied into repo

Status:

- substrate items are covered
- formal gate remains closed
- `R-Bot` is not benchmark-ready
