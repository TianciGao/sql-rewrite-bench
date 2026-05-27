# PERF_0094 Schema Notes

## Referenced tables
- `cast_info`
- `info_type`
- `movie_info`
- `movie_info_idx`
- `name`
- `title`

## Referenced columns
- `cast_info`: `movie_id`, `person_id`, `note`
- `info_type`: `id`, `info`
- `movie_info`: `movie_id`, `info_type_id`, `info`, `note`
- `movie_info_idx`: `movie_id`, `info_type_id`, `info`
- `name`: `id`, `gender`
- `title`: `id`, `title`, `production_year`

## Uncertain types
- `cast_info.note` uses text-like semantics and may need tighter cross-engine typing or collation review
- `info_type.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `movie_info.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `movie_info.note` uses text-like semantics and may need tighter cross-engine typing or collation review
- `movie_info_idx.info` uses text-like semantics and may need tighter cross-engine typing or collation review
- `name.gender` uses text-like semantics and may need tighter cross-engine typing or collation review
- `title.title` uses text-like semantics and may need tighter cross-engine typing or collation review

## Cross-engine schema caveats
- These DDL files are reduced case-local witness schemas, not full JOB schema reproductions.
- Text-heavy filter columns may need engine-specific collation review before official construction.
- Integer foreign-key assumptions should be rechecked against the full local JOB schema before execution.
