# PERF_0090 Schema Notes

## Referenced tables
- `char_name`
- `cast_info`
- `company_name`
- `company_type`
- `movie_companies`
- `role_type`
- `title`

## Referenced columns
- `char_name`: `id`, `name`
- `cast_info`: `id`, `note`, `movie_id`, `person_role_id`, `role_id`
- `company_name`: `id`, `country_code`
- `company_type`: `id`
- `movie_companies`: `movie_id`, `company_id`, `company_type_id`
- `role_type`: `id`, `role`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `char_name.name` uses text-like semantics and may need tighter cross-engine typing or collation review
- `cast_info.note` uses text-like semantics and may need tighter cross-engine typing or collation review
- `company_name.country_code` uses text-like semantics and may need tighter cross-engine typing or collation review
- `role_type.role` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
