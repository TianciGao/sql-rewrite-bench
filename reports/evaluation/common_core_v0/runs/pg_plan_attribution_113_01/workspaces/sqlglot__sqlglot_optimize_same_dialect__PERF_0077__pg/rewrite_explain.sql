set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_perf_0077_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* case_id: PERF_0077 */ /* source_family: JOB/IMDB */ /* original JOB query: 3a.sql */ /* draft_origin: JOB_DRAFT_0003 */
SELECT
  MIN("t"."title") AS "movie_title"
FROM "keyword" AS "k"
JOIN "movie_keyword" AS "mk"
  ON "k"."id" = "mk"."keyword_id"
JOIN "title" AS "t"
  ON "mk"."movie_id" = "t"."id" AND "t"."production_year" > 2005
JOIN "movie_info" AS "mi"
  ON "mi"."info" IN (
    'Sweden',
    'Norway',
    'Germany',
    'Denmark',
    'Swedish',
    'Denish',
    'Norwegian',
    'German'
  )
  AND "mi"."movie_id" = "mk"."movie_id"
  AND "mi"."movie_id" = "t"."id"
WHERE
  "k"."keyword" LIKE '%sequel%';
rollback;
