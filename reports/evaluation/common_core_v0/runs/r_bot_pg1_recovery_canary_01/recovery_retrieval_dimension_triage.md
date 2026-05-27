# R-Bot PG1 Retrieval Dimension Triage

## Scope

This is a read-only triage for the `r_bot_pg1_recovery_canary_01` exploratory actual canary failure.

Boundaries preserved:

- no database run
- no SQL execution
- no API or LLM call
- no R-Bot execution
- no generated SQL modification
- no case or registry modification
- no benchmark evidence claim change

## Executive Finding

Root cause hypothesis:

- the persisted Chroma collection was built with a `3172`-dimension vector schema
- the failing runtime built a `3139`-dimension query vector at retrieval time
- the mismatch is not caused by `EMBED_DIM` alone
- the mismatch is caused by a rule-vector width drift inside the synthesized retrieval vector:
  `3172 = 1536 + 100 + 1536`
  versus
  `3139 = 1536 + 67 + 1536`

Most likely interpretation:

- the visible Chroma index was built with a `100`-wide rule-vector segment
- the visible failing runtime uses a `67`-wide rule-vector segment
- therefore the index and the runtime were not built from the same retrieval-vector contract

## Observed Run Status

From [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json):

- `technical_dry_run_ready = true`
- `exploratory_actual_run_allowed = true`
- `actual_run_attempted = true`
- `generation_status = generation_failed`
- `generated_sql_copied = false`
- `current_benchmark_metric_evidence = false`

From [smoke_actual.stdout.log](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/logs/smoke_actual.stdout.log):

- `failure_category = subprocess_nonzero_exit`
- `generation_status = method_execution_failed`
- `retrieval_vector_patch_applied = false`

From [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr_v2.log](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr_v2.log:1):

- `chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 3172, got 3139`

## Where `EMBED_DIM` Is Defined

In both visible runtime trees:

- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py:7)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/my_rewriter/config.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/my_rewriter/config.py:7)

Observed behavior:

- if `model_type` contains `open`, `Settings.embed_model = HuggingFaceEmbedding(model_name='gte-Qwen2-1.5B-instruct', ...)`
- else `Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")`
- in both branches `embed_dim = 1536`
- returned as `model_args['EMBED_DIM']`

Conclusion:

- the visible runtime `EMBED_DIM` is `1536`
- `EMBED_DIM` controls the SQL-template embedding segment width
- `EMBED_DIM` does not explain the full `3172` collection dimension

## Where The Chroma `3172` Comes From

The persisted collection dimension is directly stored in SQLite metadata.

