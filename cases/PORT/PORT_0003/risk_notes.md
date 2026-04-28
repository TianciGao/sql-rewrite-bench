# Risk Notes

- Portability risk: `identifier_quoting`, `null_semantics_gap`, `limit_fetch_gap`.
- Likely hard-negative failure mode: a naive top-1 ordering rewrite mishandles null placement or flips the absolute-longitude ranking direction.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are not yet implemented
  - checker is draft-only
  - Spark adaptation still needs review
  - no tri-engine validation has been run
