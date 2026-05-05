# RBOT_LLM4REWRITE_JAR_DEPENDENCY_AUDIT_v1

## 0. Purpose And Boundary

This is a read-only dependency-path audit only for the `LLM4Rewrite` RAG/index build blocker. No RAG build was run, no index was built, no R-Bot method was executed, no model was called, no database was touched, and no SQLGlot route was executed.

## 1. Failure Recap

The earlier tmp RAG/index build failed before any `chroma_db` artifact was created.

Observed failure:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'CalciteRewrite/out/artifacts/LearnedRewrite_jar'
```

No index was created. No R-Bot execution, model call, or DB execution occurred during that failed attempt.

## 2. Path Existence Check

Path check results in the upstream clone:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar` exists: `yes`
- `LearnedRewrite.jar` found anywhere: `yes`
- `CalciteRewrite/out/artifacts` found: `yes`

Exact relevant paths found:

- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar`
- `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`

Conclusion from the existence check:

- this is not a pure “artifact absent from upstream clone” failure
- the jar path exists in the full upstream repo layout
- the earlier failure came from how the import-time path was resolved in the staged tmp build context

## 3. Import Chain / Trigger Analysis

Static chain:

1. `rag/rag_gen.py` imports `NL_RULES` and `NORMAL_RULES` from `rag/gen_rewrites_from_rules.py`
2. `rag/gen_rewrites_from_rules.py` imports:
   - `get_normal_rules`
   - `match_all_rules`
   - `match_normal_rules`
   from `my_rewriter/rewrite.py`
3. `my_rewriter/rewrite.py` immediately does all of the following at import time:
   - imports `jpype`
   - sets `local_lib_dir = 'CalciteRewrite/out/artifacts/LearnedRewrite_jar'`
   - calls `os.listdir(local_lib_dir)`
   - builds JVM classpath
   - starts the JVM if needed

That means the dependency is triggered at import time, not only when a rewrite function is called.

File references:

- `my_rewriter/rewrite.py` is the direct file that references `LearnedRewrite_jar`
- `rag/gen_rewrites_from_rules.py` is the file that imports `my_rewriter/rewrite.py`
- `rag/rag_gen.py` reaches the jar dependency through that import chain

## 4. Is It Needed For RAG-only Build?

For the vector-index build itself, `rag_gen.py` only needs:

- `NL_RULES`
- `NORMAL_RULES`
- local JSONL assets
- embedding/index machinery

It does not directly call:

- `match_all_rules`
- `match_normal_rules`
- `learned_rewrite`
- any Java bridge function

So the LearnedRewrite jar is not intrinsically needed to materialize the vector index.

The coupling exists because:

- `gen_rewrites_from_rules.py` computes `NORMAL_RULES = get_normal_rules()` at import time
- `get_normal_rules()` lives in `my_rewriter/rewrite.py`
- importing `my_rewriter/rewrite.py` has JPype and jar path side effects immediately

Conclusion:

- `rag_gen.py` does not semantically need LearnedRewrite to build the vector index
- the blocker is an unnecessary import side effect
- category is primarily:
  - `C. unnecessary import side effect that can be bypassed for RAG-only build`
- with a secondary staging/layout component:
  - `A. staging/cwd/PYTHONPATH layout error`

It is not best described as:

- `B. missing upstream jar artifact`

And it is weaker than:

- `D. hard coupling between RAG build and LearnedRewrite Java bridge`

because the coupling is real in code today, but appears accidental for RAG-only index creation.

## 5. Candidate Fix/Bypass Options

### Option 1: Run from full upstream repo root layout

- idea: keep cwd/PYTHONPATH aligned so relative `CalciteRewrite/out/artifacts/LearnedRewrite_jar` resolves inside the full upstream tree
- risk: medium
- modifies upstream/project: no
- preserves prior-method fidelity: yes
- should be allowed before smoke: yes

Assessment:

- this addresses the path-resolution part of the failure
- but it still leaves RAG build coupled to JVM startup and the Java bridge at import time

### Option 2: Copy or symlink the CalciteRewrite jar artifact into the staged tmp layout

- idea: make `CalciteRewrite/out/artifacts/LearnedRewrite_jar` exist relative to the tmp build cwd
- risk: medium
- modifies upstream/project: no, if done only in `/tmp`
- preserves prior-method fidelity: mostly yes
- should be allowed before smoke: yes

Assessment:

- this would satisfy the current relative path expectation
- but it still accepts the unnecessary Java bridge dependency in the RAG-only path

### Option 3: Adjust `PYTHONPATH` / cwd only

- idea: point imports back into the full upstream tree and choose cwd so relative paths resolve
- risk: low to medium
- modifies upstream/project: no
- preserves prior-method fidelity: yes
- should be allowed before smoke: yes

Assessment:

- this is the least invasive runtime-layout retry
- however, because `my_rewriter/rewrite.py` uses a relative path literal, cwd still matters

### Option 4: Isolate the RAG build code from the LearnedRewrite import

- idea: bypass or defer `my_rewriter/rewrite.py` for `rag_gen.py`, so `NL_RULES` / `NORMAL_RULES` are obtained without JVM startup
- risk: medium
- modifies upstream/project: yes if done upstream, no if done only in a temp `/tmp` copy
- preserves prior-method fidelity: yes for RAG-only build, if done carefully and documented
- should be allowed before smoke: yes, if restricted to temp-only `/tmp` staging

Assessment:

- this most directly targets the actual root cause
- this is the cleanest conceptual fix for a RAG-only build

### Option 5: Stop until a jar artifact is acquired

- idea: treat the failure as missing artifact and stop
- risk: low
- modifies upstream/project: no
- preserves prior-method fidelity: yes
- should be allowed before smoke: yes

Assessment:

- not the best diagnosis here, because the jar artifact already exists in the upstream clone

## 6. Recommended Next Step

`perform_temp_only_bypass_patch_in_tmp`

Reason:

- the upstream jar artifact is present
- the failure is caused by import-time side effects in `my_rewriter/rewrite.py`
- a temp-only bypass in `/tmp` is the most direct way to test whether RAG-only index creation can proceed without the unrelated Java bridge
- this avoids changing project files or the upstream clone while preserving a bounded, auditable experiment

## 7. Non-Modification Note

This audit performed no build, no model call, no DB execution, no SQLGlot route execution, and no R-Bot execution. It did not modify upstream files, project files, case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md`. The three long-standing taxonomy notes were untouched.
