set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_perf_0082_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
/* draft_id: JOB_DRAFT_0005 */ /* original local source path: /home/tianci_gao/code/sql-rewrite-bench/runs/codex_overnight/job_candidate_drafts_30/candidates/JOB_DRAFT_0005/source.sql */ /* not official case */
SELECT
  MIN("t"."title") AS "typical_european_movie"
FROM "company_type" AS "ct"
JOIN "movie_companies" AS "mc"
  ON "ct"."id" = "mc"."company_type_id"
  AND "mc"."note" LIKE '%(France)%'
  AND "mc"."note" LIKE '%(theatrical)%'
JOIN "movie_info" AS "mi"
  ON "mc"."movie_id" = "mi"."movie_id"
  AND "mi"."info" IN (
    'Sweden',
    'Norway',
    'Germany',
    'Denmark',
    'Swedish',
    'Denish',
    'Norwegian',
    'German'
  )
JOIN "info_type" AS "it"
  ON "it"."id" = "mi"."info_type_id"
JOIN "title" AS "t"
  ON "mc"."movie_id" = "t"."id"
  AND "mi"."movie_id" = "t"."id"
  AND "t"."production_year" > 2005
WHERE
  "ct"."kind" = 'production companies';
rollback;
