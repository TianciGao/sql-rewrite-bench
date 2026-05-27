# PERF_0086 Schema Notes

## Referenced tables
- `aka_name`
- `cast_info`
- `company_name`
- `movie_companies`
- `name`
- `role_type`
- `title`

## Referenced columns
- `aka_name`: `name`, `person_id`
- `cast_info`: `movie_id`, `note`, `person_id`, `role_id`
- `company_name`: `country_code`, `id`
- `movie_companies`: `company_id`, `movie_id`, `note`
- `name`: `id`, `name`
- `role_type`: `id`, `role`
- `title`: `id`, `title`

## Uncertain types
- `aka_name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `cast_info.note` uses free-text semantics and may need tighter cross-engine typing or collation review
- `movie_companies.note` uses free-text semantics and may need tighter cross-engine typing or collation review
- `name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
