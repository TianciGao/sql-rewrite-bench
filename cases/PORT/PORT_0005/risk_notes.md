# Risk Notes

- Portability risk: `identifier_quoting`, `null_semantics_gap`, `limit_fetch_gap`.
- Likely hard-negative failure mode: the ordering direction or null-handling logic changes the earliest non-null driver row.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are not yet implemented
  - checker is draft-only
  - Spark adaptation still needs review
  - no tri-engine validation has been run
