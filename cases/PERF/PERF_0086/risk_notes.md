# PERF_0086 Risk Notes

## Semantic risks
- Positive equivalence still needs human review because the rewrite was generated from a draft normalization pass.
- Aggregate and `MIN` projections may react to duplicate join paths if witness data is oversimplified.

## Portability risks
- Text predicates (`LIKE`, equality on text labels, country-code filtering) may behave differently across engines or collations.
- Some lookup columns are typed as text in the local JOB schema and may need tighter discipline in MySQL and Spark.

## Null / type / cast / date risks
- No major date or interval construct is foregrounded in this case-local package, but text-pattern boundaries still need review.

## Risk level
- `medium`

## Human review after construction
- required
