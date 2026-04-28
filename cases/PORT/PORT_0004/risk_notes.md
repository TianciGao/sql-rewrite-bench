# Risk Notes

- Portability risk: `identifier_quoting`, `datetime_semantics_gap`, `type_semantics_gap`.
- Likely hard-negative failure mode: the year-filter rewrite shifts from 1980 to 1981 and changes the aggregate percentage.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are not yet implemented
  - aggregate checker behavior is only drafted
  - Spark rewrite still needs review
  - no validation evidence exists yet
