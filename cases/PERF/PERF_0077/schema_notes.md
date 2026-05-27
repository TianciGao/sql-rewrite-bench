# PERF_0077 Schema Notes

## Case identity

- case_id: `PERF_0077`
- source_family: `JOB/IMDB`
- source query identity: `JOB 3a.sql`
- draft_origin: `JOB_DRAFT_0003`

## Referenced tables

- `keyword`
- `movie_info`
- `movie_keyword`
- `title`

## Referenced columns

- `keyword`: `id`, `keyword`
- `movie_info`: `info`, `movie_id`
- `movie_keyword`: `keyword_id`, `movie_id`
- `title`: `id`, `production_year`, `title`

## Type notes

- `keyword.keyword`, `movie_info.info`, and `title.title` remain text-like columns and may need tighter type/collation review during later validation work.
- Integer key columns are intentionally conservative for first case-local construction.

## Construction caveats

- These DDL files are minimal case-local reductions, not a claim about the full canonical JOB/IMDB schema.
- No validation has been run in this task.
- `inventory/case_registry.csv` is intentionally unchanged in this step.
