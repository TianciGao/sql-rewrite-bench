# PERF_0078 Witness Design Notes

## Intended equality behavior
- Source and positive rewrite are intended to remain equal because the positive rewrite only normalizes join syntax and query layout.
- The hardened witness now includes one main `[us]` / `B%` path that should satisfy source and positive, plus near-miss rows that fail either the country-code or name filter without changing the join topology.

## Intended negative divergence
- The negative rewrite should differ by at least one predicate or join condition and therefore produce a different result under a controlled witness dataset.
- The negative rewrite changes `[us]` to `[gb]`, so the witness should preserve one `[gb]` movie path and one `[us]` path to make the country-code divergence explicit rather than empty-result accidental.

## Minimal rows needed
- At least one matching row path across every referenced table.
- At least one boundary row that still satisfies the source/positive query.
- At least one near-miss row that is filtered differently by the negative rewrite.
- At least one duplicate-preserving bridge path so aggregate stability is exercised under repeated `movie_id` joins.

## Boundary cases
- Duplicate bridge-table rows are intentional here because `MIN(name)` can otherwise look stable on an unrealistically tiny witness.
- One `B%` name row and one non-`B%` row should coexist on otherwise similar movie paths.
- One `[us]` company row and one `[gb]` company row should coexist so the negative rewrite is rejected for the right reason.

## Open human questions
- Is the current negative rewrite the best divergence mechanism for this query family?
- Does the witness subset need duplicate-preserving rows to avoid accidental aggregate collapse?
- Are any text filters too collation-sensitive for a first official cross-engine pass?
