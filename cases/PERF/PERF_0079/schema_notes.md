# PERF_0079 Schema Notes

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
- `cast_info`: `movie_id`, `note`, `person_role_id`, `role_id`
- `company_name`: `country_code`, `id`
- `company_type`: `id`
- `movie_companies`: `company_id`, `company_type_id`, `movie_id`
- `role_type`: `id`, `role`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `char_name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review
- `cast_info.note` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced JOB-schema subsets for case-local validation and are not release-grade final.
- Text-heavy filter columns may need engine-specific collation review before any later formal review.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
