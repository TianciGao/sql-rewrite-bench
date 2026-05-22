SELECT MIN("title"."title") AS "movie_title"
FROM "keyword",
"movie_info",
"movie_keyword",
"title"
WHERE "keyword"."keyword" LIKE '%sequel%' AND ((CAST("movie_info"."info" AS VARCHAR(9)) = 'Sweden' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Norway' OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Germany' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Denmark') OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Swedish' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'Denish' OR (CAST("movie_info"."info" AS VARCHAR(9)) = 'Norwegian' OR CAST("movie_info"."info" AS VARCHAR(9)) = 'German'))) AND "title"."production_year" > 2005) AND ("title"."id" = "movie_info"."movie_id" AND "title"."id" = "movie_keyword"."movie_id" AND ("movie_keyword"."movie_id" = "movie_info"."movie_id" AND "keyword"."id" = "movie_keyword"."keyword_id"))
