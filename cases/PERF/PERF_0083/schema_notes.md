# PERF_0083 Schema Notes

## Referenced tables
- `cast_info`
- `keyword`
- `movie_keyword`
- `name`
- `title`

## Referenced columns
- `cast_info`: `movie_id`, `person_id`
- `keyword`: `id`, `keyword`
- `movie_keyword`: `keyword_id`, `movie_id`
- `name`: `id`, `name`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `keyword.keyword` uses free-text semantics and may need tighter cross-engine typing or collation review
- `name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are draft-only reductions of the JOB schema and are not final.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
