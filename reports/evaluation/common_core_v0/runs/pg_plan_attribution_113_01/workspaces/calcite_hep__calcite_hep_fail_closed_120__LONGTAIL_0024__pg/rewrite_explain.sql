set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_longtail_002;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "posts"."id" AS "postid", "posts"."title", "t0"."revision_count", "t0"."distinct_editors", "t0"."first_revision_at", "t0"."last_revision_at", "posts"."score", "posts"."viewcount"
FROM (SELECT "postid", COUNT(*) AS "revision_count", COUNT(DISTINCT "userid") AS "distinct_editors", MIN("creationdate") AS "first_revision_at", MAX("creationdate") AS "last_revision_at"
FROM "posthistory"
GROUP BY "postid") AS "t0"
INNER JOIN "posts" ON "t0"."postid" = "posts"."id"
WHERE "t0"."revision_count" >= 2
ORDER BY "t0"."revision_count" DESC, "t0"."last_revision_at" DESC, "posts"."id";
rollback;
