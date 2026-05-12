set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_longtail_0012_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
WITH "votecount" AS (
  SELECT
    "votes"."postid" AS "postid",
    SUM(CASE WHEN "votes"."votetypeid" = 2 THEN 1 ELSE 0 END) AS "upvotes",
    SUM(CASE WHEN "votes"."votetypeid" = 3 THEN 1 ELSE 0 END) AS "downvotes"
  FROM "votes" AS "votes"
  GROUP BY
    "votes"."postid"
)
SELECT
  "u"."displayname" AS "username",
  COUNT(DISTINCT "p"."id") AS "totalposts",
  SUM(CASE WHEN "p"."posttypeid" = 1 THEN 1 ELSE 0 END) AS "totalquestions",
  SUM(CASE WHEN "p"."posttypeid" = 2 THEN 1 ELSE 0 END) AS "totalanswers",
  "p"."title" AS "lastposttitle",
  MAX("p"."creationdate") AS "lastpostdate",
  AVG(COALESCE("votecount"."upvotes", 0)) AS "avgupvotes",
  AVG(COALESCE("votecount"."downvotes", 0)) AS "avgdownvotes",
  "u"."reputation" AS "reputation",
  "u"."views" AS "views",
  ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT "p"."id") DESC) AS "rank_value"
FROM "users" AS "u"
LEFT JOIN "posts" AS "p"
  ON "p"."owneruserid" = "u"."id"
LEFT JOIN "votecount" AS "votecount"
  ON "p"."id" = "votecount"."postid"
WHERE
  "u"."reputation" > 1000
GROUP BY
  "u"."displayname",
  "p"."title",
  "u"."reputation",
  "u"."views"
HAVING
  COUNT(DISTINCT "p"."id") > 0
ORDER BY
  "totalposts" DESC,
  "lastpostdate" DESC
LIMIT 10;
rollback;
