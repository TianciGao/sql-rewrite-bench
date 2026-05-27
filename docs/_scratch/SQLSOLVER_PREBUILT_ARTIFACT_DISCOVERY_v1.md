# SQLSOLVER_PREBUILT_ARTIFACT_DISCOVERY_v1

## 0. Purpose And Boundary
State artifact discovery only, no build, no run.

## 1. Prior Dry-run Recap
The prior SQLSolver runner dry-run stopped at one blocker:
- `build_artifact_missing_but_source_build_contract_visible`

The repo clone, entrypoint source, `gradlew`, and bundled Z3 artifacts were already visible, but no built runnable jar was present.

## 2. Local Repo Artifact Search
Searched paths:
- `/tmp/rewritebench_sqlsolver_audit/candidate/build/`
- `/tmp/rewritebench_sqlsolver_audit/candidate/api/build/`
- `/tmp/rewritebench_sqlsolver_audit/candidate/lib/`
- `/tmp/rewritebench_sqlsolver_audit/candidate/gradle/wrapper/`
- directories matching `build|dist|release|libs|target|out`

Found local jar/zip artifacts:
- `/tmp/rewritebench_sqlsolver_audit/candidate/gradle/wrapper/gradle-wrapper.jar`
- `/tmp/rewritebench_sqlsolver_audit/candidate/lib/antlr-4.8-complete.jar`
- `/tmp/rewritebench_sqlsolver_audit/candidate/lib/z3-4.13.0.jar`

Not found:
- no `build/libs/sqlsolver*.jar`
- no release/dist zip
- no packaged runnable SQLSolver distribution artifact

## 3. GitHub Release / Distribution Search
Checked GitHub release metadata for `SJTU-IPADS/SQLSolver`.

Result:
- release API returned an empty list
- no published GitHub release asset was visible from this audit

README distribution status:
- README documents how to compile and build a jar locally with `gradle fatjar`
- README does not document a hosted downloadable runnable jar or distribution package

## 4. Artifact Contract
No prebuilt artifact found.

Observed contract:
- intended runnable artifact is a locally built jar in `build/libs/`
- entrypoint is defined in `build.gradle` as `sqlsolver.api.Entry`
- companion native libraries are still required:
  - `lib/libz3.so`
  - `lib/libz3java.so`
  - `lib/z3-4.13.0.jar`

Dry-run update feasibility:
- no, not without either a prebuilt runnable jar or an approved build step

## 5. Classification
`no_prebuilt_artifact_build_required`

Justification:
- local checkout contains source and support jars only
- no runnable SQLSolver jar exists in the clone
- GitHub releases are empty
- README expects local build output rather than a downloadable binary

## 6. Recommended Next Step
Choose exactly one:
- `build SQLSolver in /tmp`

## 7. Non-Modification Note
Confirm no execution/build/install/DB/checker/speedup and no repo/case/registry changes.
