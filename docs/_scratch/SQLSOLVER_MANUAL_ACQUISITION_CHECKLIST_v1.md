# SQLSOLVER_MANUAL_ACQUISITION_CHECKLIST_v1

## 0. Status

This document is documentation-only. It is not implementation, not execution, not a runnable-substrate claim, not registry writeback, and not a closeout artifact.

SQLSolver remains support-only, not a rewrite baseline and not a speedup baseline. Based on current repo-local evidence, the current state remains `not_integrated / no runnable wrapper`.

## 1. Support-only Boundary

SQLSolver should be evaluated only as verifier/support evidence. It must not be reported in `GM_Speedup`, `W/T/L`, or `RegressionRate` tables, and it must not be presented as part of the same-engine rewrite leaderboard.

If SQLSolver is acquired later, its outputs should contribute only to verifier/support metrics such as prove, refute, unknown, timeout, and unsupported. Positive equivalence proof, negative refutation, timeout, and unsupported cases must be reported separately. SQLSolver results must not override RewriteBench execution-checker results unless a separate explicit policy is defined first.

## 2. External Artifacts Needed

Manual acquisition must recover the following external artifacts and contracts:

- Exact SQLSolver source repository or archived artifact location.
- Exact commit hash, release tag, or archived package identifier.
- Solver binary or complete build instructions.
- Dependency and runtime contract.
- SMT or theorem-prover dependencies, if required.
- Supported SQL dialect and supported SQL subset definition.
- Supported schema and constraint language.
- License and redistribution constraints.
- Timeout and runtime assumptions.
- Hardware and runtime assumptions.
- At least one example invocation from the original artifact, if available.

Current repo-local evidence does not provide a runnable SQLSolver checkout, pinned dependency stack, or local wrapper.

## 3. Input Contract To Recover

Manual acquisition must recover the precise SQLSolver input contract, including:

- Whether SQLSolver accepts SQL query pairs directly.
- Whether it requires schema DDL.
- Whether it requires constraints such as keys, uniqueness, foreign keys, nullability, or check constraints.
- Whether it supports aggregates, `EXISTS`, `NOT EXISTS`, correlated subqueries, `NULL` semantics, bags or duplicates, arithmetic, and date/time functions.
- Whether it expects canonicalized SQL or an internal algebra form.
- Whether it expects PostgreSQL syntax, Calcite-like algebra, or its own grammar.
- Whether witness data is used or whether the method is purely symbolic.
- Whether RewriteBench positive and negative pairs can be handled independently.

Current repo-local evidence suggests a pair-of-queries-plus-schema style contract, but it does not recover the full constraint contract or supported SQL-fragment boundary well enough to claim readiness.

## 4. Output Contract To Recover

Manual acquisition must recover the exact SQLSolver output contract, including:

- Whether it emits `equivalent`, `non_equivalent`, `unknown`, `timeout`, or `unsupported`.
- Whether it emits counterexamples or models.
- Whether it emits proof traces.
- Whether it distinguishes parser failure from unsupported feature from solver timeout.
- Whether it emits machine-readable results.
- Whether outputs can be mapped into a RewriteBench support table without manual interpretation.

Required future support categories:

- `proved_equivalent`
- `refuted_equivalence`
- `unknown`
- `timeout`
- `unsupported_sql`
- `parser_or_translation_failure`
- `internal_error`

Until that contract is recovered, SQLSolver cannot be counted as runnable support evidence.

## 5. RewriteBench Adapter Boundary

No wrapper or adapter should be created now.

Any future adapter must define:

- Case-package positive pair to SQLSolver input.
- Case-package negative pair to SQLSolver input.
- Schema and constraint extraction path.
- Constraint-bridge policy.
- Timeout policy.
- Unsupported-feature policy.
- Output mapping into a verifier/support table.
- A strict rule that SQLSolver output must not be fed into the speedup leaderboard.

Artifact paths needed later for reproducibility:

- `source_snapshot_ref`
- `solver_dependency_ref`
- `input_contract_note`
- `constraint_policy_note`
- `pair_input_artifacts`
- `solver_stdout_stderr`
- `machine_readable_verdict`
- `timeout_metadata`
- `unsupported_feature_log`
- `support_summary_json`

## 6. Minimum Bounded Support Smoke After Acquisition

Only after acquisition succeeds, the first bounded smoke should remain tightly scoped:

- Denominator: `1-3` `CONS` cases only.
- Support-only, not rewrite leaderboard evidence.
- No registry writeback.
- No admission or common-core claim.
- No speedup claim.

Suggested first subset:

- `CONS_0007`
- `CONS_0035`
- One additional simple `CONS` case only if its schema and constraint contract is clear.

Required first-smoke metrics:

- `prove_count`
- `refute_count`
- `unknown_count`
- `timeout_count`
- `unsupported_count`
- `parser_or_translation_failure_count`

Claim boundary for any future smoke:

`bounded_SQLSolver_support_smoke_only_not_rewrite_baseline`

## 7. Stop Conditions

Stop and classify acquisition as blocked if any of the following remains unresolved:

- No source repository or artifact package.
- No runnable entrypoint.
- No build or dependency contract.
- No supported SQL subset documentation.
- No schema or constraint input contract.
- No timeout policy.
- No machine-readable verdict.
- No license clarity.
- Requires a private solver service or inaccessible dependency.
- Cannot distinguish unsupported SQL from non-equivalence.
- Cannot map output into a support table.

## 8. Final Decision Tree

- `acquired_and_runnable_support_only`
  Exact source, dependencies, input/output contract, timeout policy, and runnable support path are all pinned and reproducible, but SQLSolver remains support-only and out of the rewrite leaderboard.

- `acquired_but_wrapper_needed`
  Upstream artifacts and contracts are recovered, but RewriteBench still lacks the minimal wrapper or adapter needed to run a bounded support smoke.

- `acquired_but_not_reproducible`
  Some artifact or invocation exists, but the dependency, license, timeout, or machine-readable verdict contract is too weak for reproducible support evidence.

- `unavailable_blocked`
  Source, dependency, wrapper, subset, or verdict contract is too incomplete to proceed safely.

- `out_of_scope_for_rewrite_leaderboard`
  Even if acquired and runnable, SQLSolver must remain outside rewrite and speedup leaderboard reporting.

## 9. Current Provisional Decision

Based only on current repo-local evidence, SQLSolver should currently be classified as:

- `not_integrated`
- `support_only`
- `unavailable_blocked` for runnable support evidence until source, wrapper, and dependencies are acquired

## 10. Relationship To VeriEQL

VeriEQL already has bounded support-canary evidence in repo history. SQLSolver does not have a repo-local runnable wrapper yet and should not inherit VeriEQL status by analogy.

Both SQLSolver and VeriEQL belong in a support/verifier table rather than a speedup leaderboard. Any future SQLSolver result should therefore be framed as support-only evidence, separate from rewrite-route and speedup-route reporting.

## 11. Recommended Next Step

The next step should be manual acquisition of SQLSolver upstream artifacts.

This is preferable to moving immediately to a SlabCity external-service acquisition checklist because SQLSolver has a narrower support-only role, clearer support-table boundary, and a more straightforward criteria set for deciding whether reproducible bounded support evidence is even possible.

## 12. Non-Modification Note

No execution occurred. No download occurred. No model call occurred. No DB run occurred. No SQLGlot run occurred. No wrapper was created. No adapter was created. No script was modified. No registry, review, rules, or `docs/EXECUTION_STATUS.md` file was modified.
