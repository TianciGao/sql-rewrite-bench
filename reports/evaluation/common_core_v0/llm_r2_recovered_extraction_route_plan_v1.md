# LLM-R2 Recovered-Extraction Route Plan v1

This is planning and implementation scaffold only.

No LLM-R2 inference, PostgreSQL, MySQL, Spark, checker, timing, speedup, or
benchmark command was run for this packet.

## Route Identity

- `route_id = llm_r2_recovered_extraction_route_v1`
- new CLI scaffold command:
  `python -m scripts.cli formal-llmr2-recovered-extraction-route --case <CASE_ID> --dry-run`
- new isolated output root:
  `/tmp/rewritebench_llmr2_recovered_extraction_route_v1/<CASE_ID>/`

## Scope

This route is a separate recovered-extraction route for future review only.

It is intended to test one narrow hypothesis from the retained PG6 failure
audit:

- preserve the first matched `SELECT` or `WITH` line in staged `rewriter.py`
- strip or reject source-layer provenance comments after the SQL candidate
  boundary
- require that any recovered candidate still begins with `SELECT` or `WITH`
  before it is written as candidate SQL

## Hard Boundaries

- Do not modify existing PG9 bounded evidence files.
- Do not overwrite original fast-path artifacts.
- Do not reinterpret original-route evidence as fixed.
- Do not manually rewrite SQL semantically.
- Do not treat a recovered-route output as original-route method success.
- Any future recovered-route run must emit a new artifact family only.

## Scaffold Behavior

The `scripts/cli.py` scaffold now adds a dry-run-only recovered-route entry
point.

Current scaffold behavior:

1. validates the supported-case boundary against `LLMR2_SUPPORTED_CASE_IDS`
2. allocates a new route root under
   `/tmp/rewritebench_llmr2_recovered_extraction_route_v1/<CASE_ID>/`
3. records future artifact paths for:
   - raw `rewritten_sql_gpt` capture
   - recovered SQL candidate
   - checker handoff candidate
   - extraction audit JSON
   - staged runtime patch audit JSON
4. records the deterministic staged-runtime patch boundary for
   `runtime_root_recovered_extraction_v1/src/rewriter.py`
5. records the deterministic recovered extraction rule:
   `first_select_or_with_then_strip_trailing_source_comments_v1`
6. intentionally does not execute LLM-R2 yet

## Narrow Patch Boundary

The preferred staged-runtime patch remains:

- patch only the staged copy of `rewriter.py`
- preserve the first matched `SELECT/WITH` line instead of dropping it
- stop collecting SQL once source-comment contamination begins
- write recovered SQL only if it still starts with `SELECT` or `WITH`

The local recovered extraction guard remains:

- preserve the raw field separately
- derive a recovered candidate deterministically from that raw field
- strip trailing source-comment contamination only at the text boundary
- reject candidates that still do not begin with `SELECT` or `WITH`

## Future Artifact Family

The recovered route is expected to use a distinct artifact family, including:

- `generated_sql_schema_native_recovered_extraction_v1.sql`
- `checker_candidate_sql_schema_native_recovered_extraction_v1.sql`
- `rewritten_sql_gpt_raw_schema_native_recovered_extraction_v1.txt`
- `recovered_candidate_schema_native_recovered_extraction_v1.sql`
- `extraction_audit_schema_native_recovered_extraction_v1.json`
- `runtime_patch_audit_schema_native_recovered_extraction_v1.json`

These are separate from the original:

- `generated_sql_schema_native_v1.sql`
- `checker_candidate_sql_schema_native_v1.sql`

## Implementation Status

`scripts/cli.py` now contains:

- `LLMR2_RECOVERED_EXTRACTION_ROUTE_ID`
- `LLMR2_RECOVERED_EXTRACTION_ROUTE_ROOT`
- `llmr2_patch_rewriter_text_for_recovered_extraction(...)`
- `llmr2_recovered_extraction_from_raw_field(...)`
- `cmd_formal_llmr2_recovered_extraction_route(...)`
- parser wiring for `formal-llmr2-recovered-extraction-route`

Current scaffold limitation:

- execution mode is intentionally not enabled in this patch
- the scaffold is dry-run-only until a separate human approval decides whether
  to authorize an actual recovered-route human-run

## Why This Does Not Change PG9

The frozen PG9 bounded packet remains the original recovered-route evidence:

- `9/9` generated
- `3/9` exact-match
- `6/9` execution-failed generated SQL rows

This new scaffold only creates a possible future route for separate review.

## Recommended Next Action

Human review this recovered-extraction route scaffold and decide whether to
approve a separate recovered-route human-run plan, or stop and preserve the
current PG9 bounded evidence as final.

## Non-Claims

- This does not say LLM-R2 is fixed.
- This does not change the frozen PG9 bounded evidence packet.
- This does not authorize any recovered-route execution.
- This does not create PG40 or full `120` evidence.
- This does not update `method_comparison_summary_v2`.
