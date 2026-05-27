# PERF_0107 Witness Design Notes

## Intended equality behavior
- Source and positive rewrite are intended to remain equal because the positive rewrite only normalizes join syntax and query layout.

## Intended negative divergence
- The negative rewrite should differ because it narrows one stable predicate or literal family under a controlled witness dataset.

## Minimal rows needed
- At least one matching row path across every referenced table.
- At least one retained row that satisfies both source and positive.
- At least one source-only row that is filtered out by the negative rewrite.

## Boundary cases
- Duplicate bridge-table rows should be avoided unless they are explicitly needed to preserve aggregate and `MIN` sensitivity.
- One retained row and one source-only row should make the source and negative outputs differ without relying on empty-result coincidence.
- Text-like predicates should be witnessed with rows that make the positive equivalence obvious and the negative divergence easy to audit.

## Open human questions
- Is the current negative rewrite the best divergence mechanism for this query family?
- Does the witness subset need duplicate-preserving rows to avoid accidental aggregate collapse?
- Are any text filters too collation-sensitive for a first official cross-engine pass?
