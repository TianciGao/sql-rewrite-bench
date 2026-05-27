# PERF_0085 Witness Design Notes

## Intended equality behavior
- Source and positive rewrite are intended to remain equal because the positive rewrite only normalizes join syntax and query layout.

## Intended negative divergence
- The negative rewrite should differ because it narrows the `aka_name.name` predicate from `%a%` to `%a` under a controlled witness dataset.

## Minimal rows needed
- At least one matching row path across every referenced table.
- At least one boundary row that still satisfies the source and positive query.
- At least one near-miss row that is filtered differently by the negative rewrite.

## Boundary cases
- Duplicate bridge-table rows if needed to preserve aggregate and `MIN` sensitivity.
- One text-matching row and one non-matching row for each important literal or `LIKE` filter.
- One fallback row to test that negative divergence is real rather than empty-result coincidence.

## Open human questions
- Is the current negative rewrite the best divergence mechanism for this query family?
- Does the witness subset need duplicate-preserving rows to avoid accidental aggregate collapse?
- Are any text filters too collation-sensitive for a first official cross-engine pass?
