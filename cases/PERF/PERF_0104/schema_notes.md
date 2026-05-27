# PERF_0104 Schema Notes

- This witness preserves the `movie_link` plus `movie_companies` plus country-info chain of the source query while dropping unrelated JOB columns.
- `linked_movie_id` is retained even though the source projection does not read the linked title because the source family is fundamentally a follow-up link query.
- The witness uses one earlier and one later German follow-up so the narrower year window changes the aggregate result.
