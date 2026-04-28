# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair materializes EXISTS as a grouped TRUE witness relation.
- Expected hard-negative mechanism: Tighten the EXISTS threshold from EMPNO < 20 to EMPNO < 10.
- Witness complexity: small
