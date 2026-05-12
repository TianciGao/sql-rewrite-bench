set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_longtail_002;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "posts"."id" AS "postid", "posts"."title", "posts"."score", "t0"."comment_count", "t0"."distinct_commenters", "users"."displayname" AS "ownerdisplayname"
FROM (SELECT "postid", COUNT(*) AS "comment_count", COUNT(DISTINCT "userid") AS "distinct_commenters"
FROM "comments"
GROUP BY "postid") AS "t0"
INNER JOIN "posts" ON "t0"."postid" = "posts"."id"
LEFT JOIN "users" ON "posts"."owneruserid" = "users"."id"
WHERE "t0"."comment_count" >= 3
ORDER BY "t0"."distinct_commenters" DESC, "posts"."score" DESC, "posts"."id";
rollback;
