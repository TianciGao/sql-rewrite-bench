# REMAINING_PRIOR_BASELINES_FEASIBILITY_v0

## Status

This note audits the remaining prior-method baseline lines for bounded runnable-subset feasibility only.

Audited baselines:

- `LearnedRewrite`
- `GenRewrite`
- `R-Bot`
- `LLM-R2`
- `SlabCity`
- `SQLSolver`
- `VeriEQL`

Explicit boundary:

- no experiments
- no model calls
- no PostgreSQL execution
- no checker execution
- no speedup execution
- no registry or formal review update

## Executive Conclusion

Current result:

- `runnable_now=yes`: `0 / 7`
- `runnable_now=no`: `7 / 7`
- best next bounded candidate among not-yet-advanced lines: none

Interpretation:

- none of the remaining prior baselines can move immediately to a runnable bounded subset with the current repo state
- `VeriEQL` is the only line that has now moved beyond pure feasibility and into bounded support-canary evidence
- `LearnedRewrite`, `GenRewrite`, `R-Bot`, and `LLM-R2` have plausible first subsets on the clean 4-case PERF slice, but they still lack the core execution substrate
- `SQLSolver` and `VeriEQL` belong in a verifier/support table, not a same-engine speedup table
- `SlabCity` remains blocked unless a local runner or reproducible service/runtime contract appears

## Shared Reuse Finding

For the rewrite-style baselines, the bounded first subset can reuse existing case-package inputs if a candidate-SQL generator ever appears:

- `source.sql`
- `schema/ddl_pg.sql`
- `validation/checker.yaml`
- existing PostgreSQL checker path
- existing PostgreSQL speedup path

For the verifier/support lines, the reusable substrate is narrower:

- `source.sql`
- `schema/ddl_pg.sql`
- `validation/checker.yaml`

They do not belong on the PostgreSQL speedup path.

## Per-Baseline Table

