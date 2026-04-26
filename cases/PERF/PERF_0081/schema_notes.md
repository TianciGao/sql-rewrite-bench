# PERF_0081 Schema Notes

## Referenced tables
- `info_type`
- `keyword`
- `movie_info_idx`
- `movie_keyword`
- `title`

## Referenced columns
- `info_type`: `id`, `info`
- `keyword`: `id`, `keyword`
- `movie_info_idx`: `info`, `info_type_id`, `movie_id`
- `movie_keyword`: `keyword_id`, `movie_id`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `movie_info_idx.info` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review
- `keyword.keyword` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are draft-only reductions of the JOB schema and are not final.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
