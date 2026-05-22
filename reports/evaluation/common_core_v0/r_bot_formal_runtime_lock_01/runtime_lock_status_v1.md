# Runtime Lock Status v1

## Scope

This document records the runtime/dependency lock status for the formal R-Bot
runtime package after the successful human-run runtime verifier.

It incorporates:

- [runtime_environment_snapshot_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json)
- [runtime_verify_report_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_verify_report_v1.md)
- [r_bot_formal_requirements_lock.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt)
- [formal_gate_status_v11.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/formal_gate_status_v11.md)
- [formal_chroma_index_identifier_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json)
- [r_bot_parameter_freeze_v2.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json)

It remains a status document only.
It does not authorize generation.

## Direct Answers

- runtime verification passed: `yes`
- required package versions pinned: `yes`
- required package versions importable: `yes`
- Python metadata captured: `yes`
- platform metadata captured: `yes`
- provider/base_url metadata recorded without secrets: `yes`
- formal Chroma index visible: `yes`
- retained index identifier reports `index_id = r_bot_formal_chroma_index_01`: `yes`
- retained index identifier reports `rule_vector_width = 100`: `yes`
- retained index identifier reports `total_dimension = 3172`: `yes`
- runtime/dependency lock blocker closed: `yes`
- `current_benchmark_gate_ready`: `false`
- formal `R-Bot @120` generation may start: `no`

## Evidence Summary

### Verifier Result

The retained verifier report records:

- status: `runtime_verify_passed_gate_still_closed`
- package checks: `53`
- package failures: `0`
- Python executable:
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python`
- Python version:
  - `3.12.3`
- platform:
  - `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39`

### Package Lock

The retained requirements lock is fully pinned with `==` versions and the
runtime snapshot shows no package-version mismatches and no import failures.

### Provider Metadata

The retained runtime snapshot records provider metadata without secrets:

- provider family: `api.gptsapi.net`
- provider name: `api.gptsapi.net`
- base_url field present but non-secret-bearing
- `secrets_present = false`

### Formal Index Visibility

The retained runtime snapshot confirms:

- index identifier path exists
- index directory is visible:
  - `/tmp/rewritebench_rbot_formal_chroma_index_01`
- retained index identifier reports:
  - `index_id = r_bot_formal_chroma_index_01`
  - `rule_vector_width = 100`
  - `total_dimension = 3172`

## What Closed In v1

Closed by this package:

1. the runtime/dependency lock blocker is now closed
2. a retained formal runtime requirements lock now exists
3. a retained environment snapshot with Python/platform metadata now exists
4. required package import and version checks passed against the retained lock
5. the formal Chroma index visibility and dimension checks passed inside the retained runtime verifier

## What Remains Blocked

The overall formal gate does not open in this package.

Remaining blockers:

1. retained run-path artifact-contract validation remains open
2. denominator-aware formal run evidence has not yet been retained
3. generation-side runtime attestation remains incomplete until a formal denominator-aware run satisfies the retained artifact contract

These remain sufficient to keep:

- `current_benchmark_gate_ready = false`
- formal `R-Bot @120` generation may start: `no`

## Bottom Line

The runtime/dependency lock blocker is closed.

Formal `R-Bot @120` generation still may not start because retained run-path
artifact-contract validation and denominator-aware formal run evidence remain
open.
