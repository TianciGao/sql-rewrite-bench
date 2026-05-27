# PERF_0080 Schema Notes

## Referenced tables
- `company_type`
- `info_type`
- `movie_companies`
- `movie_info_idx`
- `title`

## Referenced columns
- `company_type`: `id`, `kind`
- `info_type`: `id`, `info`
- `movie_companies`: `company_type_id`, `movie_id`, `note`
- `movie_info_idx`: `info_type_id`, `movie_id`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `movie_companies.note` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are draft-only reductions of the JOB schema and are not final.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
