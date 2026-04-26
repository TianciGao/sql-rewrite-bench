# PERF_0093 Schema Notes

## Referenced tables
- `aka_name`
- `cast_info`
- `company_name`
- `keyword`
- `movie_companies`
- `movie_keyword`
- `name`
- `title`

## Referenced columns
- `aka_name`: `id`, `name`, `person_id`
- `cast_info`: `movie_id`, `person_id`
- `company_name`: `id`, `country_code`
- `keyword`: `id`, `keyword`
- `movie_companies`: `movie_id`, `company_id`
- `movie_keyword`: `movie_id`, `keyword_id`
- `name`: `id`
- `title`: `id`, `title`, `episode_nr`

## Uncertain types
- `aka_name.name` uses text-like semantics and may need tighter cross-engine typing or collation review
- `company_name.country_code` uses text-like semantics and may need tighter cross-engine typing or collation review
- `keyword.keyword` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
