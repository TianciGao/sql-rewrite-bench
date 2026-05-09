# R-Bot PG40 Generation Expansion Failure Triage

## Observed Failures

The first human-run `r_bot_pg40_generation_expansion_02` attempt reached the generalized PG route and failed uniformly across all `40` PG rows before any raw-response generation.

### Cleared blocker

Representative stderr from the first failure:

`java.lang.SecurityException: Invalid signature file digest for Manifest main attributes`

Failure import chain:

- `my_rewriter/my_utils.py`
- `rag.gen_rewrites_from_rules`
- `my_rewriter.rewrite`
- `from rewriter import Rewriter, RewriteResult, MyRules`
- JPype Java import fails

That blocker has now been addressed by using an unsigned temp runtime copy of `LearnedRewrite.jar` inside `/tmp`.

### Current blocker

After the JAR-signature patch, the next human-run failure moved forward and now stops in upstream retrieval corpus initialization:

`FileNotFoundError: [Errno 2] No such file or directory: '../rag/stackoverflow-rewrite-query-optimization.jsonl'`

Representative path:

- `runtime_patch_v4/my_rewriter/rag_retrieve.py`
- `init_docstore`
- `read_docs('../rag/stackoverflow-rewrite-query-optimization.jsonl')`

## Root Cause Hypothesis

The remaining harness blocker is not row-specific SQL. It is temp-runtime provisioning:

- upstream retrieval code expects JSONL corpus members under `../rag/` relative to `runtime_root/my_rewriter`
- the copied temp runtime did not provide those extracted JSONL files
- the subprocess `cwd` itself is correct, but `../rag/...` still fails because the files are absent

The earlier JAR-signature failure came from copying the upstream `LearnedRewrite.jar` directly from:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`

That upstream JAR still contains stale signature entries:

- `META-INF/DUMMY.SF`
- `META-INF/DUMMY.DSA`

The known-good PG7 runtime copy does **not** contain those entries. The successful PG7 path removed them before JPype import.

So the original failure was a temp-runtime JAR-signature/classpath issue, not:

- API visibility
- provider/base_url visibility
- case SQL shape
- case schema/data availability
- row-specific retrieval quality

The current failure is a temp-runtime RAG-corpus provisioning / upstream relative-path satisfaction issue, not:

- API visibility
- provider/base_url visibility
- case SQL shape
- case schema/data availability
- engine-level PostgreSQL incompatibility

## Comparison Against Known-Good PG7 Runtime

Known-good PG7 behavior:

- copied the runtime JAR into a temp runtime directory
- removed stale `META-INF/*.SF` / `*.DSA` / `*.RSA` entries from the copied `LearnedRewrite.jar`
- ran with the upstream retrieval corpus files available to the runtime
- then imported `Rewriter`, `RewriteResult`, and `MyRules` successfully

Broken PG40 expansion behavior before the first patch:

- copied the signed upstream JAR directly
- did not remove stale signature entries
- attempted JPype import immediately
- failed before row-level generation work

Broken PG40 expansion behavior after the first patch:

- cleared the JPype/JAR failure
- still copied a temp runtime without the extracted upstream JSONL corpus files
- reached `init_docstore`
- failed on `../rag/stackoverflow-rewrite-query-optimization.jsonl`

## Classification

The cleared failure was:

- `java_classpath_or_jar_signature_failure`

The current blocker should be classified as:

- `missing_rag_jsonl_runtime_corpus`

It should **not** be classified as:

- case-specific SQL failure
- LLM response failure
- unsupported PostgreSQL route
- method-level rejection of the 40 PG rows

## Required Fix

The runner must:

1. keep using an unsigned temp runtime copy of `LearnedRewrite.jar`
2. provide the required upstream JSONL corpus files under `runtime_root/rag/`
3. prefer symlinking/copying visible upstream JSONL files if they exist
4. otherwise extract the required JSONL members from `stackoverflow-rewrite-embed.zip` into the temp runtime only
5. keep the retained upstream ZIP and upstream source tree untouched
6. run a fail-closed package preflight before the 40-row loop:
   - verify formal Chroma index visibility
   - verify required RAG JSONL files exist at the actual runtime path
   - verify Java import still succeeds
7. stop the run if preflight fails

That is now the expected behavior of the patched package runner.
