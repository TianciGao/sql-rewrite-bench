SELECT "displayname", "answeredquestions", CAST(CASE WHEN "$f6" IS NOT NULL THEN "$f6" ELSE 0 END AS DECIMAL(18, 4)) AS "avgscore", "totalbounty", "goldbadges", "questioncount", "bestpostcontent"
FROM (SELECT "users"."displayname", "t4"."totalbounty", "t4"."goldbadges", "t4"."questioncount", "posts1"."body" AS "bestpostcontent", COUNT(DISTINCT "posts"."id") AS "answeredquestions", AVG("posts"."score") AS "$f6"
FROM "users"
LEFT JOIN "posts" ON "users"."id" = "posts"."owneruserid" AND "posts"."posttypeid" = 2
LEFT JOIN (SELECT "id" AS "postid", "title", "owneruserid", "creationdate", "score", ROW_NUMBER() OVER (PARTITION BY "owneruserid" ORDER BY "score" DESC) AS "rank_value"
FROM "posts"
WHERE "posttypeid" = 1) AS "t0" ON "users"."id" = "t0"."owneruserid" AND "t0"."rank_value" = 1
LEFT JOIN "posts" AS "posts1" ON "t0"."postid" = "posts1"."id"
LEFT JOIN (SELECT "users0"."id" AS "userid", "users0"."displayname", CASE WHEN CASE WHEN COUNT("votes"."bountyamount") = 0 THEN NULL ELSE COALESCE(SUM("votes"."bountyamount"), 0) END IS NOT NULL THEN CAST(CASE WHEN COUNT("votes"."bountyamount") = 0 THEN NULL ELSE COALESCE(SUM("votes"."bountyamount"), 0) END AS INTEGER) ELSE 0 END AS "totalbounty", COALESCE(SUM(CASE WHEN "badges"."class" = 1 THEN 1 ELSE 0 END), 0) AS "goldbadges", COUNT(DISTINCT "posts2"."id") AS "questioncount"
FROM "users" AS "users0"
LEFT JOIN "votes" ON "users0"."id" = "votes"."userid" AND "votes"."votetypeid" IN (8, 9)
LEFT JOIN "badges" ON "users0"."id" = "badges"."userid"
LEFT JOIN "posts" AS "posts2" ON "users0"."id" = "posts2"."owneruserid" AND "posts2"."posttypeid" = 1
GROUP BY "users0"."id", "users0"."displayname") AS "t4" ON "users"."id" = "t4"."userid"
WHERE "users"."reputation" > 1000
GROUP BY "users"."displayname", "t4"."totalbounty", "t4"."goldbadges", "t4"."questioncount", "posts1"."body") AS "t9"
WHERE "t9"."answeredquestions" > 0
ORDER BY 3 DESC, "totalbounty" DESC;
