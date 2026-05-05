# LLMR2_LOGICAL_PLAN_FAILURE_AUDIT_PERF_0006_v1

## 0. Purpose And Boundary
This is a read-only logical-plan failure audit for bounded LLM-R2 fast-path execution on `PERF_0006`.

No rerun occurred. No OpenAI/API call occurred in this audit. No Java rule applier ran in this audit. No DB, checker, or speedup step ran.

## 1. Failure Recap
Current bounded state:
- one-row fast path works
- CPU-only execution works past the prior device mismatch
- schema-list contract works
- current blocker is upstream `get_logical_plan(...)` / `create_nested_tree(...)` before prompt/API dispatch

The latest failure came from:
- `logical_plan = get_logical_plan(db_id, edit_queries(query))`
- `create_nested_tree(...)`
- `IndexError: list index out of range`

## 2. Artifact Inspection
- smoke result path:
  `/tmp/rewritebench_llmr2_fast_path/PERF_0006/smoke_result_schema_fix_v1.json`
- staged query CSV path:
  `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/queries/queries_rewritebench_perf_0006_test.csv`
- staged schema path:
  `/tmp/rewritebench_llmr2_fast_path/PERF_0006/runtime_root_v1/data/data_llmr2/schemas/rewritebench_perf_0006.json`
- generated SQL exists: no
- result CSV exists: no

Staged query text:
- still includes the full RewriteBench frozen file body, including leading `-- ...` comment lines
- the first non-comment SQL line is `select`

`edit_queries(query)` effect:
- it likely leaves the query structure intact
- it rewrites tokens like ` date ` to ` calcite_date `
- it also rewrites the cutoff line inside comments from `DATE` to `calcite_DATE`
- it does not strip comments

Observed stdout/stderr evidence:
- stdout still contains upstream `rewriter.py` import-time example SQL noise
- stdout also shows:
  - `preprocess time: ...`
  - `query pool embeddings collected`
- stderr shows the failure after that point:
  - `IndexError: list index out of range`

## 3. Upstream Logical-plan Path Analysis
Definition locations:
- `edit_queries(...)`: [LLM_R2.py](/tmp/rewritebench_llmr2_audit/LLM-R2/src/LLM_R2.py:275)
- `get_logical_plan(...)`: [get_query_meta.py](/tmp/rewritebench_llmr2_audit/LLM-R2/src/get_query_meta.py:80)
- `create_nested_tree(...)`: [get_query_meta.py](/tmp/rewritebench_llmr2_audit/LLM-R2/src/get_query_meta.py:53)

Logical-plan path:
1. `LLM_R2.py` calls `logical_plan = get_logical_plan(db_id, edit_queries(query))`.
2. `get_logical_plan(...)` sends `[db_id, sql_input]` to Java:
   - `java -cp rewriter_java.jar src/get_logical_plan.java`
3. Java `get_logical_plan.java`:
   - reads `data/data_llmr2/schemas/<db_id>.json`
   - constructs `Rewriter(schemaJson)`
   - runs `rewriter.SQL2RA(testSql)`
   - prints `testRelNode.explain()`
4. Python receives the explain text, strips a success banner if present, computes:
   - `nodes = [...]`
   - `heights = [...]`
5. `create_nested_tree(heights, nodes, True)` assumes the explain output has at least one child at indentation level `root_h + 1`.

Important contract facts:
- `get_logical_plan(...)` does not appear to require a hardcoded dataset name beyond locating `schemas/<db_id>.json`.
- it does invoke Java plan extraction, but this audit did not run it
- there is no cached logical-plan path on the Python side here; the parser expects raw explain text from Java

Why `create_nested_tree(...)` can fail:
- for trees longer than 3 lines, it computes:
  - `left_root = [i for i, x in enumerate(heights) if x == root_h + 1][0]`
- if no node exists at `root_h + 1`, the list is empty and `[0]` raises `IndexError`
- so the parser assumes a specific indentation pattern in the explain output

## 4. Diagnosis
Primary diagnosis:
- `malformed_logical_plan_text`

Why this is the best fit:
- the schema contract mismatch is already resolved
- the failure occurs after Java-side plan generation is invoked and after the Python side starts parsing the textual plan
- the immediate exception is not a SQL parse error or schema lookup error; it is a tree-shape assumption failure in `create_nested_tree(...)`
- the most likely cause is that the explain text produced for the bounded `PERF_0006` query does not satisfy the parser’s expected indentation/child-layout contract

Contributing adapter risk:
- the staged query still includes many leading comment lines and a RewriteBench narrative wrapper
- that may influence Java/Calcite output shape, but the direct exception is still the malformed-plan-text / parser-assumption failure rather than a plain db-id or schema-file miss

## 5. Recommended Next Step
- `implement bounded logical-plan probe`

Reason:
- the least invasive next step is to capture the raw Java logical-plan output for this exact staged query before the Python tree parser runs
- that will determine whether:
  - the query comments / formatting need normalization
  - the Java extractor emits an unexpected explain format
  - or `create_nested_tree(...)` simply needs a bounded guard / fallback for unary or irregular plan shapes

`patch query formatting and retry` is premature before the raw explain text is captured.

## 6. Non-Modification Note
No rerun, model/API call, Java invocation, DB access, checker, or speedup occurred in this audit.

No repo state was changed except this scratch report.
