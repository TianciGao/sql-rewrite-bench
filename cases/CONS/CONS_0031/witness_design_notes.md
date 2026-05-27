# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair rewrites nested EXISTS / NOT EXISTS into grouped boolean-join form.
- Expected hard-negative mechanism: Flip NOT EXISTS to EXISTS on the same correlated job predicate.
- Witness complexity: small
