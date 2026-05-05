# LEARNEDREWRITE_LLM4REWRITE_JAR_CLASSPATH_RECOVERY_AUDIT_v1

## 0. Purpose And Boundary
This is a classpath recovery audit only. It does not execute LearnedRewrite, call `LearnedRewriter.learnedRewrite`, connect to PostgreSQL, run checker/speedup, call models, or modify the upstream jar.

## 1. Prior Failure Recap
The original bundled jar is structurally listable with `jar tf`, but JPype class loading against the original jar failed with:

`java.lang.SecurityException: Invalid signature file digest for Manifest main attributes`

A prior temp unsigned-copy attempt avoided the exact signature symptom but produced an invalid jar copy, so class loading remained blocked. This audit checks safer recovery paths using a clean exploded classpath and a clean repacked unsigned jar built in `/tmp` only.

## 2. Original Jar Structure
- Original jar path:
  `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
- `jar tf` status: success
- Signature metadata entries found:
  - `META-INF/MANIFEST.MF`
  - `META-INF/DUMMY.SF`
  - `META-INF/DUMMY.DSA`
- Key class entries found:
  - `learned/LearnedRewriter.class`
  - `learned/Rewriter.class`
  - `learned/MyRules.class`
  - `learned/RewriteResult.class`
  - `learned/Node.class`
  - `rewriter/Rewriter.class`
  - `rewriter/SqlIo.class`
  - `rewriter/DBConn.class`
  - `rewriter/MyRules.class`
  - `rewriter/RewriteResult.class`
- Actual package names present are therefore `learned.*` and `rewriter.*`, and the candidate class names used in prior probes were correct.

## 3. Exploded Classpath Probe
- Temp extract dir:
  `/tmp/rewritebench_learnedrewrite_classpath_recovery/exploded`
- The original jar was extracted there with `jar xf`.
- Signature metadata removal from exploded temp dir: yes
  - removed `META-INF/*.SF`
  - removed `META-INF/*.RSA`
  - removed `META-INF/*.DSA`
- JVM start against exploded classpath: success
- Class lookup via exploded classpath:
  - `learned.LearnedRewriter`: success
  - `learned.Rewriter`: success
  - `rewriter.SqlIo`: success
  - `rewriter.DBConn`: success
- JVM shutdown: success
- LearnedRewrite method invoked: no

This shows the signature blocker can be bypassed by using an exploded temp classpath with signature metadata removed.

## 4. Repacked Jar Probe
- Temp repacked jar path:
  `/tmp/rewritebench_learnedrewrite_classpath_recovery/LearnedRewrite_repacked_unsigned.jar`
- Repack method:
  build a new jar from the clean exploded temp directory using `jar cf`
- `jar tf` status on repacked jar: success
- Class lookup via repacked unsigned jar:
  - `learned.LearnedRewriter`: success
  - `learned.Rewriter`: success
  - `rewriter.SqlIo`: success
  - `rewriter.DBConn`: success
- JVM shutdown: success
- LearnedRewrite method invoked: no

This shows the earlier unsigned-copy failure was due to the copy/rewrite method, not because unsigned recovery is inherently invalid.

## 5. Readiness Decision
`repacked_unsigned_jar_classload_ready`

Both recovery paths worked in temp-only class lookup:
- exploded classpath with signature metadata removed
- clean repacked unsigned jar created from the exploded tree

The repacked unsigned jar is the cleaner artifact for a future bounded smoke because it preserves a single-file classpath handoff while avoiding the original signature failure.

## 6. Remaining Blockers Before LearnedRewrite Smoke
- `single_case_execution_not_implemented`
- `output_sql_extraction_not_tested`
- `checker_handoff_not_run`

The classpath recovery blocker is no longer the primary blocker for a future bounded LearnedRewrite smoke.

## 7. Recommended Next Step
`implement 1-case LearnedRewrite smoke using recovered classpath`

The safer recovery path is:
- prefer the temp repacked unsigned jar built from the clean exploded tree
- keep it in `/tmp` only
- do not use the original signed jar for JPype class loading
- do not rely on JVM signature disabling

## 8. Non-Modification Note
No LearnedRewrite execution occurred. No method calls were made beyond class lookup. No PostgreSQL access, checker, speedup, model/API call, or SQLGlot route execution occurred. The upstream jar and upstream LLM4Rewrite clone were not modified, and no jar was added to the project repo.
