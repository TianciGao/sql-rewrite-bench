# Direct LLM Same-Engine Generation Protocol

## Role

This package defines the generation-only protocol for a reproducible Direct LLM baseline on `common_core_v0_40`.

It does not call any LLM or API in this task.
It does not execute SQL.
It does not produce validity, timing, speedup, or leaderboard claims.

## Denominator And Identity

- `denominator_id = common_core_v0_40`
- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`
- planned rows = `120` (`40` cases x `3` engines)

All `120` case-engine rows remain explicit in the generation matrix. `PORT` rows must not be silently dropped.

## Initial Generation Shape

The initial Direct LLM run plans one candidate rewrite per `case_id x engine` row.

- one output SQL file per row
- same-engine only
- no cross-engine translation in this package
- no retry tree or N-best tree in the initial run

## Prompt Contract

The prompt must:

- request a semantics-preserving rewrite
- specify the target engine
- include the source SQL
- include same-engine schema when available
- require SQL-only output
- forbid markdown fences
- forbid explanations
- forbid new comments unless comments already exist in the SQL
- forbid DDL and data-changing statements
- preserve result semantics
- avoid engine-incompatible functions

## Output Contract

The first run should write generated SQL only under:

- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated/<CASE>/<engine>/direct_llm_same_engine_rewrite.sql`

This preflight does not create:

- `run_event_long.csv`
- `method_case_summary.csv`
- timing outputs
- speedup outputs
- leaderboard outputs

## Governance Boundary

Direct LLM remains separate from SQLGlot until it has its own:

- generation evidence
- execution evidence
- validity summary
- timing evidence
- speedup summary

Therefore no multi-method leaderboard comparison is valid yet on `common_core_v0_40`.

## PORT Boundary

`PORT` cases remain in the planned `120` rows. Unsupported or caveated same-engine downstream rows must remain explicit later in execution/materialization rather than disappearing during generation planning.

## Readiness In This Task

This preflight confirms only that prompt inputs are assembled and output targets are defined. No model call is made in this task.
