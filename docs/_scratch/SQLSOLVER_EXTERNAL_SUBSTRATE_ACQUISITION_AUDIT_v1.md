# SQLSOLVER_EXTERNAL_SUBSTRATE_ACQUISITION_AUDIT_v1

## 0. Purpose And Boundary
This is a SQLSolver acquisition and substrate audit only.

It is support/verifier only, not rewrite generation, not speedup, not leaderboard evidence, and not execution.

## 1. Local Evidence Recap
Current repo-local SQLSolver state remains:
- support-only
- not integrated
- no repo-local runnable wrapper
- no known repo-local SQLSolver checkout before this audit
- no current RewriteBench machine-readable verdict path

Existing local evidence consistently said:
- SQLSolver is a verifier/support line, not a rewrite leaderboard line
- no local runner or wrapper exists
- no local solver/dependency stack was previously staged in the repo

Key local evidence:
- [docs/_scratch/SQLSOLVER_MANUAL_ACQUISITION_CHECKLIST_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/SQLSOLVER_MANUAL_ACQUISITION_CHECKLIST_v1.md)
- [docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md)
- [docs/_scratch/PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_RUNNABLE_SUBSTRATE_AUDIT_v1.md)
- [reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json)

## 2. External Acquisition Search
Search terms used:
- `"SQLSolver" SQL equivalence`
- `"SQL Solver" SQL equivalence`
- `"SQLSolver" database`
- `"SQLSolver" "query" "equivalence"`
- `"SQLSolver" "Z3" SQL`
- `"SQLSolver" "CVC" SQL`
- `"SQLSolver" GitHub SQL`
- `SQLSolver query equivalence GitHub`

Candidate URLs found:
- `https://github.com/SJTU-IPADS/SQLSolver`
- `https://github.com/WeTune/SQLSolver-code`

Candidate assessment:
- `SJTU-IPADS/SQLSolver`
  - plausible and confirmed
  - GitHub description: `An automated prover that verifies the equivalence of SQL queries`
  - `git ls-remote` succeeded
  - shallow clone succeeded
  - cloned commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- `WeTune/SQLSolver-code`
  - not the main target
  - GitHub description states the project moved to `SJTU-IPADS/SQLSolver`

Clone status:
- clone attempted: yes
- clone success: yes
- local candidate path: `/tmp/rewritebench_sqlsolver_audit/candidate`

## 3. Candidate Substrate Inventory
Recovered public substrate signals from `SJTU-IPADS/SQLSolver`:

README:
- present
- documents purpose, requirements, build, JAR usage, Java API, benchmarks, and repository layout

LICENSE:
- present
- Apache License 2.0

Requirements/build files:
- root `build.gradle`
- `settings.gradle`
- `gradle.properties`
- `gradlew`
- Gradle wrapper files
- subproject `build.gradle` files under `api/`, `common/`, and `sql/`

Solver dependencies:
- documented in README: `z3 4.8.9`, `antlr 4.8`, `Python 3`, `Java 17`, `Gradle 7.3.3`
- bundled artifacts visible in `lib/`:
  - `libz3.so`
  - `libz3java.so`
  - `z3-4.13.0.jar`
  - `antlr-4.8-complete.jar`

Scripts/entrypoints:
- JAR main class declared in `build.gradle`: `sqlsolver.api.Entry`
- Java API entry documented in README and source: `sqlsolver.api.entry.Verification`
- CLI contract visible in [Entry.java](</tmp/rewritebench_sqlsolver_audit/candidate/api/src/main/java/sqlsolver/api/Entry.java>)

Examples:
- README includes a file-based example with:
  - `-sql1=<path/to/query1>`
  - `-sql2=<path/to/query2>`
  - `-schema=<path/to/schema>`
  - optional `-print`
  - optional `-output=<path/to/output>`

Supported SQL subset docs:
- explicit full support matrix not found
- README says queries must satisfy Calcite parser syntax
- code evidence shows at least partial support signals for:
  - aggregates
  - `EXISTS`
  - correlated variables/subqueries
  - `NULL` semantics
  - arithmetic
  - `DATE`, `TIMESTAMP`, and `INTERVAL`
