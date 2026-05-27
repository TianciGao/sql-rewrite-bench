# PERF_0080 Risk Notes

## Semantic risks
- Positive equivalence still needs human review because the rewrite was generated from a draft-only normalization pass.
- Aggregate/min projections may react to duplicate join paths if witness data is oversimplified.

## Portability risks
- Text predicates (`LIKE`, equality on text labels, country-code filtering) may behave differently across engines or collations.
- Some lookup columns are typed as text in the local JOB schema and may need tighter discipline in MySQL and Spark.

## Null / type / cast / date risks
- Numeric year filtering is straightforward, but still needs witness-boundary review.

## Risk level
- `low`

## Human review before official construction
- required
