# PERF_0095 Schema Notes

## Referenced tables
- `complete_cast`
- `comp_cast_type`
- `char_name`
- `cast_info`
- `keyword`
- `kind_type`
- `movie_keyword`
- `name`
- `title`

## Referenced columns
- `complete_cast`: `movie_id`, `subject_id`, `status_id`
- `comp_cast_type`: `id`, `kind`
- `char_name`: `id`, `name`
- `cast_info`: `movie_id`, `person_role_id`, `person_id`
- `keyword`: `id`, `keyword`
- `kind_type`: `id`, `kind`
- `movie_keyword`: `movie_id`, `keyword_id`
- `name`: `id`
- `title`: `id`, `title`, `production_year`, `kind_id`

## Uncertain types
- `comp_cast_type.kind` uses text-like semantics and may need tighter cross-engine typing or collation review
- `char_name.name` uses text-like semantics and may need tighter cross-engine typing or collation review
- `keyword.keyword` uses text-like semantics and may need tighter cross-engine typing or collation review
- `kind_type.kind` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
