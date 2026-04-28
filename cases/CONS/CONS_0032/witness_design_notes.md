# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair decorrelates NOT IN into grouped left-join null-aware counting logic.
- Expected hard-negative mechanism: Replace NOT IN with IN against the same correlated derived-table subquery.
- Witness complexity: small
