# LEARNEDREWRITE_LLM4REWRITE_JVM_JAR_PREFLIGHT_v1

## 0. Purpose And Boundary

This is a Java/JVM/JAR preflight only for embedded `LearnedRewrite` via upstream `LLM4Rewrite`.

It is not LearnedRewrite execution.
It is not database execution.
It is not checker execution.
It is not speedup evaluation.

No `LearnedRewriter.learnedRewrite(...)` method was invoked in this preflight.

## 1. Runtime Inputs

- jar path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
- runner path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_learned_rewrite.py`
- Java source path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/learned/LearnedRewriter.java`
- venv path:
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- case context:
  - `PERF_0006`

## 2. Java Visibility

- `java` visible: yes
- `java` path:
  - `/usr/bin/java`
- `java -version` status: success
- detected version:
  - `openjdk version "17.0.18" 2026-01-20`
- `jar tf` status: success
- jar entry count:
  - `24247`
- important classes found:
  - `rewriter/DBConn.class`
  - `rewriter/SqlIo.class`
  - `learned/Rewriter.class`
  - `learned/LearnedRewriter.class`
  - `learned/Node.class`

## 3. JPype / JVM Probe

- `jpype` import success: yes
- `jpype` version:
  - `1.7.0`
- JVM start attempted: yes
- JVM start status: success
- class load status: failed
- JVM shutdown status: success
- class-load failure:
  - `java.lang.SecurityException: Invalid signature file digest for Manifest main attributes`
- no LearnedRewrite method invoked: yes

Interpretation:

- the JVM itself is visible and startable
- the jar is structurally present and listable
- the blocking failure happens at class loading because the jar signature metadata is invalid for the current runtime path

## 4. Readiness Decision

- `jvm_jar_preflight_blocked_with_exact_reason`

Exact blocker:

- JPype class loading of embedded `LearnedRewrite.jar` fails with:
  - `java.lang.SecurityException: Invalid signature file digest for Manifest main attributes`

## 5. Remaining Blockers Before LearnedRewrite Smoke

- jar signature / class-load blocker
- single_case_execution_not_implemented
- output_sql_extraction_not_tested
- checker_handoff_not_run

## 6. Recommended Next Step

- `fix JVM/JAR blocker`

Reason:

- Java visibility is already confirmed
- the current hard blocker is the signed-jar class-load failure
- no case-level smoke should be attempted until that is resolved

## 7. Non-Modification Note

No LearnedRewrite execution occurred.
No DB connection occurred.
No checker ran.
No speedup ran.
No model/API call occurred.
No SQLGlot route ran.
No case, registry, review, rules, or `docs/EXECUTION_STATUS.md` files were modified.