| baseline | current_status | runnable_now | exact blocker category | candidate subset | expected metrics if runnable | belongs to | recommended next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LearnedRewrite` | `preflight_only` | no | `artifact_stack_missing` | `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` | generation, PG execution, checker consistency, speedup | backlog only | keep as readiness-only unless a repo-local adapter, checkpoint, and inference path are added |
| `GenRewrite` | `preflight_only` | no | `missing_genrewrite_control_stack` | `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` | generation, PG execution, checker consistency, speedup, token usage | backlog only | keep in backlog until a bounded correction/verifier loop with frozen budget and prompt controls exists |
| `R-Bot` | `preflight_only` | no | `missing_retrieval_control_stack` | `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` | generation, PG execution, checker consistency, speedup, token usage | backlog only | keep in backlog until a reproducible retrieval corpus, demo policy, and rule-selection path exist |
| `LLM-R2` | `preflight_only` | no | `missing_retrieval_control_stack` | `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` | generation, PG execution, checker consistency, speedup, token usage | backlog only | keep in backlog until demonstration selection and rule-application paths are explicit and reproducible |
| `SlabCity` | `blocked` | no | `no_local_runner_or_service_contract` | `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054` in principle only | generation, PG execution, checker consistency, speedup | backlog only | keep blocked unless a local runner or reproducible service contract is added first |
| `SQLSolver` | `not_integrated` | no | `solver_wrapper_and_dependency_missing` | `CONS_0007` | verifier support verdict, unknown rate, timeout rate | verifier/support table | keep as support-only backlog unless a repo-local SQLSolver checkout and wrapper are added |
| `VeriEQL` | `bounded_support_canary_evidence` | no | `positive_proof_not_closed_under_constraint_bridge` | bounded support canary `CONS_0035` | support verdicts, refutation evidence, timeout rate under bridge | verifier/support table | keep as bounded support evidence only; do not promote to rewrite/speedup baseline |

## Detailed Findings

### LearnedRewrite

- Existing readiness scaffold already identifies `PERF_0006`, `PERF_0008`, `PERF_0033`, and `PERF_0054` as the clean first subset.
- The repo still has no adapter, no checkpoint, no inference entrypoint, and no canonical representation bridge.
- Result: it is not runnable now and remains backlog-only despite a plausible bounded denominator.

### GenRewrite

- Existing readiness scaffold again points to the same clean 4-case PERF subset.
- The decisive gap is not prompting alone; it is the missing control stack:
  - correction loop
  - verifier loop
  - executor-feedback loop
  - prompt/rule library
  - retry and correction-budget policy
  - pricing/cost freeze
- Result: not runnable now; still backlog-only.

### R-Bot / LLM-R2

- Both retrieval-based methods also have the same clean analytical 4-case PERF subset as the best first denominator.
- The repo has no retrieval corpus, no index, no demo selector, no rule pool, no rerank path, and no fair-comparison / contamination policy.
- Result: neither method is runnable now, and neither should move beyond backlog status until the retrieval substrate exists.

### SlabCity

- Prior readiness work still holds: there is no local runner, no synthesis adapter, no solver/verifier stack, and no reproducible service contract in the repo.
- Clean PERF cases would be the only plausible first denominator in principle, but there is no executable substrate to connect them to.
- Result: remains blocked.

### SQLSolver

- There is still no repo-local SQLSolver checkout, wrapper, or solver dependency path.
- It should be treated only as a verifier/support line, not a same-engine runtime baseline.
- `CONS_0007` remains the best bounded support candidate if SQLSolver were ever staged locally.
- Result: support-table candidate in theory, but not runnable now.

### VeriEQL

- Unlike the other remaining lines, the repo does contain a staged `VeriEQL` codebase under `datasets/raw/verieql/staged/VeriEQL/`, including:
  - `README.md`
  - `requirements.txt`
  - `__main__.py`
  - benchmark and verifier modules
- That made `VeriEQL` the strongest feasibility target, and it has since advanced beyond that stage.
- Current bounded evidence now exists on `CONS_0035`:
  - empty constraint: `source_positive=non_equivalent`, `source_negative=non_equivalent`
  - report-local uniqueness bridge on `(EMPNO, DEPTNO)`: constrained `source_positive=timeout`, constrained `source_negative=non_equivalent`
  - `prove_count=0`
- Interpretation:
  - negative-pair refutation is real support evidence
  - positive side is constraint-sensitive
  - positive proof is still not closed under the bounded bridge experiment
- Result: no longer pure feasibility-only, but still not runnable-now as a general verifier baseline and still not promotable beyond bounded support-canary evidence.

## Recommended Classification

- `LearnedRewrite`: backlog only for now; would belong to the main same-engine speedup table only after a real runner/checkpoint path exists
- `GenRewrite`: backlog only for now; main same-engine LLM prior baseline only after a bounded correction/verifier loop exists
- `R-Bot`: backlog only for now; appendix or main baseline only after retrieval/rule-selection infrastructure is explicit
- `LLM-R2`: backlog only for now; appendix or main baseline only after demonstration/rule-selection infrastructure is explicit
- `SQLSolver`: verifier/support table only
- `VeriEQL`: verifier/support table only, now with bounded support-canary evidence on `CONS_0035`
- `SlabCity`: backlog only until a local runner/service contract exists

## Recommended Next Action

If one remaining prior-method line is advanced next, it should not restart VeriEQL feasibility from scratch. VeriEQL already has bounded support-canary evidence.

The remaining backlog emphasis should stay on the still-unadvanced lines:

1. keep `VeriEQL` as bounded support evidence with caveat
2. leave `SQLSolver` as support-only backlog
3. leave `LearnedRewrite`, `GenRewrite`, `R-Bot`, `LLM-R2`, and `SlabCity` unchanged until real substrate appears

Everything else should remain backlog/readiness-only until core missing substrate appears.
