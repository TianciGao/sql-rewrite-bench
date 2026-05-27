# Direct LLM Same-Engine Generation Canary 01

This run package materializes a 9-row canary for `common_core_v0_40` using the `direct_llm_same_engine_rewrite` route.

It is generation-only:

- no database activity
- no SQL execution
- no validity, timing, speedup, or leaderboard outputs

The runner reads the prompt template and case-local `source.sql` plus engine-specific schema DDL, calls an OpenAI-compatible endpoint, saves prompt and raw response audit artifacts, and writes `run_results.json` with explicit status for every planned row.

Default model behavior:

- uses `DIRECT_LLM_MODEL` if present
- otherwise defaults to `gpt-4o-mini`

Stable outputs:

- `generation_canary_plan.md`
- `generation_command_matrix.csv`
- `run_direct_llm_generation_canary.py`
- `run_results.json`
- `expected_artifacts.md`
- `prompts/`
- `raw_responses/`
- `generated/`
