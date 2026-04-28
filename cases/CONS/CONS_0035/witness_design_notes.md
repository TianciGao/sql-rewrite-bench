# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair reduces per-group COUNT(MGR) to row-local NULL test under unique grouping.
- Expected hard-negative mechanism: Replace COUNT(MGR) with COUNT(*) semantics.
- Witness complexity: small
