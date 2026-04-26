# PERF_0084 Schema Notes

## Referenced tables
- `company_name`
- `company_type`
- `info_type`
- `movie_companies`
- `movie_info`
- `movie_info_idx`
- `title`

## Referenced columns
- `company_name`: `country_code`, `id`, `name`
- `company_type`: `id`, `kind`
- `info_type`: `id`, `info`
- `movie_companies`: `company_id`, `company_type_id`, `movie_id`
- `movie_info`: `info`, `info_type_id`, `movie_id`
- `movie_info_idx`: `info`, `info_type_id`, `movie_id`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `company_name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `movie_info_idx.info` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review
- `movie_info.info` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are draft-only reductions of the JOB schema and are not final.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
