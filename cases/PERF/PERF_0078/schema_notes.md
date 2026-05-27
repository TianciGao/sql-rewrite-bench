# PERF_0078 Schema Notes

## Referenced tables
- `cast_info`
- `company_name`
- `keyword`
- `movie_companies`
- `movie_keyword`
- `name`
- `title`

## Referenced columns
- `cast_info`: `movie_id`, `person_id`
- `company_name`: `country_code`, `id`
- `keyword`: `id`, `keyword`
- `movie_companies`: `company_id`, `movie_id`
- `movie_keyword`: `keyword_id`, `movie_id`
- `name`: `id`, `name`
- `title`: `id`

## Uncertain types
- `name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `keyword.keyword` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced JOB-schema subsets for case-local validation and are not release-grade final.
- Text-heavy filter columns may need engine-specific collation review before any later formal review.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
