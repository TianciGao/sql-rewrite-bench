# R-Bot PG40 Generation Expansion Patch Plan

## Patch Objective

Fix the remaining upstream runtime-preparation blockers in the PG40 expansion harness without changing:

- denominator scope
- engine scope
- existing PG7 retained evidence
- generation-only boundary

## Exact Patch

### 1. Keep the known-good JAR handling pattern
The runner continues to mirror the successful PG7 temp-runtime behavior:

- copy the upstream `LearnedRewrite.jar` into the temp runtime
- remove only stale signature entries from the copied temp JAR:
  - `META-INF/*.SF`
  - `META-INF/*.DSA`
  - `META-INF/*.RSA`
- replace the copied runtime JAR with the unsigned temp copy

The retained upstream JAR is not modified.

### 2. Provision the required upstream RAG JSONL corpus into the temp runtime
The runner now prepares `runtime_root/rag/` so the upstream relative-path reads under `my_rewriter/rag_retrieve.py` resolve correctly.

Required files:

- `stackoverflow-rewrite-query-optimization.jsonl`
- `stackoverflow-rewrite-rules-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-query-optimization.jsonl`
- `stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl`

Provision policy:

- prefer symlink/copy from `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/rag/` when extracted JSONL files are already visible there
- otherwise extract only the required JSONL members from `stackoverflow-rewrite-embed.zip`
- write them only into the temp runtime under `/tmp`
- do not modify the retained upstream ZIP or upstream source artifact

### 3. Add a fail-closed package preflight
Before row attempts, the runner now:

- prepares one temp runtime under `_java_preflight`
- patches the runtime, including RAG JSONL provisioning
- verifies the formal Chroma index directory is visible
- verifies the required runtime `rag/*.jsonl` files exist at the actual path used by the subprocess
- tries:
  - `import my_rewriter.rewrite`
  - `from rewriter import Rewriter, RewriteResult, MyRules`
  - open the expected `../rag/...jsonl` files from the subprocess working directory

If that import fails:

- write `run_event_long.csv` with header only
- write `run_results.json` with a clear preflight failure status:
  - `runtime_rag_corpus_preflight_failed`
  - `formal_index_preflight_failed`
  - or `java_import_preflight_failed`
- stop before the 40-row loop

### 4. Preserve row-loop runtime preparation
For each row runtime, the runner now uses the same temp-runtime preparation helper so the JAR fix and the RAG-corpus provisioning are applied consistently.

## Why This Patch Is Preferred

It is the smallest patch that matches the upstream runtime expectations without over-claiming method support.

It avoids:

- modifying retained upstream artifacts in place
- changing benchmark denominator logic
- weakening failure classification
- masking package-level harness failures as row-level SQL failures

## Expected Outcome On Rerun

Expected first-order result:

- the prior JAR-signature failure remains cleared
- the upstream retrieval corpus initialization failure should disappear
- rows should proceed past JPype import and `init_docstore()` into actual generation logic

This does **not** guarantee broad generation success. It only removes the pre-generation classpath blocker so genuine row-level outcomes can be observed.
