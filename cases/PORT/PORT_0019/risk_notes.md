# Risk Notes

- Portability focus: aggregate_edge_case, pagination_or_limit_offset.
- Primary draft risk: grouped-count ordering can drift if the target rewrite changes the top-1 direction.
- This package received a static source-literal and Spark runner repair only; that does not imply any validation or plan evidence.
- This package is draft-only, not registered, not validated, not admitted, and not under formal review.
