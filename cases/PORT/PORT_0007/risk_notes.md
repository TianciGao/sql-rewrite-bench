# Risk Notes

- Portability risk: `identifier_quoting`, `null_semantics_gap`, `limit_fetch_gap`.
- Likely hard-negative failure mode: the target rewrite drops or weakens the intended null-aware descending score ordering and returns the wrong comment text.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: medium.
- Blockers before registry writeback:
  - witness rows are not yet implemented
  - checker is draft-only
  - Spark adaptation still needs review
  - subquery and ordering semantics need later tri-engine validation
