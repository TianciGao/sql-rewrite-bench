# PERF_0109 Schema Notes

- This package preserves the Lionsgate company filter and violent keyword family while keeping only the bridge tables needed for the source query.
- `company_name.name` is the key text predicate column and remains text-typed across engines.
- The witness uses one `Action` row and one `Horror` row so the narrower negative genre set changes the aggregate output instead of producing an empty result.
