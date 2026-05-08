## Runtime Lock Expected Artifacts

Date: 2026-05-08

### Package Inputs

- [r_bot_formal_requirements_lock.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt)
- [runtime_environment_snapshot_schema.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_schema.json)
- [run_manual_r_bot_formal_runtime_verify.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)

### Human-Run Outputs

The human verification step should write:

1. `runtime_environment_snapshot_v1.json`
2. `runtime_verify_report_v1.md`

Both outputs are expected under:

- `reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/`

### Required Snapshot Facts

The retained snapshot must include:

- Python version
- Python executable path
- platform fields
- requirements lock path
- requirements lock SHA-256
- provider/base_url metadata without secrets
- formal index identifier path
- formal index id
- formal index directory path
- formal index directory visibility boolean
- retained `rule_vector_width`
- retained `total_dimension`
- per-package import/version checks
  - with distribution version checks separated from import-target checks
- final verifier status
- explicit `current_benchmark_gate_ready = false`
- explicit `formal_generation_may_start = false`

### Success Interpretation

Success means:

- required packages import successfully
- required package versions match the formal lock
- formal Chroma index directory is visible
- retained formal index identifier exists
- retained formal index identifier reports:
  - `index_id = r_bot_formal_chroma_index_01`
  - `total_dimension = 3172`
  - `rule_vector_width = 100`

### Gate Boundary

Even after a successful runtime verification:

- formal `R-Bot @120` generation still may not start until the retained run-path artifact-contract gate is closed separately
