# PERF_0102 Schema Notes

- This package keeps the compact `name` plus `character-name-in-title` keyword join family with only the bridge tables needed by the source query.
- `title` is retained even though no title predicate is applied so the witness matches the original JOB join topology.
- The witness is intentionally minimal and uses one `B%` row and one `C%` row to make the negative rewrite divergence easy to audit.
