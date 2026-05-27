# SQLSOLVER_TMP_BUILD_AUDIT_v1

## 0. Purpose And Boundary
State:
- build-only audit
- support/verifier only
- no SQLSolver verification execution
- no DB/checker/speedup
- no leaderboard

## 1. Preconditions
Report:
- repo path: `/tmp/rewritebench_sqlsolver_audit/candidate`
- commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- Java version: `openjdk 17.0.18`
- Gradle wrapper exists: yes
- Z3 artifacts visible: yes
- prebuilt jar previously absent: yes

## 2. Build Attempt
Report:
- command(s) run:
  - initial wrapper attempt without redirected Gradle home
  - retry with `GRADLE_USER_HOME=/tmp/rewritebench_sqlsolver_gradle_home ./gradlew fatjar`
- build status: success
- stdout log path: `/tmp/rewritebench_sqlsolver_build_stdout_v1.log`
- stderr log path: `/tmp/rewritebench_sqlsolver_build_stderr_v1.log`
- failure summary before success: first attempt failed because the wrapper tried to create its lock under the default home path; second attempt succeeded after pinning `GRADLE_USER_HOME` into `/tmp`

## 3. Artifact Verification
If jar exists:
- jar path: `/tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar`
- jar size: `45M`
- `Entry.class` present: yes
- required classes present: yes
- companion libs present: yes
- runnable command shape for future dry-run update, marked NOT RUN:
  - `java -cp /tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar sqlsolver.api.Entry ...`

## 4. Classification
`build_success_runner_dry_run_update_ready`

## 5. Recommended Next Step
Choose exactly one:
- `update SQLSolver runner dry-run with built jar`

## 6. Non-Modification Note
Confirm:
- no SQLSolver verification run
- no DB/checker/speedup
- no case/registry/review/rules/EXECUTION_STATUS changes
