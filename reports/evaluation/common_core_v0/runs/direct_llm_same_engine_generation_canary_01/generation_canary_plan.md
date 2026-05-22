# Direct LLM Same-Engine Generation Canary 01

## Scope

- denominator_id: `common_core_v0_40`
- route_id: `direct_llm_same_engine_rewrite`
- run scope: canary only
- planned rows: `9`
- cases: `PERF_0006`, `CONS_0010`, `LONGTAIL_0011`
- engines: `pg`, `mysql`, `spark`
- one rewrite candidate per case-engine row

## Boundaries

- Uses the OpenAI-compatible API environment only for generation.
- Does not run databases.
- Does not execute SQL.
- Does not compute validity, timing, speedup, or leaderboard outputs.
- Does not modify case files, registry files, `README`, or `docs/EXECUTION_STATUS.md`.

## Inputs

- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_protocol.md`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_matrix.csv`
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_run_plan.json`
- `reports/curation/common_core_v0_final_denominator.csv`

## Row Selection

The canary is a strict subset of the preflight matrix:

- `PERF_0006 x {pg, mysql, spark}`
- `CONS_0010 x {pg, mysql, spark}`
- `LONGTAIL_0011 x {pg, mysql, spark}`

## Output Contract

- Prompt text is written for each row under `prompts/<case_id>/<engine>/prompt.txt`.
- Raw model text is written for each row under `raw_responses/<case_id>/<engine>/response.txt`.
- Successful SQL-only generations are written under `generated/<case_id>/<engine>/direct_llm_same_engine_rewrite.sql`.
- Every planned row remains explicit in `run_results.json`.
- Per-row status is one of:
  - `success`
  - `format_violation`
  - `generation_failed`
