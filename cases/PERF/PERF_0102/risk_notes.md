# PERF_0102 Risk Notes

## Semantic risks
- Positive equivalence still needs human review because the rewrite was normalized directly from the local JOB source query.
- Aggregate and `MIN` projections may react to duplicate join paths if witness data is oversimplified.

## Portability risks
- Text predicates (`LIKE`, equality on text labels, country-code filtering) may behave differently across engines or collations.
- Some lookup columns are typed as text in the local JOB schema and may need tighter discipline in MySQL and Spark.

## Null / type / cast / date risks
- Numeric filters are intentionally preferred in this package when possible, but witness-boundary review is still required before treating the case as stable.

## Risk level
- `low`

## Stretch candidate
- no

## Human review after construction
- required
