# PERF_0079 Witness Design Notes

## Intended equality behavior
- Source and positive rewrite are intended to remain equal because the positive rewrite only normalizes join syntax and query layout.
- The hardened witness now contains one row with `(voice)` in the interior of the string and one row beginning with `(voice)`, so the source/positive pair should keep both rows while the negative keeps only the anchored one.

## Intended negative divergence
- The negative rewrite should differ by at least one predicate or join condition and therefore produce a different result under a controlled witness dataset.
- The negative rewrite uses `LIKE '(voice)%'`, so the witness should prove divergence by retaining one `x(voice)...` row for the source only and one `(voice)...` row that still survives the negative.

## Minimal rows needed
- At least one matching row path across every referenced table.
- At least one boundary row that still satisfies the source/positive query.
- At least one near-miss row that is filtered differently by the negative rewrite.
- At least one row that fails the source entirely by omitting `(voice)` so the package does not accidentally validate through a too-permissive pattern.

## Boundary cases
- One note value such as `x(voice)y(uncredited)z` should satisfy the source and positive but fail the negative anchored pattern.
- One note value such as `(voice)x(uncredited)tail` should satisfy both the source and the anchored negative so the divergence is shown by result narrowing rather than by an all-empty negative.
- One note value omitting `(voice)` entirely should fail both source and negative and act as a guardrail row.

## Open human questions
- Is the current negative rewrite the best divergence mechanism for this query family?
- Does the witness subset need duplicate-preserving rows to avoid accidental aggregate collapse?
- Are any text filters too collation-sensitive for a first official cross-engine pass?
