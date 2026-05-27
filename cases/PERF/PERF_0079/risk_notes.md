# PERF_0079 Risk Notes

## Semantic risks
- Positive equivalence still needs human review because the rewrite was generated from a draft-only normalization pass.
- The main hardening fix here is witness-driven rather than SQL-driven: official construction should verify that the source/positive pair still returns rows once both `(voice)` and `(uncredited)` are present.
- The anchored negative `LIKE '(voice)%'` is intentionally stricter, but it remains text-pattern-sensitive and should be treated as a medium-risk divergence mechanism until reviewed on all engines.

## Portability risks
- Text predicates (`LIKE`, equality on text labels, country-code filtering) may behave differently across engines or collations.
- Some lookup columns are typed as text in the local JOB schema and may need tighter discipline in MySQL and Spark.

## Null / type / cast / date risks
- Numeric year filtering is straightforward, but still needs witness-boundary review.

## Risk level
- `medium`

## Human review after construction
- required
- Confirm that the witness retains one row matching both source predicates but failing the anchored negative, plus one row matching both, so divergence is not demonstrated by an all-empty negative.