Observed by read-only inspection of:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db/chroma.sqlite3`
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/chroma_db/chroma.sqlite3`
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/rag/chroma_db/chroma.sqlite3`

All three show:

- collection `stackoverflow`
- dimension `3172`

Build-side code path:

- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py:31)

Relevant formula in `rag_gen.py`:

- `summary_embedding` length = `1536`
- `sql_template_embedding` length = `1536`
- `sql_embedding` is the rule-vector segment
- final stored embedding:
  `summary_embedding + sql_embedding + sql_template_embedding`

Observed stored source lengths:

- `summary_embedding_len = 1536`
- `sql_template_embedding_len = 1536`

Therefore:

- `3172 - 1536 - 1536 = 100`
- the stored index implies a `100`-wide rule-vector segment

## Where The Query `3139` Comes From

Failing query vectors are synthesized in:

- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py:103)

Relevant formula:

- query embedding from `Settings.embed_model.get_query_embedding(q)`
- `rules_one_hot` from `NL_RULES + NORMAL_RULES`
- SQL-template embedding from `Settings.embed_model.get_query_embedding(sql_template)`
- final query embedding:
  `q_embedding + rules_one_hot + t_embedding`

Observed live widths:

- `q_embedding` uses current `Settings.embed_model`, with configured `EMBED_DIM = 1536`
- `t_embedding` also uses current `Settings.embed_model`, width `1536`
- `rules_one_hot` width comes from:
  - `len(NL_RULES) = 30`
  - `len(NORMAL_RULES) = 37`
  - total `67`

Therefore:

- `1536 + 67 + 1536 = 3139`

This exactly matches the observed Chroma error.

## Whether The Existing Index Was Built With A Different Embedding Model Or Config

Yes, with qualification.

What clearly differs:

- the rule-vector width in the persisted index is `100`
- the rule-vector width in the failing runtime is `67`

What is not shown to differ:

- the summary embedding source length remains `1536`
- the SQL-template embedding source length remains `1536`

Inference:

- the dominant mismatch is a different retrieval-vector schema, not necessarily a different base embedding model width
- the persisted index was built under a different rule-vector configuration or different rule inventory than the failing runtime

Because the index is `/tmp`-scoped and not frozen, a stronger reproducibility conclusion should be:

- current `/tmp` substrate is not yet a deterministic, fully reproducible benchmark substrate

## Whether Code Already Has A `retrieval_vector_patch_applied` Path

Yes.

In [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:38151), the smoke runner accepts:

- `--align-rule-vector-dim <int>`

In [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:38400), if `align_rule_vector_dim > 0`:

- runtime is copied into `runtime_patch_v3`
- `rag/my_query_fusion_retriver.py` is patched
- `rules_one_hot` is padded or truncated to `target_rule_vector_dim`

Observed patch semantics:

- it does not change `EMBED_DIM`
- it changes only the rule-vector slice width

Observed prior successful exploratory artifact:

- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/smoke_result_v3.json](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/smoke_result_v3.json:1)
- `retrieval_vector_patch_applied = true`
- `retrieval_vector_expected_dim = 100`
- `generation_status = generation_success_with_output_sql`

## Whether Generated SQL Exists Despite Retrieval Failure

For the current failed canary attempt:

- no run-local v2 generated SQL file is present at `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v2.sql`
- [run_results.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json) records `generated_sql_copied = false`

For an older patched exploratory run:

- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql_v3.sql:1) exists
- this is not current benchmark evidence
- this should not be treated as output from the failed v2 canary

Conclusion:

- generated SQL exists historically in `/tmp`
- no generated SQL exists for the failed retrieval-mismatch attempt

## Whether Selected Rules / Retrieval Trace / Token Cost Artifacts Are Meaningful

Repo-local current canary artifacts under `reports/.../artifacts/` are not meaningful as current run evidence:

- [PERF_0006_selected_rules.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/artifacts/PERF_0006_selected_rules.json) says `available = false`
- [PERF_0006_retrieval_trace.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/artifacts/PERF_0006_retrieval_trace.json) says `available = false`
- [PERF_0006_token_cost_log.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/artifacts/PERF_0006_token_cost_log.json) contains only partial cost info and no valid current retrieval/output trace

Reason:

- the failed v2 run did not complete retrieval
- the repo-local artifact set is incomplete and not sufficient to interpret rule selection or retrieval behavior for the failed attempt

Historical `/tmp` v3 artifacts are meaningful only as exploratory smoke history:

- `selected_rules_v3.json`
- `retrieval_trace_v3.json`
- `token_cost_log_v3.json`

They are not current canary evidence and not leaderboard evidence.

## Fix Option Evaluation

### Option 1. Rebuild Chroma index with current embedding configuration

Assessment:

- technically coherent if the rebuild target is made explicit
- not safe to assume from current `/tmp` state alone

Risk:

- if rebuilt from the current visible runtime without a frozen contract, it produces a new exploratory substrate, not benchmark evidence

### Option 2. Force query embedding configuration to match existing Chroma index

Assessment:

- partially correct only if interpreted as matching the full retrieval-vector schema
- incorrect if interpreted as changing base embedding model only

Needed nuance:

- the mismatch is in the rule-vector slice width, not just the base embed model

### Option 3. Patch runtime config `EMBED_DIM` to discovered index dimension

Assessment:

- not correct

Reason:

- `EMBED_DIM` is the base embedding width `1536`
- setting `EMBED_DIM = 3172` would conflate total vector width with one segment width
- the visible successful exploratory patch does not change `EMBED_DIM`

### Option 4. Reject current `/tmp` substrate as not reproducible and require deterministic rebuild

Assessment:

- this is the conservative governance-safe fix for any future evidence-bearing path

Reason:

- current index is `/tmp`-only
- current index contract is not frozen
- current runtime and current index do not share a single explicit vector-schema contract

## Recommended Fix

Two-level recommendation:

1. For exploratory smoke only:
   use the already-existing `--align-rule-vector-dim 100` patch path, and label the outcome `exploratory_smoke_only_not_current_metric`.

2. For anything beyond exploratory smoke:
   reject the current `/tmp` substrate as non-reproducible and require an explicit deterministic rebuild or retained frozen index/runtime pair before rerun.

Conservative choice:

- do not patch `EMBED_DIM`
- do not silently reinterpret the failed v2 run
- do not promote any patched run to benchmark evidence

## Exact File / Config Candidates

Primary runtime/config candidates:

- [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py:38151)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/my_rewriter/config.py:7)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/my_query_fusion_retriver.py:103)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/rag_gen.py:96)

Index metadata candidates:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db/chroma.sqlite3`
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag/chroma_db/chroma.sqlite3`
- `/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/rag/chroma_db/chroma.sqlite3`

Build lineage candidates:

- [/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log](/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag_gen_build.log:1)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag_gen_build.log](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_root/rag_gen_build.log:1)
- [/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/rag_gen_build.log](/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/runtime_patch_v3/rag_gen_build.log:1)

## Rerun Recommendation

Rerun is recommended only after the patch target is explicit.

Meaning:

- exploratory rerun: only after explicitly choosing `align_rule_vector_dim = 100`
- evidence-bearing rerun: only after explicitly choosing a deterministic rebuild or frozen retained substrate path

Current status remains:

- `current_benchmark_metric_evidence = false`

