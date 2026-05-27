# PERF_0087 Schema Notes

## Referenced tables
- `company_name`
- `company_type`
- `keyword`
- `link_type`
- `movie_companies`
- `movie_keyword`
- `movie_link`
- `title`

## Referenced columns
- `company_name`: `country_code`, `id`, `name`
- `company_type`: `id`, `kind`
- `keyword`: `id`, `keyword`
- `link_type`: `id`, `link`
- `movie_companies`: `company_id`, `company_type_id`, `movie_id`, `note`
- `movie_keyword`: `keyword_id`, `movie_id`
- `movie_link`: `link_type_id`, `movie_id`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `company_name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `keyword.keyword` uses free-text semantics and may need tighter cross-engine typing or collation review
- `link_type.link` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
