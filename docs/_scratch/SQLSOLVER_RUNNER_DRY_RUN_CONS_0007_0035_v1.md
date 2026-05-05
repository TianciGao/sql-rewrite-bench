# SQLSOLVER_RUNNER_DRY_RUN_CONS_0007_0035_v1

## 0. Purpose And Boundary
State:
- no-execution runner dry-run
- support/verifier only
- not rewrite generation
- not speedup
- not leaderboard

## 1. SQLSolver Runtime Inputs Checked
Report:
- repo path: `/tmp/rewritebench_sqlsolver_audit/candidate`
- entrypoint source: present at `api/src/main/java/sqlsolver/api/Entry.java`
- build files: `build.gradle` present
- gradlew: present
- lib/z3 artifacts: `lib/libz3.so`, `lib/libz3java.so`, `lib/z3-4.13.0.jar` present
- built jar exists: no
- `sqlsolver.properties` timeout: `sqlsolver.z3.timeout = 10000`

## 2. Case Bundle Checks
For `CONS_0007`:
- adapter bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0007`
- positive pair files: present
- negative pair files: present
- schema file: present
- expected verdicts: present
- files found/missing: all required bundle files found

For `CONS_0035`:
- adapter bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0035`
- positive pair files: present
- negative pair files: present
- schema file: present
- expected verdicts: present
- files found/missing: all required bundle files found

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
- can_execute_support_smoke_next: `false`
- blockers:
  - `build_artifact_missing_but_source_build_contract_visible`

For `CONS_0035`:
- can_execute_support_smoke_next: `false`
- blockers:
  - `build_artifact_missing_but_source_build_contract_visible`

## 5. Verdict Mapping / Metrics
Report:
- verdict mapping:
  - `EQ -> proved_equivalent`
  - `NEQ -> refuted_equivalence`
  - `TIMEOUT -> timeout`
  - `UNKNOWN -> unknown_or_unsupported`
  - wrapper parse/launch failures must map to `parser_or_translation_failure` or `internal_error`
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
- `locate prebuilt SQLSolver jar`

## 7. Non-Modification Note
Confirm no execution/build/install/DB/checker/speedup and no case/registry/review/rules/EXECUTION_STATUS changes.
