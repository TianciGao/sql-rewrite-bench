# PERF_0091 Schema Notes

## Referenced tables
- `company_name`
- `company_type`
- `info_type`
- `kind_type`
- `movie_companies`
- `movie_info`
- `movie_info_idx`
- `title`

## Referenced columns
- `company_name`: `id`, `country_code`, `name`
- `company_type`: `id`, `kind`
- `info_type`: `id`, `info`
- `kind_type`: `id`, `kind`
- `movie_companies`: `movie_id`, `company_id`, `company_type_id`
- `movie_info`: `movie_id`, `info_type_id`
- `movie_info_idx`: `movie_id`, `info_type_id`, `info`
- `title`: `id`, `title`, `kind_id`

## Uncertain types
- `company_name.country_code` uses text-like semantics and may need tighter cross-engine typing or collation review
- `company_name.name` uses text-like semantics and may need tighter cross-engine typing or collation review
- `company_type.kind` uses text-like semantics and may need tighter cross-engine typing or collation review
- `info_type.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `kind_type.kind` uses text-like semantics and may need tighter cross-engine typing or collation review
- `movie_info_idx.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
