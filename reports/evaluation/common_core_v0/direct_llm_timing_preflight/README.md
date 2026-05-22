# Direct LLM Timing Preflight

This directory holds the timing and speedup preflight package for Direct LLM same-engine Common-core v0 evaluation.

Contents:

- `direct_llm_timing_preflight.md`: human-readable eligibility and caveat summary
- `direct_llm_timing_candidate_matrix.csv`: full 120-row candidate matrix with explicit timing exclusions
- `direct_llm_timing_run_plan.json`: machine-readable run plan for a later human-run timing experiment

Boundary:

- no timing is computed here
- no speedup is computed here
- no leaderboard is created here
- validity exclusions from the prior execution phase are preserved rather than recomputed
