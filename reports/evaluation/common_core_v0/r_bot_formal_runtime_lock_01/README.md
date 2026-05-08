# R-Bot Formal Runtime Lock 01

This package freezes the formal runtime/dependency lock needed after the
successful formal Chroma index build and inspect.

## Files

- [runtime_lock_plan.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_lock_plan.md)
- [r_bot_formal_requirements_lock.txt](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt)
- [runtime_environment_snapshot_schema.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_schema.json)
- [run_manual_r_bot_formal_runtime_verify.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py)
- [runtime_lock_expected_artifacts.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_lock_expected_artifacts.md)

## Role

This package does not install dependencies and does not run R-Bot.

It provides:

- a pinned formal runtime lock
- a schema for the retained runtime snapshot
- a human-run verifier that checks imports, versions, and retained formal index visibility

## Human Use

Run:

```bash
python reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py
```

Expected retained outputs:

- `runtime_environment_snapshot_v1.json`
- `runtime_verify_report_v1.md`

## Gate Boundary

This package is intended to close the runtime/dependency lock blocker only after
successful human verification.

It does not by itself open the formal `R-Bot @120` generation gate. The
retained run-path artifact-contract blocker still needs to close separately.
