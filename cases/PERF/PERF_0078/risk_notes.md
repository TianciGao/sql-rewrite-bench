# PERF_0078 Risk Notes

## Semantic risks
- Positive equivalence still needs human review because the rewrite was generated from a draft-only normalization pass.
- Aggregate/min projections are duplicate-sensitive here because the same `movie_id` is bridged through both `movie_companies` and `movie_keyword`.
- Official construction should keep at least one duplicate-preserving path in the witness subset so `MIN(...)` agreement is not demonstrated only on a degenerate one-row join.

## Portability risks
- Text predicates (`LIKE`, equality on text labels, country-code filtering) may behave differently across engines or collations.
- Some lookup columns are typed as text in the local JOB schema and may need tighter discipline in MySQL and Spark.

## Null / type / cast / date risks
- No major date/interval construct is foregrounded in this draft package.

## Risk level
- `medium`

## Human review after construction
- required
- Confirm that the duplicate-preserving witness rows are sufficient to show that source and positive remain aligned under repeated bridge paths.
