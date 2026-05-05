# LLMR2_EXTERNAL_REPO_SUBSTRATE_AUDIT_v1

## 0. Purpose And Boundary
This note is an external repo substrate audit only for `LLM-R2`. It does not execute the method, does not call any model/API, does not run any database, does not install packages, does not implement an adapter, and is not leaderboard evidence.

## 1. Acquisition Result
- URL: `https://github.com/DAMO-NLP-SG/LLM-R2`
- `git ls-remote` status: success
- clone method attempted: `git clone --depth 1`
- clone success: yes
- local `/tmp` path: `/tmp/rewritebench_llmr2_audit/LLM-R2`
- default branch: `main`
- commit hash: `91ba530b45b1353d6d2cc45d816dfefc34dbad92`
- failure details: previous clone failure did not recur on this retry

## 2. Repository Inventory
- `README.md`: present
- root `LICENSE`: not present
- requirements/environment files:
  - `requirements.txt`
- main directories:
  - `data/data_llmr2/`
  - `src/`
  - `src/calcite_core_main_jar/`
  - `src/simcse_models/`
  - `src/rules_for_selected/`
  - `src/src/`
- runnable scripts / entrypoints found:
  - `src/LLM_R2.py`
  - `src/LLM_baseline_rewriter.py`
  - `src/learned_rewriter_pg.py`
  - `src/run_CLTrain.sh`
  - `src/run_postgre.py`
  - `src/run_sql_time_pg.py`
  - `src/evaluation_cl.py`
  - `src/train.py`
- configs / data / rule / checkpoint artifacts:
  - demo pools present under `data/data_llmr2/pools/`
  - test/train queries present under `data/data_llmr2/queries/`
  - schema JSON files present under `data/data_llmr2/schemas/`
  - rule files present under `src/rules_for_selected/`
  - Java rewrite artifacts present as `src/rewriter_java.jar` and `src/src/rule_rewriter.java`
  - Calcite/JVM dependency jars are vendored under `src/calcite_core_main_jar/`
  - local contrastive selector checkpoint present at `src/simcse_models/tpch/pytorch_model.bin`

## 3. Method Contract Inferred
- expected input format:
  - dataset-scoped CSV inputs such as `queries_tpch_test.csv`, `queries_job_syn_test.csv`, `queries_dsb_test.csv`
  - per-query fields include `db_id` and `original_sql`
  - per-dataset schema JSON files under `data/data_llmr2/schemas/`
  - positive and negative demonstration pools under `data/data_llmr2/pools/`
- expected output format:
  - `LLM_R2.py` writes results CSV files under `../results/`, including `rewritten_sql_gpt`, `activated_rules_gpt`, and prompt-demo trace fields
  - `learned_rewriter_pg.py` builds `rewritten_queries` and `activated_rules` arrays and is set up to emit CSVs, though the final write lines are commented in the checked-in file
- `output_sql` visible: yes
  - `LLM_R2.py` materializes candidate SQL in the `rewritten_sql_gpt` column
  - `learned_rewriter_pg.py` returns `rewrite_query` from `call_rewriter(...)`
- demo selection path:
  - `LLM_R2.py` loads pools from `../data/data_llmr2/pools/`
  - selector methods include `plan`, `sentbert`, and `queryCL`
- rule selection/path:
  - `LLM_R2.py` uses an OpenAI chat call to select rewrite rules
  - selected rules are filtered against a hardcoded Calcite-style rule allowlist
- rule application path:
  - selected rules are applied by `rewriter.py`
  - `rewriter.py` shells into `java -cp rewriter_java.jar src/rule_rewriter.java`
- model / embedding / contrastive components:
  - OpenAI client in `src/LLM_R2.py`
  - `SentenceTransformer('all-MiniLM-L6-v2')`
  - `QueryformerForCL` plus checkpoint load from `src/simcse_models/<model_name>/pytorch_model.bin`
- DB / execution feedback requirement:
  - not required on the main generation path in `LLM_R2.py`
  - repo-local evaluation scripts use PostgreSQL runtime measurement via `src/run_postgre.py`
  - `run_postgre.py` also embeds hardcoded localhost/postgres credentials, which is an adapter concern
- benchmark / dataset assumptions:
  - built around repo-packaged `tpch`, `job_syn`, and `dsb` query/schema/pool assets
  - schema contract is JSON metadata, not raw DDL

## 4. RewriteBench Mapping Feasibility
Mapping a RewriteBench case such as `PERF_0006` looks plausible but incomplete:
- source SQL: yes, a case query can map into the `original_sql` field
- schema / DDL: partial, because LLM-R2 expects compact schema JSON with table/column/row metadata rather than `ddl_pg.sql`
- witness data: not part of the LLM-R2 generation contract, but still compatible with later RewriteBench checker handoff
- dialect: PostgreSQL mapping is plausible because the rewrite stack includes PostgreSQL-oriented normalization and Calcite-to-PostgreSQL SQL emission
- output candidate SQL: yes, candidate SQL is visible in result CSV fields or returned rewrite strings
- checker handoff: yes, RewriteBench could hand the extracted candidate into its existing PostgreSQL checker after adapter work

Current conclusion:
- a RewriteBench case package can probably be mapped into the LLM-R2 contract
- but it will need adapter translation for schema JSON, dataset naming, pool/demo expectations, output capture, and API/model wiring

## 5. Blockers Before Any Smoke
- no acquisition blocker remains
- dependency contract is only partially explicit:
  - `requirements.txt` says `openai`, `sentence_transformers`, `transformers`, `torch`, `psycopg2-binary`, `gradio`, and others
- model/checkpoint blocker:
  - a local `tpch` contrastive checkpoint exists, but the repository does not clearly explain whether equivalent checkpoints are expected for `job_syn` or `dsb`
- dataset/demo blocker:
  - the method expects its own pool CSVs and dataset-specific schema JSON files
  - RewriteBench does not natively provide those in LLM-R2 format
- output capture blocker:
  - output SQL path is visible, but there is no RewriteBench adapter yet to capture it into bounded single-case artifacts
- API/model policy blocker:
  - `LLM_R2.py` requires OpenAI on the main rule-selection path
- DB/runtime blocker:
  - generation itself does not require DB execution, but repo-local evaluation scripts do
- license/redistribution blocker:
  - no root repository `LICENSE` file was found, so redistribution/use terms should be treated as unresolved until clarified

## 6. Classification
`external_substrate_found_but_contract_unclear`

Justification:
- the official repo is now acquired and inspectable under `/tmp`
- the method substrate is real and includes data pools, rule assets, Java rewrite machinery, and a contrastive selector checkpoint
- however, the exact adapter contract for a single RewriteBench case is still unclear because the repo assumes its own dataset CSV/schema/pool layout, an OpenAI-backed rule selector, and result CSV output conventions rather than a direct one-case command

## 7. Recommended Next Step
`implement no-execution adapter preflight for PERF_0006`

Reason:
- acquisition is no longer blocked
- the next unknown is the single-case contract mapping, not repository availability
- a no-execution preflight can answer schema translation, prompt/demo stub, output capture, and artifact layout questions without running the method

## 8. Non-Modification Note
No LLM-R2 execution occurred. No model/API call was made. No database was run. No package install occurred. No scripts, cases, registries, review files, rules, or `docs/EXECUTION_STATUS.md` were changed. The long-standing taxonomy notes were untouched.
