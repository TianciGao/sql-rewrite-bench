# Risk Notes

- Portability risk: `identifier_quoting`, `boolean_semantics_gap`, `type_semantics_gap`.
- Likely hard-negative failure mode: the threshold predicate expands from `< 100000` to `<= 100000` and changes the percentage.
- Witness rows intended to expose the failure: mixed `status` values plus an `amount = 100000` boundary row and at least one row strictly below the threshold.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are still draft fixtures and have not been loaded
  - checker is draft-only and not executed
  - Spark rewrite still needs review
  - no tri-engine validation has been run
  - common-core vs extended status remains unresolved
