# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair isolates CASE expression before grouping while preserving outer-join semantics.
- Expected hard-negative mechanism: Use INNER JOIN instead of LEFT JOIN to drop unmatched bonus rows.
- Witness complexity: small
