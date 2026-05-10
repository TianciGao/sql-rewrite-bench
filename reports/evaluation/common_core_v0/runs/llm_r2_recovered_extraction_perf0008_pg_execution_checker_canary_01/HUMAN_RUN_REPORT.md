## LLM-R2 Recovered-Extraction PERF_0008 PG Execution/Checker Canary 01

This run records a single-case PostgreSQL execution/checker canary for `PERF_0008:pg`.

Scope:
- case_id: `PERF_0008`
- route_id: `llm_r2_recovered_extraction_route_v1`
- candidate source: retained recovered-extraction generated SQL
- execution scope: PostgreSQL source execution + PostgreSQL generated execution + exact TSV checker

Boundary:
- no timing
- no speedup
- no MySQL
- no Spark
- no PG6 expansion
- no PG9 expansion
- no full120 expansion
- no result card
- no proposed row
- no `method_comparison_summary_v2` update

Execution input note:
- original recovered SQL was preserved unchanged
- a semicolon-normalized execution copy was created only for execution input

Observed result:
- source execution: success
- generated execution: success
- checker status: consistent
- consistency status: consistent
- source row count: `1`
- candidate row count: `1`
- speedup status: `not_run`

Primary retained artifacts:
- `candidate_input/generated_sql_schema_native_recovered_extraction_v1.sql`
- `candidate_input/generated_sql_schema_native_recovered_extraction_v1_semicolon_normalized.sql`
- `retained_checker_artifacts/checker_result_v1.json`
- `retained_checker_artifacts/checker_source_v1.tsv`
- `retained_checker_artifacts/checker_candidate_v1.tsv`
- `validation/scope_attestation.txt`
- `validation/result_summary.json`
- `command_used.txt`

Non-claims:
- This does not reinterpret or overwrite the frozen original-route PG9 bounded evidence.
- This does not claim PG40 evidence.
- This does not claim full120 evidence.
- This does not claim MySQL/Spark support.
- This does not claim timing or speedup evidence.
