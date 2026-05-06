# SQLSOLVER_RUNNER_DRY_RUN_WITH_JAR_CONS_0007_0035_v1

## 0. Purpose And Boundary
State:
- no-execution runner dry-run with built jar
- support/verifier only
- not rewrite generation
- not speedup
- not leaderboard

## 1. Built Artifact
Report:
- jar path: `/tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar`
- jar exists: yes
- `Entry.class` present: yes
- companion Z3 artifacts: `lib/libz3.so`, `lib/libz3java.so`, `lib/z3-4.13.0.jar`
- no SQLSolver verification executed

## 2. Case Bundle Checks
For `CONS_0007`:
- adapter bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0007`
- positive pair files: present
- negative pair files: present
- schema file: present
- expected verdicts: present
- files found/missing: all required files found

For `CONS_0035`:
- adapter bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0035`
- positive pair files: present
- negative pair files: present
- schema file: present
- expected verdicts: present
- files found/missing: all required files found

## 3. Future Command Plan
For `CONS_0007`:
- positive command path: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0007/future_positive_command_NOT_RUN.txt`
- negative command path: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0007/future_negative_command_NOT_RUN.txt`
- output verdict paths: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0007/positive_verdicts_NOT_RUN.txt`, `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0007/negative_verdicts_NOT_RUN.txt`
- timeout policy: wall timeout `60s` per pair, `sqlsolver.z3.timeout = 10000 ms`
- NOT RUN status: recorded

For `CONS_0035`:
- positive command path: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0035/future_positive_command_NOT_RUN.txt`
- negative command path: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0035/future_negative_command_NOT_RUN.txt`
- output verdict paths: `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0035/positive_verdicts_NOT_RUN.txt`, `/tmp/rewritebench_sqlsolver_runner_dry_run/CONS_0035/negative_verdicts_NOT_RUN.txt`
- timeout policy: wall timeout `60s` per pair, `sqlsolver.z3.timeout = 10000 ms`
- NOT RUN status: recorded

## 4. Dry-run Result
For `CONS_0007`:
- can_execute_support_smoke_next: `true`
- blockers: none

For `CONS_0035`:
- can_execute_support_smoke_next: `true`
- blockers: none

## 5. Verdict Mapping / Metrics
Report:
- `EQ -> proved_equivalent`
- `NEQ -> refuted_equivalence`
- `TIMEOUT -> timeout`
- `UNKNOWN -> unknown_or_unsupported`
- support-only metrics:
  - `prove_count`
  - `refute_count`
  - `unknown_count`
  - `timeout_count`
  - `unsupported_count`
  - `parser_or_translation_failure_count`
  - `internal_error_count`
  - `verifier_support_rate`
- no speedup / no WTL / no leaderboard

## 6. Recommended Next Step
Choose exactly one:
- `execute bounded SQLSolver support smoke for CONS_0007 / CONS_0035`

## 7. Non-Modification Note
Confirm no execution/build/install/DB/checker/speedup and no case/registry/review/rules/EXECUTION_STATUS changes.
