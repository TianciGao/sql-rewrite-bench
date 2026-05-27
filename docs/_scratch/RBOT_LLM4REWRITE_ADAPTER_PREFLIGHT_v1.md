# RBOT_LLM4REWRITE_ADAPTER_PREFLIGHT_v1

## 0. Purpose And Boundary

This is adapter-readiness preflight only.

It is not implementation.
It is not method execution.
It is not a model call.
It is not DB execution.
It is not leaderboard evidence.
It is not an R-Bot result.

## 1. Current Status Change

`R-Bot` is no longer pure `unavailable_blocked`.

An upstream substrate candidate now exists via `curtis-sun/LLM4Rewrite`, and the repo-local planning status should be updated to:

`external_substrate_found_runnable_after_adapter_possible`

That status change is narrow. No RewriteBench adapter exists yet, and no bounded RewriteBench smoke has been run.

## 2. LLM4Rewrite Runtime Contract Observed

Observed runtime contract from README and visible code:

- OS/runtime:
  - Ubuntu 22.04
- Python:
  - Python 3.10
- Java:
  - OpenJDK 17.0.12
- PostgreSQL:
  - PostgreSQL 14.13
  - `psycopg2` path and PostgreSQL JDBC path are both visible
- OpenAI/API requirement:
  - documented `OPENAI_API_KEY` path
  - `OpenAIEmbedding`
  - `OpenAI(model="gpt-4o")`
  - `OpenAI(model="gpt-3.5-turbo-0125")`
  - optional `OpenAILike` path for `DeepSeek-R1-Distill-32B`
- `requirements.txt` dependencies visible:
  - `chromadb`
  - `llama_index`
  - `llama-index-vector-stores-chroma`
  - `jsonlines`
  - `jpype1`
  - `sqlglot`
  - `psycopg2`
  - `prettytable`
  - `scipy`
- Calcite/JAR requirements visible:
  - bundled `CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
  - bundled `calcite_core_main_jar/`
  - visible PostgreSQL JDBC jar and other Java dependencies
- dataset assumptions:
  - explicit `TPC-H`, `DSB`, and `Calcite`
- database assumptions:
  - six named PostgreSQL databases:
    - `tpch10`
    - `tpch50`
    - `dsb10`
    - `dsb50`
    - `calcite10`
    - `calcite10zipf`

Practical interpretation:

- the substrate is real
- the runtime is not lightweight
- the original method assumes benchmark-specific PostgreSQL database state and a prebuilt retrieval/index workflow

## 3. LLM4Rewrite Input Contract

Observed input path from README and code:

- source SQL is supplied from dataset files under repo-controlled benchmark folders such as:
  - `tpch/`
  - `dsb/`
  - `calcite/`
- schema/context is supplied from dataset-local `create_tables.sql`
- benchmark/database name is effectively hardcoded into the execution flow via `--database`
- code maps database name to dataset family:
  - `calcite`
  - `tpch`
  - `dsb`
  - optionally `hbom`
- the main runner loops over dataset directories and template files rather than accepting a RewriteBench case package directly
- the method can accept one arbitrary SQL query at the lower-level function boundary, but the packaged runners are not shaped that way

Implication for RewriteBench:

- a RewriteBench case package can likely map into the method without rewriting core method logic
- but it cannot map in directly through the stock runners
- an adapter would need to bypass dataset-directory assumptions and inject:
  - one SQL query
  - one schema DDL
  - one PostgreSQL DB config
  - one retrieval/index context

## 4. LLM4Rewrite Output Contract

Observed output path from code:

- `my_rewriter/db_utils.py` logs `Rewrite Execution Results`
- that result dict includes:
  - `used_rules`
  - `output_sql`
  - `output_cost`
  - `time`
- `test_learned_rewrite.py` also writes machine-readable `jsonl` objects containing:
  - `input_sql`
  - `input_cost`
  - `output_sql`
  - `output_cost`
  - `used_rules`
  - `rewrite_time`
- `rag_rewrite.py` logs:
  - intermediate suggestions
  - selected rules
  - arranged rule sequence
  - rearranged rule sequence

Practical interpretation:

- `output_sql` is visible and captureable
- candidate SQL appears deterministic enough to artifact if the runtime path is held fixed
- selected rules and some retrieval/rewrite trace are accessible via logs
- failure modes are mostly log-driven rather than cleanly normalized into a dedicated machine-readable taxonomy

## 5. RewriteBench Adapter Gap

Exact adapter work required later:

- map RewriteBench case package to LLM4Rewrite single-query input
- map RewriteBench schema/DDL into the expected `create_tables` path
- map RewriteBench PostgreSQL connection/config into `init_db_config`
- define the retrieval/index setup boundary:
  - whether upstream bundled assets are sufficient
  - whether Chroma index rebuild is required
  - whether index artifacts must be pinned separately
- capture generated SQL in a stable artifact path
- capture selected rules and retrieval/rewrite trace
- feed generated SQL into the existing PostgreSQL checker/speedup pipeline
- capture token/cost logging if API models are used
- map method-side failures into RewriteBench failure taxonomy

Most important gap:

- the original upstream runners are benchmark-loop runners, not case-package runners

## 6. First Bounded Smoke Proposal

If later approved:

- PostgreSQL-only first
- `1` case first, then at most `3`
- candidate first cases:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
- no registry writeback
- no leaderboard claim

Claim boundary:

`bounded_RBot_LLM4Rewrite_adapter_smoke_only_not_full_prior_method_coverage`

## 7. Must Not Conflate

- the `LLM4Rewrite` R-Bot path must not be conflated with the embedded `LearnedRewrite` jar path
- an `R-Bot` result must not be reported as a `LearnedRewrite` result
- the embedded `LearnedRewrite` jar needs a separate audit before any use
- `LLM4Rewrite` does not provide `LLM-R2` coverage

## 8. Blocking Questions Before Any Execution

- Is OpenAI API allowed for this baseline?
- Can the RAG index be built reproducibly?
- Are the knowledge-base assets complete and licensed for reuse?
- Can the method run without its original `TPC-H` / `DSB` / `Calcite` DB setup?
- Can one RewriteBench case be injected cleanly?
- Can `output_sql` be captured without manual interpretation?
- Can selected rules and retrieval trace be captured?
- Can token/cost be logged?
- Is the license acceptable?

## 9. Recommended Next Step

Recommended next step: acquire missing runtime/data dependencies first.

Reason:

- the upstream substrate is real
- but the current execution path still assumes:
  - benchmark-specific PostgreSQL databases
  - retrieval/index setup
  - API/runtime policy decisions
- a no-execution adapter scaffold would still be guessing about those boundaries too early

## 10. Non-Modification Note

No method execution occurred.
No DB execution occurred.
No model call occurred.
No SQLGlot route was run.
No package was installed.
No adapter, script, case, registry, review, rules, or `docs/EXECUTION_STATUS.md` file was modified.