- support boundaries are still incomplete because the public user-facing contract collapses unsupported features and syntax errors into `UNKNOWN`

Input format:
- yes, SQL query pairs directly
- two SQL files with one SQL statement per line
- corresponding lines are paired
- separate schema file required

Schema / constraint contract:
- schema DDL is required
- code evidence shows support signals for:
  - `PRIMARY KEY`
  - `FOREIGN KEY`
  - `UNIQUE`
  - `NOT NULL`
- `CHECK` constraint support was not confirmed from the public contract in this audit

Output / verdict format:
- README and enum show four result values:
  - `EQ`
  - `NEQ`
  - `UNKNOWN`
  - `TIMEOUT`
- CLI can write line-oriented results to a file via `-output=<path>`
- this is machine-readable enough for a bounded support table
- however it does not distinguish:
  - unsupported SQL
  - parser or translation failure
  - internal error
  - all of these may collapse into `UNKNOWN`

Timeout/config policy:
- API exposes timeout overloads
- README notes timeouts may still overrun due to external libraries like Z3
- `sqlsolver.properties` exposes `sqlsolver.z3.timeout = 10000`

## 4. RewriteBench Mapping Feasibility
For a future bounded `CONS` support smoke:

Source-positive query pair mapping:
- feasible in principle by writing the positive pair as aligned lines in `sql1` and `sql2`

Source-negative query pair mapping:
- also feasible in principle with the same aligned-line contract

Schema / constraint mapping:
- feasible only if RewriteBench can export not just table DDL but the constraint subset SQLSolver relies on
- `PRIMARY`, `FOREIGN`, `UNIQUE`, and `NOT NULL` appear relevant

Constraint bridge policy:
- still needed
- RewriteBench must decide what to do when a case package has weaker, missing, or non-DDL-manifested constraints than SQLSolver expects

Timeout policy:
- still needed
- SQLSolver has a Z3 timeout knob, but RewriteBench needs a bounded support-smoke timeout contract

Unsupported-feature policy:
- still needed
- SQLSolver’s public verdict surface does not separate unsupported SQL from parser failure or generic unknown

Machine-readable verdict mapping:
- possible
- suggested mapping:
  - `EQ` -> `proved_equivalent`
  - `NEQ` -> `refuted_equivalence`
  - `TIMEOUT` -> `timeout`
  - `UNKNOWN` -> coarse `unknown_or_unsupported`
- a finer RewriteBench split would require wrapper-side diagnostics

Support table output mapping:
- feasible after wrapper work
- but still support-only, never rewrite leaderboard or speedup

Best first bounded support candidates:
- `CONS_0007`
- `CONS_0035`

## 5. Support Metrics
Future support-only metrics should include:
- `prove_count`
- `refute_count`
- `unknown_count`
- `timeout_count`
- `unsupported_count`
- `parser_or_translation_failure_count`
- `internal_error_count`
- `verifier_support_rate`

Explicitly out of scope:
- no `GM_Speedup`
- no `W/T/L`
- no `RegressionRate@20`
- no rewrite leaderboard

## 6. Classification
`acquired_but_wrapper_needed`

Justification:
- a public upstream repo was found and cloned
- runnable entrypoint, build contract, solver dependencies, schema input, and line-oriented verdict output are all visible
- but RewriteBench still lacks:
  - a local wrapper
  - a timeout contract
  - a constraint-bridge policy
  - a verdict mapping policy that separates `UNKNOWN` from unsupported/parser/internal categories

## 7. Recommended Next Step
`implement no-execution SQLSolver adapter preflight for CONS_0007 / CONS_0035`

Reason:
- upstream acquisition is now strong enough to justify a repo-local preflight
- `CONS_0007` is already the best bounded support candidate in prior readiness notes
- `CONS_0035` already has support-line history nearby through VeriEQL, so it is a useful contrast case
- this remains support-only and avoids premature execution

## 8. Non-Modification Note
This audit did not execute SQLSolver or any cloned code.

Confirmed:
- no execution
- no model/API
- no DB
- no package install
- no checker
- no speedup
- no registry/review/rules/`docs/EXECUTION_STATUS.md`/case changes
