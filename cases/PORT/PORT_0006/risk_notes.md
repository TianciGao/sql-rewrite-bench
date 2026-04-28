# Risk Notes

- Portability risk: `identifier_quoting`, `boolean_semantics_gap`, `type_semantics_gap`.
- Likely hard-negative failure mode: the threshold predicate expands from `< 100000` to `<= 100000` and changes the percentage.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are not yet implemented
  - checker is draft-only
  - Spark rewrite still needs review
  - no tri-engine validation has been run
