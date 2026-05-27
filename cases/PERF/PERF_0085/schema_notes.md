# PERF_0085 Schema Notes

## Referenced tables
- `aka_name`
- `cast_info`
- `info_type`
- `link_type`
- `movie_link`
- `name`
- `person_info`
- `title`

## Referenced columns
- `aka_name`: `name`, `person_id`
- `cast_info`: `movie_id`, `person_id`
- `info_type`: `id`, `info`
- `link_type`: `id`, `link`
- `movie_link`: `link_type_id`, `linked_movie_id`
- `name`: `gender`, `id`, `name`, `name_pcode_cf`
- `person_info`: `info_type_id`, `note`, `person_id`
- `title`: `id`, `production_year`, `title`

## Uncertain types
- `name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `title.title` uses free-text semantics and may need tighter cross-engine typing or collation review
- `aka_name.name` uses free-text semantics and may need tighter cross-engine typing or collation review
- `person_info.note` uses free-text semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
