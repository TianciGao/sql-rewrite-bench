# LLMR2_RUNTIME_FAILURE_AUDIT_PERF_0006_v1

## 0. Purpose And Boundary
This is a read-only runtime failure audit for the bounded `PERF_0006` LLM-R2 smoke.

No rerun occurred. No OpenAI/API call occurred in this audit. No Java rule applier ran in this audit. No DB, checker, or speedup step ran.

## 1. Smoke Result Recap
Committed smoke result:
- `dry_run_passed`: `true`
- `method_executed`: `true`
- `openai_api_used`: `false`
- `java_rule_applier_used`: `true`
- `generation_status`: `method_execution_failed`
- `output_sql_extracted`: `false`
- `checker_status`: `not_run`
- `speedup_status`: `not_run`
- `failure_category`: `runtime_timeout_before_prompt_api_phase`

Claim boundary:
- `bounded_1_case_LLMR2_smoke_attempt_not_leaderboard`

## 2. Artifact Inspection
- smoke result path:
  `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/smoke_result_v1.json`
- expected result CSV path:
  `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/gpt_rewritebench_perf_0006_one_promo_queryCL_updated.csv`
- result CSV exists: no
- generated SQL exists: no
- token/cost log exists: yes, but it explicitly says prompt/completion usage was not reached
- prompt/API marker appears: no
- OpenAI call evidence: no
- HuggingFace / sentence-transformer load evidence: yes
  - stderr shows unauthenticated HF Hub access warning
  - stderr shows `Loading weights` progress twice
- Java import-time side-effect output appears: yes
  - stdout contains the example SQL printed by upstream `rewriter.py`
  - this is not a bounded `PERF_0006` candidate artifact

## 3. Wrapper Path Analysis
The wrapper in [scripts/cli.py](/home/tianci_gao/code/sql-rewrite-bench/scripts/cli.py) does the following:
- copies the upstream repo to `/tmp/rewritebench_llmr2_single_case_runner/PERF_0006/runtime_root_v1`
- patches `LLM_R2.py` to switch the terminal dataset literal from `dsb` to `rewritebench_perf_0006`
- stages:
  - `queries_rewritebench_perf_0006_test.csv`
  - `rewritebench_perf_0006.json`
  - `pos_pool_rewritebench_perf_0006_updated.csv`
  - `neg_pool_rewritebench_perf_0006_updated.csv`
- sets marker env vars for:
  - OpenAI prompt/API use
  - Java rule applier use
  - token log path
  - prompt trace path
- runs:
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python LLM_R2.py`
  - cwd: `runtime_root_v1/src`

Important wrapper properties:
- there is no explicit timeout in the subprocess call
- output capture expects a final result CSV under `runtime_root_v1/results/`
- the wrapper does not bypass upstream pool preprocessing

## 4. Upstream Runtime Path Analysis
Upstream `LLM_R2.py` behavior is the decisive point:
- it loads `SentenceTransformer('all-MiniLM-L6-v2')` at module import time
- it loads a `QueryformerForCL` checkpoint at module import time
- `LLM_R2(dataset, method, num_promos)` then loads:
  - `../data/data_llmr2/queries/queries_<dataset>_test.csv`
  - `../data/data_llmr2/pools/pos_pool_<dataset>_updated.csv`
  - `../data/data_llmr2/pools/neg_pool_<dataset>_updated.csv`
- for `method='queryCL'`, `get_pool(...)` calls `batcher(...)`
- `batcher(...)` calls `prepare_enc_data(...)`
- `prepare_enc_data(...)` calls `get_physical_tree(...)` for each pool query
- `get_physical_tree(...)` shells out through Java before any prompt/API dispatch

This means:
- the one-row adapter query CSV is used for `df_test`
- but upstream still preprocesses the full positive and negative demo pools first
- prompt/API dispatch only happens later, inside the per-test-row loop, after demo-pool embedding and retrieval setup
- therefore the bounded one-row adapter does not create a truly bounded one-row runtime path

Hardcoded / path-coupled upstream behaviors:
- dataset naming controls all three data paths
- result CSV is only written at the end of the loop or every 500 rows
- no early single-row fast path exists upstream

## 5. Diagnosis
Primary diagnosis:
- `prompt_api_not_reached_due_preprocessing`

Why this is the best fit:
- the wrapper did stage the one-row adapter file into the exact path upstream reads
- no result CSV was produced
- no prompt/API marker was produced
- stderr shows model loading progressed
- upstream still performs full pool preprocessing and queryCL embedding setup before first prompt dispatch

Secondary contributing note:
- `java_import_side_effect_noise` is real but not primary
- it explains the misleading stdout SQL line, not the missing prompt/API phase

## 6. Recommended Next Step
- `implement bounded one-row fast path wrapper`

Reason:
- increasing timeout alone is not the right first move because the current path still front-loads full-pool preprocessing
- the least invasive useful next step is to build a truly bounded path that:
  - loads only the staged one-row test query
  - loads a deliberately tiny demo pool slice
  - reaches prompt/API dispatch before expensive whole-pool setup dominates runtime

## 7. Non-Modification Note
No rerun, model/API call, Java invocation, DB access, checker, or speedup occurred in this audit.

No repo state was changed except this scratch report.
