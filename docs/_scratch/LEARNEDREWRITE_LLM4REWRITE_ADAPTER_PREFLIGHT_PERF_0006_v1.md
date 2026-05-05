# LEARNEDREWRITE_LLM4REWRITE_ADAPTER_PREFLIGHT_PERF_0006_v1

## 0. Purpose And Boundary

This is a no-execution adapter preflight for embedded `LearnedRewrite` via upstream `LLM4Rewrite`, targeting `PERF_0006` as the first PostgreSQL-only smoke candidate.

No LearnedRewrite execution occurred.
No R-Bot execution occurred.
No database execution occurred.
No model/API call occurred.
No SQLGlot route, checker, or speedup run occurred.

## 1. Target Case

- `case_id`: `PERF_0006`
- source SQL path:
  - [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql)
- PG DDL path:
  - [ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/schema/ddl_pg.sql)
- witness data path:
  - [pg_witness_data.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/validation/pg_witness_data.sql)
- file existence:
  - source SQL: yes
  - PG DDL: yes
  - witness data: yes

## 2. Embedded LearnedRewrite Substrate

- jar path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
- jar exists: yes
- runner path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_learned_rewrite.py`
- runner exists: yes
- Java source path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/learned/LearnedRewriter.java`
- Java source found: yes
- `output_sql` visible: yes
  - Java emits `output_sql`
  - Python runner writes it into `res.jsonl`

## 3. Input Mapping Result

- temp bundle path:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006`
- source copied: yes
- schema copied: yes
- config stub created: yes
- expected command documented: yes
- output capture documented: yes

Bundle files created:

- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/source.sql`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/create_tables.sql`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/learnedrewrite_case_metadata.json`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/learnedrewrite_config_stub.py`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/expected_command_NOT_RUN.txt`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/output_capture_contract.md`
- `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/preflight_summary.json`

## 4. Future Smoke Readiness

- `adapter_preflight_ready_not_executed`

Current supporting classification:

- `embedded_substrate_found_adapter_preflight_possible`

## 5. Remaining Blockers Before Execution

- Java/JVM runtime verification
- PostgreSQL runtime verification if needed
- single-case execution harness not implemented
- output_sql extraction not tested
- checker handoff not run

## 6. Must Not Conflate

- LearnedRewrite result must not be reported as R-Bot result.
- R-Bot result must not be reported as LearnedRewrite result.
- embedded LearnedRewrite path is separate from the R-Bot RAG path.

## 7. Recommended Next Step

- `implement single-case LearnedRewrite runner dry-run`

Reason:

- the substrate exists
- the adapter bundle is now materialized
- the next unresolved step is a bounded no-execution or dry-run wrapper that proves command shape, logdir shape, and future `output_sql` capture path before any real invocation

## 8. Non-Modification Note

No execution occurred.
No model/API call occurred.
No DB call occurred.
No SQLGlot route ran.
No checker ran.
No speedup ran.
No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were modified.
