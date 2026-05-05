# RBOT_LLM4REWRITE_SQLGLOT_COMPAT_AUDIT_v1

## 0. Purpose And Boundary

This is a read-only `sqlglot` compatibility audit only for the `LLM4Rewrite` RAG/index build path. No RAG build was run, no index was built, no R-Bot method was executed, no model was called, no database was touched, and no SQLGlot route was executed.

## 1. Failure Recap

The earlier temp-only RAG build bypass successfully avoided the LearnedRewrite / JPype import side effect, but then failed on a new compatibility error:

```text
ImportError: cannot import name 'NONDETERMINISTIC' from 'sqlglot.optimizer.simplify'
```

No index was created. No R-Bot execution, model call, or DB execution occurred.

## 2. Offending Import Location

Primary offending file:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/knowledge-base/rule_cluster_funcs/24.py`

Exact import line:

```python
from sqlglot.optimizer.simplify import NONDETERMINISTIC
```

Surrounding usage:

```python
def is_non_deterministic_function(node):
    if isinstance(node, NONDETERMINISTIC):
        return True
    if isinstance(node, exp.Anonymous) and node.name.upper() in NON_DETERMINISTIC_FUNCS:
        return True
    return False
```

This means `NONDETERMINISTIC` is not imported as a dead constant. It is used directly in logic via `isinstance(...)`.

Additional offending file:

- `/tmp/rewritebench_rbot_llm4rewrite_rag_build_bypass/rag/gen_sql_templates.py`

It also imports `NONDETERMINISTIC` and uses it in AST filtering logic:

```python
return all(flags) and len(list(node.find_all(NONDETERMINISTIC))) == 0 and has_no_star(node)
return len(list(node.find_all(tuple(list(NONDETERMINISTIC) + [exp.Identifier])))) == 0 and has_no_star(node)
```

These are copied upstream files, not project files.

## 3. Current sqlglot Environment

- venv path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke`
- installed `sqlglot` version: `30.7.0`
- `sqlglot` module path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/lib/python3.12/site-packages/sqlglot/__init__.py`
- `simplify.py` path: `/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/lib/python3.12/site-packages/sqlglot/optimizer/simplify.py`
- `NONDETERMINISTIC` exists in that module: `no`

Visible nearby names:

- module-level names include `FINAL` and `SIMPLIFIABLE`
- `NONDETERMINISTIC` does exist in the file, but as `Simplifier.NONDETERMINISTIC`, not as a module-level export

So the copied upstream code expects:

- `from sqlglot.optimizer.simplify import NONDETERMINISTIC`

but the installed environment only provides:

- `sqlglot.optimizer.simplify.Simplifier.NONDETERMINISTIC`

## 4. Upstream Requirements Contract

Upstream requirements line:

- `sqlglot`

The dependency is not version-pinned.

The smoke venv therefore installed the latest unconstrained version available during the probe:

- `sqlglot==30.7.0`

Compatibility implication:

- the upstream code is relying on an API shape that is not guaranteed by an unpinned dependency
- the current failure is consistent with an upstream/runtime version mismatch rather than a missing local artifact

## 5. Diagnosis

Primary diagnosis:

`version_mismatch_likely`

Why:

- upstream requirements do not pin `sqlglot`
- installed `sqlglot` is `30.7.0`
- copied upstream files expect a module-level `NONDETERMINISTIC` export that is absent in this installed version
- the installed `simplify.py` still contains a related symbol, but only as `Simplifier.NONDETERMINISTIC`

This also implies:

- upstream code is incompatible with current `sqlglot` as installed
- a temp-only shim is plausible
- but the root cause is still a dependency/API mismatch

## 6. Candidate Fix Options

### A. temp-only shim `NONDETERMINISTIC` in copied build tree

- risk: low to medium
- changes project repo: `no`
- changes upstream clone: `no`
- preserves prior-method fidelity: `partial`
- recommended: `yes`, as the narrowest next experiment

Rationale:

- likely replace the import with a compatible local definition such as `Simplifier.NONDETERMINISTIC`
- bounded to `/tmp`
- directly targets the current blocker

### B. temp-only requirements pin / version sweep for sqlglot

- risk: medium
- changes project repo: `no`
- changes upstream clone: `no`
- preserves prior-method fidelity: `yes`
- recommended: `secondary`

Rationale:

- more faithful to upstream intent if the expected historical version can be recovered
- more expensive than a narrow shim because it reopens dependency probing

### C. recover upstream expected sqlglot version manually

- risk: low
- changes project repo: `no`
- changes upstream clone: `no`
- preserves prior-method fidelity: `yes`
- recommended: `secondary`

Rationale:

- strongest provenance path
- slower than a temp-only shim

### D. stop R-Bot path

- risk: low
- changes project repo: `no`
- changes upstream clone: `no`
- preserves prior-method fidelity: `yes`
- recommended: `no`

Rationale:

- too early to stop because the blocker is now narrow and technically understandable

## 7. Recommended Next Step

`temp-only_shim_and_retry_RAG/index_build`

Reason:

- the incompatibility is narrowly localized
- the expected semantic object appears to exist in installed `sqlglot`, just under a different access path
- a temp-only shim in the copied `/tmp` build tree is the least invasive next step
- it avoids modifying the project repo or upstream clone

## 8. Non-Modification Note

This audit performed no build, no model call, no DB execution, no SQLGlot route execution, and no R-Bot execution. It did not modify project files, upstream files, temp build code, case files, registry files, review files, rules files, or `docs/EXECUTION_STATUS.md`. The three long-standing taxonomy notes were untouched.
