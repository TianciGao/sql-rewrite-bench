# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair materializes global EXISTS state and combines it with a local predicate.
- Expected hard-negative mechanism: Replace OR with AND against the same EXISTS state and salary predicate.
- Witness complexity: small
