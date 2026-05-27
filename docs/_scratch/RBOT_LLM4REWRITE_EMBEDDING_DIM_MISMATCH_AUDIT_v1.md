# RBOT_LLM4REWRITE_EMBEDDING_DIM_MISMATCH_AUDIT_v1

## 0. Purpose And Boundary
This is a read-only audit of the embedding-dimension mismatch from the bounded `PERF_0006` R-Bot / LLM4Rewrite smoke v2. No rerun, model call, DB call, checker, speedup, or index rebuild occurred in this audit.

## 1. Smoke Failure Recap
The corrected smoke v2 reached the real model/retrieval path and then failed before candidate SQL generation with:

```text
chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 3172, got 3139
```

The failure occurred after the wrapper fresh-run-name fix had already avoided the earlier upstream log short-circuit.

## 2. Artifact Inspection
- smoke result path:
  - `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/smoke_result_v2.json`
- `method_stdout_v2.log` excerpt shows:
  - `Input Cost: 36.37`
  - matched NL rules
  - matched Calcite exploration rules
  - real `chat/completions` request
  - real `embeddings` requests
- `method_stderr_v2.log` excerpt shows the terminal failure:
  - `Collection expecting embedding with dimension of 3172, got 3139`
- Chroma index path:
  - `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db`
- Chroma files present:
  - `chroma.sqlite3`
  - one HNSW segment directory with `header.bin`, `data_level0.bin`, `length.bin`, `link_lists.bin`, `index_metadata.pickle`
- build log path:
  - `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log`
- build log excerpt:
  - node creation completed successfully
  - `Q&A Count: 2091, SQL Count: 2910, Node Count: 5459`
  - no rebuild-time failure signal

## 3. Chroma Collection Inspection
- collection names:
  - `stackoverflow`
- collection metadata:
  - sqlite `collections.dimension = 3172`
  - collection row count in `embeddings` table: `5459`
- stored embedding dimension:
  - directly recorded in sqlite as `3172`
- collection metadata table:
  - no custom dimensionality override beyond collection row

## 4. Upstream Embedding Path Analysis
### Build path
In `rag/rag_gen.py`, the default build path runs with `args.model == ''`, so it does **not** compute fresh embeddings for the stored content vectors. Instead it uses bundled JSONL embeddings:
- summary embedding: `obj['embedding']`
- SQL template embedding: `obj['embedding']`
- rule vector: one-hot from `NL_RULES + NORMAL_RULES`

Then it concatenates:
- summary embedding
- rule one-hot vector
- SQL template embedding

Because the stored collection dimension is `3172`, the build-time vector shape is consistent with:
- `1536` summary embedding
- `100` rule one-hot width
- `1536` SQL-template embedding

### Query path
In `my_rewriter/rag_retrieve.py` and `rag/my_query_fusion_retriver.py`, the smoke query path does something different:
- uses runtime `Settings.embed_model.get_query_embedding(...)` for generated rewrites
- uses runtime `Settings.embed_model.get_query_embedding(...)` for generated SQL templates
- builds a live rule one-hot vector from `matched_rules['nl']` and `matched_rules['calcite_normal']`

Then it concatenates:
- runtime query embedding
- live rule one-hot vector
- runtime SQL-template embedding

The smoke error says the live query vector was `3139`, which matches:
- `1536` runtime query embedding
- `67` live rule one-hot width
- `1536` runtime SQL-template embedding

So build and query do **not** use the same vector-construction contract.

## 5. Diagnosis
`mixed_embedding_sources`

Reason:
- build path used bundled/precomputed embeddings plus a build-time rule-vector width of `100`
- query path used runtime embeddings plus a runtime rule-vector width of `67`
- both hit the same `stackoverflow` collection
- the mismatch is therefore structural, not just a bad collection selection or generic Chroma corruption

## 6. Recommended Next Step
`temp-only retrieval config patch`

Least invasive next action:
- patch the temp smoke retrieval path so runtime query vectors are constructed to match the built `3172`-dimensional collection contract
- this is preferable to blindly rebuilding first, because the current mismatch is identifiable and localized to the temp execution path

## 7. Non-Modification Note
No rerun, model call, DB call, checker, speedup, or index rebuild occurred in this audit. No repo files were changed except this scratch report. No registry, review, rules, or `docs/EXECUTION_STATUS.md` changes occurred.
