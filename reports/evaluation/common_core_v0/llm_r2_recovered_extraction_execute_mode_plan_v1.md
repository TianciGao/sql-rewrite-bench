# LLM-R2 Recovered-Extraction Execute-Mode Plan v1

This is planning and implementation documentation for the non-dry-run execute
mode of the recovered-extraction route.

No PostgreSQL, checker, timing, speedup, MySQL, or Spark execution is part of
this route. This route is generation-only.

## Route Identity

- `route_id = llm_r2_recovered_extraction_route_v1`
- command:
  `python -m scripts.cli formal-llmr2-recovered-extraction-route --case <CASE> --force-cpu --schema-native-contract`
- output root:
  `/tmp/rewritebench_llmr2_recovered_extraction_route_v1/<CASE_ID>/`

## Execute-Mode Scope

The new execute mode does only this:

1. stage a fresh runtime copy under
   `runtime_root_recovered_extraction_v1`
2. patch only the staged `src/rewriter.py`
3. invoke LLM-R2 only inside that staged runtime
4. preserve the raw `rewritten_sql_gpt` field
5. derive a recovered SQL candidate deterministically
6. retain recovered generated SQL only if it begins with `SELECT` or `WITH`
7. emit recovered-route artifacts only under the separate recovered route root

## Execute-Mode Output Contract

Required artifacts:

- `artifact_paths.json`
- `runtime_patch_audit_schema_native_recovered_extraction_v1.json`
- `extraction_audit_schema_native_recovered_extraction_v1.json`
- `smoke_result_schema_native_recovered_extraction_v1.json`
- `method_stdout_schema_native_recovered_extraction_v1.log`
- `method_stderr_schema_native_recovered_extraction_v1.log`
- `gpt_rewritebench_<case>_one_promo_queryCL_updated.csv` if upstream emits it
- `rewritten_sql_gpt_raw_schema_native_recovered_extraction_v1.txt` if raw field exists
- `generated_sql_schema_native_recovered_extraction_v1.sql` if recovery succeeds
- `checker_candidate_sql_schema_native_recovered_extraction_v1.sql` if recovery succeeds

## Success Boundary

The command exits `0` only if:

- the method runs to completion or at least emits a result CSV
- a raw SQL field is captured
- the recovered candidate is non-empty
- the recovered candidate begins with `SELECT` or `WITH`
- the recovered candidate passes the deterministic extraction guard
- recovered generated SQL is retained under the recovered route root

Otherwise it exits nonzero and records explicit failure metadata.

## Deterministic Recovery Rule

The execute mode uses the same narrow rule fixed in the scaffold:

- preserve the first matched `SELECT/WITH` line in staged `rewriter.py`
- stop at full-line source comments
- strip inline source-comment tails
- reject candidates that do not still begin with `SELECT/WITH`

This is boundary recovery only. It is not semantic SQL repair.

## Original-Route Boundary

This execute mode must not:

- modify existing PG9 bounded evidence
- overwrite original fast-path generated SQL
- reinterpret original-route PG9 evidence as recovered-route success

Any future recovered-route run must be reviewed as a separate route.

## Recommended Next Action

Human review the execute-mode implementation and decide whether to authorize a
bounded recovered-route human-run on selected PG6 cases.

## Non-Claims

- This does not say LLM-R2 is fixed.
- This does not create PG40 or full `120` evidence.
- This does not update `method_comparison_summary_v2`.
- This does not authorize PostgreSQL or checker execution.
