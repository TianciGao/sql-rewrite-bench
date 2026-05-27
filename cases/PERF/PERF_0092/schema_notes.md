# PERF_0092 Schema Notes

## Referenced tables
- `aka_title`
- `company_name`
- `company_type`
- `info_type`
- `keyword`
- `movie_companies`
- `movie_info`
- `movie_keyword`
- `title`

## Referenced columns
- `aka_title`: `id`, `title`, `movie_id`
- `company_name`: `id`, `country_code`
- `company_type`: `id`
- `info_type`: `id`, `info`
- `keyword`: `id`
- `movie_companies`: `movie_id`, `company_id`, `company_type_id`
- `movie_info`: `movie_id`, `info_type_id`, `note`
- `movie_keyword`: `movie_id`, `keyword_id`
- `title`: `id`, `title`, `production_year`

## Uncertain types
- `aka_title.title` uses text-like semantics and may need tighter cross-engine typing or collation review
- `company_name.country_code` uses text-like semantics and may need tighter cross-engine typing or collation review
- `info_type.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `movie_info.note` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
