# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair converts correlated NOT IN into grouped left-join semijoin-style logic.
- Expected hard-negative mechanism: Replace NOT IN with IN on the same correlated DEPT subquery.
- Witness complexity: small
