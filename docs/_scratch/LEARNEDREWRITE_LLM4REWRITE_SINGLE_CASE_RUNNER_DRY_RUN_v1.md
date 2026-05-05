# LEARNEDREWRITE_LLM4REWRITE_SINGLE_CASE_RUNNER_DRY_RUN_v1

## 1. Purpose And Boundary

This is a dry-run only scaffold for embedded `LearnedRewrite` via upstream `LLM4Rewrite`, targeting `PERF_0006`.

No LearnedRewrite execution occurred.
No JVM start occurred.
No database connection occurred.
No checker or speedup run occurred.
No R-Bot run, model/API call, or SQLGlot route occurred.

## 2. Inputs Checked

- case: `PERF_0006`
- adapter bundle source SQL:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/source.sql`
  - found: yes
- adapter bundle schema:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_adapter_preflight/PERF_0006/create_tables.sql`
  - found: yes
- embedded jar:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
  - found: yes
- runner:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_learned_rewrite.py`
  - found: yes
- Java source / output contract path:
  - `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/src/learned/LearnedRewriter.java`
  - visible: yes

## 3. Runtime Visibility

- `java` visible on `PATH`: yes
  - path: `/usr/bin/java`
- `java -version` executed: no
  - intentionally skipped because this dry-run must not start the JVM
- `jpype` import available in current Python: no
- `jpype` import available in known `/tmp` smoke venv: yes
  - `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python`
- PG env visibility:
  - `PGHOST`: yes
  - `PGPORT`: yes
  - `PGDATABASE`: yes
  - `PGUSER`: yes
  - `PGPASSWORD`: yes
- PostgreSQL connected: no

## 4. Future Execution Artifact Plan

Dry-run output directory:

- `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006`

Artifacts defined:

- future execute command:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/future_execute_command_NOT_RUN.txt`
- artifact path registry:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/artifact_paths.json`
- dry-run summary:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/dry_run_summary.json`
- do-not-run marker:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/DO_NOT_RUN_YET.txt`

Defined future runtime artifact paths:

- future `res.jsonl`:
  - `/tmp/rewritebench_learnedrewrite_logs/rewritebench_perf_0006/res.jsonl`
- future generated SQL capture:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/generated_sql.sql`
- future checker handoff SQL:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/checker_candidate_sql.sql`
- future stdout/stderr:
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/method_stdout.log`
  - `/tmp/rewritebench_learnedrewrite_llm4rewrite_single_case_runner/PERF_0006/method_stderr.log`

## 5. Dry-run Result

- `can_execute_smoke_next`: no

Blockers:

- `java_version_not_checked_due_no_jvm_boundary`
- `jvm_runtime_not_verified`
- `single_case_execution_not_implemented`
- `output_sql_extraction_not_tested`
- `checker_handoff_not_run`

Interpretation:

- the single-case runner dry-run scaffold exists
- the path is materially staged
- the remaining blockers are execution-side verification blockers, not missing-substrate blockers

## 6. Future Execution Command

Documented and marked `NOT RUN`:

```bash
cd /tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter
PYTHONPATH=.. python3 test_learned_rewrite.py \
  --database rewritebench_perf_0006 \
  --logdir /tmp/rewritebench_learnedrewrite_logs
```

This is a future command candidate only.
It was not executed in this step.

## 7. Forbidden Claims

- no LearnedRewrite result
- no checker-backed result
- no speedup result
- no leaderboard result
- no claim that JVM or jar invocation is already validated

## 8. Recommended Next Step

- `verify Java/JVM and jar invocation preflight`

Reason:

- the next unresolved boundary is no longer bundle assembly
- it is the bounded runtime verification needed before any actual single-case smoke

## 9. Non-Modification Note

No execution occurred.
No model/API call occurred.
No DB execution occurred.
No SQLGlot route occurred.
No checker or speedup ran.
No case files, registry files, review files, rules, or `docs/EXECUTION_STATUS.md` were modified.
