# Direct LLM Preflight

This package prepares a reproducible Direct LLM same-engine generation baseline on `common_core_v0_40` without making any LLM or API call.

Current scope:
- `denominator_id = common_core_v0_40`
- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`
- planned rows = `120`
- one candidate rewrite per `case_id x engine`

Coverage:
- by pool: `performance=48`, `consistency=27`, `portability=27`, `longtail=18`
- by engine: `pg=40`, `mysql=40`, `spark=40`
- prompt-input-ready rows: `120/120`

Important boundaries:
- no generated SQL is created in this task
- no `run_event_long` is created in this task
- no validity, timing, speedup, or leaderboard claim is made in this task
- Direct LLM stays separate from SQLGlot until Direct LLM has its own generation, execution, timing, and speedup evidence on `common_core_v0_40`

PORT note:
- all `9` portability cases remain explicit in the generation matrix
- unsupported or caveated downstream same-engine rows must remain explicit later rather than being silently dropped
- portability cases in scope: `PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025`
