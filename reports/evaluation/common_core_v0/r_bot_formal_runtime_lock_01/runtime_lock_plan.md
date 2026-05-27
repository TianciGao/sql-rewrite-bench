## Runtime Lock Plan

Date: 2026-05-08

### Goal

Close the R-Bot runtime/dependency lock blocker with a retained, human-verifiable runtime package before any formal `@120` generation.

### Inputs

- [formal_gate_status_v11.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v11.md)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [smoke_env_package_snapshot.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/smoke_env_package_snapshot.txt)
- [r_bot_recovery_requirements.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/r_bot_recovery_requirements.txt)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)
- [r_bot_artifact_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md)

### Lock Decisions

1. Use the retained PG1 smoke package snapshot as the exact version source when present.
2. Preserve explicit dual driver coverage for:
   - `psycopg==3.3.4`
   - `psycopg-binary==3.3.4`
   - `psycopg2-binary==2.9.12`
3. Preserve the formal Chroma/index stack exactly as retained:
   - `chromadb==1.5.9`
   - `llama-index-core==0.14.21`
   - `llama-index==0.14.21`
   - `llama-index-vector-stores-chroma==0.5.5`
   - `llama-index-embeddings-openai==0.6.0`
   - `llama-index-embeddings-huggingface==0.7.0`
   - `llama-index-llms-openai==0.7.7`
   - `llama-index-llms-openai-like==0.7.2`
4. Preserve the retained numerical/runtime dependencies needed by the formal index and upstream runner:
   - `numpy==2.4.4`
   - `scipy==1.17.1`
   - `jpype1==1.7.0`
   - `jsonlines==4.0.0`
   - `openai==2.34.0`
   - `sqlglot==30.7.0`

### Human Verification Flow

1. Create or activate the intended formal runtime environment outside the repo bootstrap path.
2. Install from [r_bot_formal_requirements_lock.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt).
3. Run:

```bash
python reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py
```

4. Retain:
   - `runtime_environment_snapshot_v1.json`
   - `runtime_verify_report_v1.md`
5. Review whether the verifier passed and whether the remaining artifact-contract gate is still the only open blocker.

### What The Verifier Checks

- Python version and platform fields are captured
- required packages are importable
- required package versions match the formal lock
- distribution version verification is done separately from module import verification
- provider/base_url metadata fields are read from the retained index identifier without secrets
- formal Chroma index directory is visible
- retained index identifier exists
- retained index identifier reports:
  - `index_id = r_bot_formal_chroma_index_01`
  - `rule_vector_width = 100`
  - `total_dimension = 3172`
  - `embedding_model = text-embedding-3-small`

Explicit verifier import-target mappings include:

- `PyYAML -> yaml`
- `scikit-learn -> sklearn`
- `llama-index-instrumentation -> llama_index_instrumentation`
- `llama-index-workflows -> workflows`

### Non-Goals

- no package installation
- no database or SQL execution
- no R-Bot execution
- no formal generation authorization

### Expected Gate Effect

If human verification passes, the runtime/dependency lock blocker can be closed.

The overall formal gate still remains closed until retained run-path artifact-contract validation is closed separately.
