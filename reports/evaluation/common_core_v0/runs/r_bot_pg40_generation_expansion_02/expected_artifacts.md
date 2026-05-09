# Expected Artifacts

Package-level artifacts written by the human-run script:

- `run_event_long.csv`
- `run_results.json`
- `logs/_preflight/java_import_preflight.stdout.log`
- `logs/_preflight/java_import_preflight.stderr.log`
- `logs/<case_id>/pg/generation.stdout.log`
- `logs/<case_id>/pg/generation.stderr.log`

Per-row retained artifacts:

- `generated/<case_id>/pg/r_bot_same_engine_rewrite.sql`
- `prompts/<case_id>/pg/prompt.txt`
- `raw_responses/<case_id>/pg/response.txt`
- `traces/<case_id>/pg/selected_rules.json`
- `traces/<case_id>/pg/retrieval_trace.json`
- `metadata/<case_id>/pg/token_cost.json`
- `metadata/<case_id>/pg/provider_metadata.json`
- `metadata/<case_id>/pg/row_run_metadata.json`

Row-level status policy:

- `generated`
- `failed`
- `blocked`

All 40 PG rows must remain explicit. No row may be dropped from the denominator.

This package does not produce execution, validity, timing, speedup, or leaderboard artifacts.

If the Java import preflight fails, `run_results.json` must record:

- `preflight_status = runtime_rag_corpus_preflight_failed`, `formal_index_preflight_failed`, or `java_import_preflight_failed`
- `preflight_failure_category = missing_rag_jsonl_runtime_corpus`, `missing_formal_index_dir`, or `java_runtime_or_upstream_rag_resolution_failure`

and the runner must stop before the 40-row loop.
