# PERF_0108 Schema Notes

- This stretch case keeps the complete-cast status tables because that is the point of broadening beyond the earlier non-complete violent writer families.
- `movie_info` models genres as text because the source query filters them textually, while `movie_info_idx` keeps votes as text to match local JOB conventions.
- The witness uses one `Thriller` row and one `Horror` row so the negative rewrite can narrow the genre set without collapsing to an empty result.
