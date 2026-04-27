# PERF_0103 Schema Notes

- Only the six source tables needed for the producer budget-and-votes family are retained.
- `movie_info.info` and `movie_info_idx.info` stay text-typed to match the local JOB style while remaining easy to load across engines.
- The witness intentionally uses one producer row and one executive-producer row so the note narrowing changes the aggregate output.
