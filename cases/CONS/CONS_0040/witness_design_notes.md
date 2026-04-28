# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair expands IN semantics into explicit count/null-aware left-join logic.
- Expected hard-negative mechanism: Replace IN with NOT IN on the same CASTed deptno subquery.
- Witness complexity: small
