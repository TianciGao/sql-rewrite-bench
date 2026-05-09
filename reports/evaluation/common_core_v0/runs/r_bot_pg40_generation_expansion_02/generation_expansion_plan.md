# R-Bot PG40 Generation Expansion Plan

## Scope

- Method: `r_bot`
- Route: `r_bot_same_engine_rewrite`
- Source denominator reference: `common_core_v0_40_same_engine_120`
- Expansion run denominator: `common_core_v0_40_pg40`
- Engine scope: `pg` only
- Planned rows: `40`

This package is a **new** denominator-aware PG-only expansion run. It does not overwrite the existing PG7 formal evidence and it does not create any tri-engine claim.

## Goal

Attempt all `40` PostgreSQL rows through a generalized PG route instead of the old recovered-harness support whitelist.

Rows are carried forward with explicit prior classifications:

- `previously_generated_pg7`
- `previously_failed_pg2`
- `previously_blocked_pg31`

## Key Design Choice

The expansion runner is generation-only and stays within the task boundary:

- no database connection
- no DDL/DML execution
- no query execution
- no timing
- no speedup

To do that, the human-run script patches the copied upstream runtime **outside the repo** at run time so that:

1. retrieval still uses the retained formal Chroma index
2. rule-vector width remains `100`
3. generation still runs retrieval + rule selection + rewrite
4. DB cost-estimation calls are disabled for the expansion run

This preserves a bounded PG generation attempt route without silently reintroducing SQL execution into the generation phase.

## Runtime Patch Shape

Per row, the human-run script will:

1. Copy the visible upstream `LLM4Rewrite` tree into a fresh temp runtime directory.
2. Replace `rag/chroma_db` in that temp runtime with the retained formal index at `/tmp/rewritebench_rbot_formal_chroma_index_01`.
3. Patch the copied runtime so:
   - `my_rewriter/test_utils.py` no longer creates a live `Database()` just to compute `input_cost`
   - `my_rewriter/db_utils.py` no longer computes `output_cost` through DB execution
   - `my_rewriter/config.py` uses the formal model from the retained parameter freeze
   - `rag/my_query_fusion_retriver.py` aligns the rule-vector width to `100`
   - the copied `LearnedRewrite.jar` has stale `META-INF/*.SF` and `*.DSA` signature entries removed in the temp runtime copy only
   - the copied runtime `rag/` directory contains the required upstream JSONL corpus files, sourced from visible upstream files or extracted from the retained ZIP into the temp runtime only
4. Run the patched runtime with the formal Python environment and visible `OPENAI_API_KEY`.
5. Extract row artifacts into this package.

Before the row loop, the runner now performs a fail-closed package preflight against the patched temp runtime:

- verify the formal Chroma index directory is visible
- verify the required `rag/*.jsonl` files exist at the actual runtime path used by the subprocess
- `import my_rewriter.rewrite`
- `from rewriter import Rewriter, RewriteResult, MyRules`

If that preflight fails, the run stops before any of the 40 row attempts.

## Why This Is Bounded

This package is intentionally narrower than a full method recovery:

- it only expands PostgreSQL coverage
- it keeps MySQL/Spark unsupported
- it avoids SQL execution in the generation phase
- it preserves explicit failed/blocked row states rather than forcing apparent success

## Expected Outcomes

For each PG row, the expansion run will end in one of:

- `generated`
- `failed`
- `blocked`

No row is dropped. All 40 rows remain explicit in:

- `generation_command_matrix.csv`
- `run_event_long.csv`
- `run_results.json`

## Non-Claims

This package does **not**:

- replace the existing R-Bot PG7 result card
- create execution evidence
- create validity evidence
- create timing evidence
- create speedup evidence
- create leaderboard-comparable evidence

## Human-Run Readiness

The package is ready for human-run generation if:

- `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python` exists
- `/tmp/rewritebench_rbot_formal_chroma_index_01` exists
- `reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json` exists
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite` is visible
- `OPENAI_API_KEY` is visible in the shell

MySQL/Spark remain out of scope for this expansion package.
