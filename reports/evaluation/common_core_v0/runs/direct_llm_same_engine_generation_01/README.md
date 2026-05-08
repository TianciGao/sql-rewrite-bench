# Direct LLM Same-Engine Generation 01

This run package materializes the full `120`-row Direct LLM same-engine generation pass for `common_core_v0_40`.

It is generation-only:

- no database activity
- no SQL execution
- no validity, timing, speedup, or leaderboard outputs
- no `run_event_long.csv` in this run

The runner reads the preflight prompt template and the full case-engine matrix, calls an OpenAI-compatible endpoint, writes prompt and raw response audit files, writes successful SQL-only generations, and records explicit row status for all planned rows in `run_results.json`.

Model selection:

- uses `DIRECT_LLM_MODEL` if present
- otherwise falls back to the canary model from `direct_llm_same_engine_generation_canary_01/run_results.json`
- if the canary result is unavailable, falls back to `gpt-4o-mini`
