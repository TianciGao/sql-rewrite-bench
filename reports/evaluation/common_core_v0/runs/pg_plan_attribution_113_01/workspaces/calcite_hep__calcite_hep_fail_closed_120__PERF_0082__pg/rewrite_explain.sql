set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_perf_0082_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT MIN("title"."title") AS "typical_european_movie"
FROM "company_type",
"info_type",
"movie_companies",
"movie_info",
"title"
WHERE CAST("company_type"."kind" AS VARCHAR(20)) = 'production companies' AND "movie_companies"."note" LIKE '%(theatrical)%' AND ("movie_companies"."note" LIKE '%(France)%' AND ((CAST("movie_info"."info" AS VARCHAR(9)) = 'Sweden' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Norway' OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Germany' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Denmark') OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Swedish' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Denish' OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Norwegian' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'German'))) AND "title"."production_year" > 2005)) AND ("title"."id" = "movie_info"."movie_id" AND "title"."id" = "movie_companies"."movie_id" AND ("movie_companies"."movie_id" = "movie_info"."movie_id" AND ("company_type"."id" = "movie_companies"."company_type_id" AND "info_type"."id" = "movie_info"."info_type_id")));
rollback;
