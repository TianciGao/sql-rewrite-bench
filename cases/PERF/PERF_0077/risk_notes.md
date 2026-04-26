# PERF_0077 Risk Notes

## Construction-state caveat

- This is an official case-local construction package only.
- It is not yet registry-admitted, not yet validated, and carries no admission, promotion, common-core, or extended claim.

## Semantic risks

- The positive rewrite is intended to be equivalent, but later human review should still confirm that the explicit inner-join normalization preserves the original semantics exactly.
- `MIN(title)` can appear stable on an overly small witness, so the later validation pass should keep the multi-path witness structure intact.

## Portability risks

- The negative rewrite depends on text `LIKE` semantics around `%sequel%` versus `sequel%`.
- Text filtering and collation behavior may differ slightly across PostgreSQL, MySQL, and Spark and should be reviewed before interpreting cross-engine results.

## Validation-state risks

- No validation or plan collection has been run in this task.
- The validation scripts are prepared for later use only.

## Current risk level

- `low` for case-local construction quality
- `medium` for later cross-engine semantics review
