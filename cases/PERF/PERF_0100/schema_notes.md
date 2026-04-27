# PERF_0100 Schema Notes

- Minimal witness schema includes only `title`, `movie_companies`, `company_name`, `company_type`, `cast_info`, `char_name`, and `role_type`.
- `company_type` and `role_type` are retained even though the source query does not filter them directly, so the positive rewrite can keep an explicit normalized join chain.
- Witness rows are intentionally small and avoid duplicate bridge rows.
