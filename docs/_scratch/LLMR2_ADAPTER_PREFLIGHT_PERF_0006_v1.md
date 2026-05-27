# LLMR2_ADAPTER_PREFLIGHT_PERF_0006_v1

## 0. Purpose And Boundary
This note is a no-execution adapter preflight only for mapping RewriteBench `PERF_0006` into the official `LLM-R2` repository contract. It does not execute LLM-R2, does not call any model/API, does not run Java rule application, does not run any database, and does not run checker or speedup.

## 1. Target Case
- `case_id`: `PERF_0006`
- source SQL path: `cases/PERF/PERF_0006/source.sql`
- PG DDL path: `cases/PERF/PERF_0006/schema/ddl_pg.sql`
- witness data path: `cases/PERF/PERF_0006/validation/pg_witness_data.sql`
- file existence:
  - source SQL: yes
  - PG DDL: yes
  - PG witness data: yes

## 2. LLM-R2 Substrate Inputs
- repo path: `/tmp/rewritebench_llmr2_audit/LLM-R2`
- main script path: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/LLM_R2.py`
- learned rewriter path: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/learned_rewriter_pg.py`
- rule assets: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/rules_for_selected/`
- demo pools: `/tmp/rewritebench_llmr2_audit/LLM-R2/data/data_llmr2/pools/`
- checkpoint assets: `/tmp/rewritebench_llmr2_audit/LLM-R2/src/simcse_models/tpch/pytorch_model.bin`
- schema examples: `/tmp/rewritebench_llmr2_audit/LLM-R2/data/data_llmr2/schemas/`
- output SQL contract visible: yes
  - `LLM_R2.py` writes `rewritten_sql_gpt`
  - `learned_rewriter_pg.py` returns `rewrite_query`

## 3. Adapter Bundle
- temp bundle path: `/tmp/rewritebench_llmr2_adapter_preflight/PERF_0006`
- query CSV created: yes
  - `perf_0006_queries.csv`
  - one bounded row with:
    - `db_id = rewritebench_perf_0006`
    - `original_sql = PERF_0006 source SQL`
- schema stub created: yes
  - `perf_0006_schema_stub.json`
  - derived from `ddl_pg.sql`
  - marked as adapter stub rather than official LLM-R2 dataset schema
- metadata created: yes
  - `llmr2_case_metadata.json`
- expected command documented: yes
  - `expected_command_NOT_RUN.txt`
- output capture documented: yes
  - `output_capture_contract.md`

## 4. Contract Gaps
- schema JSON may be approximate
- demo pool selection contract
- API/model requirement
- rule applier Java path
- result CSV capture
- license unresolved if the upstream repo still lacks a root license file

## 5. Future Smoke Readiness
`adapter_preflight_ready_not_executed`

The substrate assets needed for a one-case adapter dry-run are present, and the mapping bundle now exists, but no execution path has been exercised yet.

## 6. Recommended Next Step
`implement single-case LLM-R2 runner dry-run`

Reason:
- the next open question is runner wiring rather than repository acquisition
- the bundle now provides the one-row query CSV, schema stub, future command shape, and output capture contract needed for a dry-run scaffold

## 7. Non-Modification Note
No execution occurred. No model/API call occurred. No Java rule applier was run. No database was run. No checker or speedup was run. No registry, review, rules, `docs/EXECUTION_STATUS.md`, or case files were changed. The long-standing taxonomy notes were untouched.
