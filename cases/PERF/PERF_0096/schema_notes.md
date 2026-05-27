# PERF_0096 Schema Notes

## Referenced tables
- `keyword`
- `link_type`
- `movie_keyword`
- `movie_link`
- `title`

## Referenced columns
- `keyword`: `id`, `keyword`
- `link_type`: `id`, `link`
- `movie_keyword`: `movie_id`, `keyword_id`
- `movie_link`: `movie_id`, `linked_movie_id`, `link_type_id`
- `title`: `id`, `title`

## Uncertain types
- `keyword.keyword` uses text-like semantics and may need tighter cross-engine typing or collation review
- `link_type.link` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
