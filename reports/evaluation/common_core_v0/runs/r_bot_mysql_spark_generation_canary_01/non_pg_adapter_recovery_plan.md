# Non-PG Adapter Recovery Plan

## Goal

Allow the six-row MySQL/Spark canary to attempt **generation only** without:

- pretending non-PG rows are PostgreSQL
- calling MySQL or Spark databases
- using witness-data SQL as execution input

## Recovery approach

The canary runner now uses a temp-runtime patch derived from the retained PG expansion route, with these non-PG changes:

1. It copies the visible upstream `LLM4Rewrite` tree into a temp runtime under `/tmp`.
2. It provisions the retained RAG JSONL corpus files into `runtime_root/rag/`.
3. It links or copies the formal Chroma index into `runtime_root/rag/chroma_db`.
4. It strips stale JAR signature entries from the copied runtime `LearnedRewrite.jar`.
5. It materializes `runtime_root/my_rewriter/CalciteRewrite/out/artifacts/LearnedRewrite_jar` so upstream `rewrite.py` can resolve its local classpath from the subprocess working directory.
6. It removes live DB cost/execution dependencies from:
   - `my_rewriter/test_utils.py`
   - `my_rewriter/db_utils.py`
7. It replaces `my_rewriter/database.py` with a generation-only stub `DBArgs` class so non-PG rows do not hit the PostgreSQL-only adapter path.
8. It patches `my_rewriter/rewrite.py` so Calcite rule matching and Java rewrite calls read the target engine from `RBOT_REWRITER_DATABASE` rather than defaulting to `PostgreSQL`.
9. It injects a target-engine system preface into LLM prompt messages so MySQL/Spark remain explicit in generation context.

## What remains intentionally unchanged

- no SQL execution
- no witness-data execution
- no timing
- no speedup
- no method-comparison updates

## Fail-closed boundaries

The runner still blocks rows if any of these fail:

- source/schema/witness metadata paths missing
- formal Chroma index missing
- required RAG JSONL files unavailable
- `CalciteRewrite/out/artifacts/LearnedRewrite_jar` missing from the temp runtime relative to subprocess cwd
- JPype Java import fails in the temp runtime
- provider env visibility missing

## Claim boundary

Even after this recovery, the package can only support:

- MySQL/Spark generation canary evidence

It still cannot support:

- execution validity evidence
- timing or speedup evidence
- leaderboard evidence
