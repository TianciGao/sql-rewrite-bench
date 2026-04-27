# PERF_0101 Schema Notes

- Minimal witness schema keeps only the pseudonym, person, keyword, company, and episodic title tables referenced by the query family.
- `episode_nr` is typed numerically in all engines because the negative rewrite narrows the lower bound.
- Witness rows use two episodes so the negative threshold changes the `MIN` result instead of collapsing to an empty set.
