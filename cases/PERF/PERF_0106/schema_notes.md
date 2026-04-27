# PERF_0106 Schema Notes

- The witness keeps the `complete_cast` status table because that is the distinctive part of this internet-release query family.
- `movie_info.note` and `movie_info.info` are both retained as text because the source relies on release-date and internet-note pattern matching.
- The witness uses one `loner` row and one `nerd` row so the negative rewrite can narrow the keyword set without producing an empty result.
