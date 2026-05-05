# LEARNEDREWRITE_LLM4REWRITE_UNSIGNED_JAR_PROBE_v1

## 0. Purpose And Boundary

This is a temp-only unsigned-jar class-load probe for embedded `LearnedRewrite` via upstream `LLM4Rewrite`.

It is not LearnedRewrite execution.
It is not database execution.
It is not checker execution.
It is not speedup evaluation.

No `LearnedRewriter.learnedRewrite(...)` method was invoked.

## 1. Original Blocker

Prior JVM/JAR preflight showed:

- JVM start succeeded
- JPype import succeeded
- class loading failed before any method call with:
  - `java.lang.SecurityException: Invalid signature file digest for Manifest main attributes`

This probe tested whether that blocker was caused by signature metadata inside the bundled jar.

## 2. Temp Copy / Signature Metadata

- original jar path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
- temp jar probe directory:
  - `/tmp/rewritebench_learnedrewrite_unsigned_jar_probe`
- first temp copy:
  - `LearnedRewrite_unsigned_probe.jar`
- second fresh temp copy:
  - `LearnedRewrite_unsigned_probe_clean.jar`

Signature files found in the original jar:

- `META-INF/DUMMY.SF`
- `META-INF/DUMMY.DSA`

Signature files removed from temp copy only:

- `META-INF/DUMMY.SF`
- `META-INF/DUMMY.DSA`

Important notes:

- upstream jar modified: no
- repo jar committed: no
- the shell `zip -d` path was unavailable in this environment
- signature stripping was therefore done only on a fresh `/tmp` copy via Python zip rewriting

## 3. Class-load Probe Result

- java visible: yes
- `java -version`: success
- JPype import: success
- JVM start with temp unsigned copy: success
- class lookup results on temp unsigned copy:
  - `learned.LearnedRewriter`: failed, `TypeError: Class learned.LearnedRewriter is not found`
  - `learned.Rewriter`: failed, `TypeError: Class learned.Rewriter is not found`
  - `rewriter.SqlIo`: failed, `TypeError: Class rewriter.SqlIo is not found`
  - `rewriter.DBConn`: failed, `TypeError: Class rewriter.DBConn is not found`
- JVM shutdown: success
- no LearnedRewrite method invoked: yes

Additional static observation:

- `jar tf` on the fresh unsigned copy failed with:
  - `java.util.zip.ZipException: zip END header not found`

Interpretation:

- removing signature-file entries did avoid the original direct `SecurityException` symptom on class lookup
- but the rewritten unsigned temp jar was not usable as a valid class-loading artifact
- the temp unsigned copy therefore remains blocked by an archive/classpath problem rather than proving readiness

## 4. Readiness Decision

- `classpath_or_dependency_blocker`

Reason:

- original signed jar fails class loading with manifest/signature validation
- rewritten unsigned temp copy no longer demonstrates the same exact error, but it is not class-loadable as a valid jar
- this means the probe did not reach a clean ready state

## 5. Remaining Blockers Before LearnedRewrite Smoke

- jar signature / unsigned-copy packaging blocker
- single_case_execution_not_implemented
- output_sql_extraction_not_tested
- checker_handoff_not_run

## 6. Recommended Next Step

- `fix remaining classpath blocker`

Reason:

- the next issue is no longer just “does a signature problem exist”
- it is “produce a valid unsigned temp jar or equivalent safe classpath layout that class-loads successfully before any smoke”

## 7. Non-Modification Note

No LearnedRewrite execution occurred.
No DB connection occurred.
No checker ran.
No speedup ran.
No model/API call occurred.
No SQLGlot route ran.
No upstream jar was modified.
No repo jar was added or committed.
