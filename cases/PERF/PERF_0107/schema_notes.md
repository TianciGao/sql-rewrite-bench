# PERF_0107 Schema Notes

- This stretch case keeps both `complete_cast` status semantics and `movie_link` follow-up semantics, which is why its minimal schema is still broader than the other wave-06 packages.
- `linked_movie_id` is retained for the sequel-link topology even though the projection does not read the linked title directly.
- The witness uses one `followed by` row and one `follows` row so the negative rewrite can narrow the link literal family without relying on null-sensitive behavior.
