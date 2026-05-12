SELECT "username", "totalposts", "totalquestions", "totalanswers", "lastposttitle", "lastpostdate", "avgupvotes", "avgdownvotes", "reputation", "views", ROW_NUMBER() OVER (ORDER BY "totalposts" DESC) AS "rank_value"
FROM (SELECT "users"."displayname" AS "username", "posts"."title" AS "lastposttitle", "users"."reputation", "users"."views", COUNT(DISTINCT "posts"."id") AS "totalposts", COALESCE(SUM(CASE WHEN "posts"."posttypeid" = 1 THEN 1 ELSE 0 END), 0) AS "totalquestions", COALESCE(SUM(CASE WHEN "posts"."posttypeid" = 2 THEN 1 ELSE 0 END), 0) AS "totalanswers", MAX("posts"."creationdate") AS "lastpostdate", AVG(CASE WHEN "t0"."upvotes" IS NOT NULL THEN CAST("t0"."upvotes" AS INTEGER) ELSE 0 END) AS "avgupvotes", AVG(CASE WHEN "t0"."downvotes" IS NOT NULL THEN CAST("t0"."downvotes" AS INTEGER) ELSE 0 END) AS "avgdownvotes"
FROM "users"
LEFT JOIN "posts" ON "users"."id" = "posts"."owneruserid"
LEFT JOIN (SELECT "postid", COALESCE(SUM(CASE WHEN "votetypeid" = 2 THEN 1 ELSE 0 END), 0) AS "upvotes", COALESCE(SUM(CASE WHEN "votetypeid" = 3 THEN 1 ELSE 0 END), 0) AS "downvotes"
FROM "votes"
GROUP BY "postid") AS "t0" ON "posts"."id" = "t0"."postid"
WHERE "users"."reputation" > 1000
GROUP BY "users"."displayname", "posts"."title", "users"."reputation", "users"."views") AS "t4"
WHERE "t4"."totalposts" > 0
ORDER BY "totalposts" DESC, "lastpostdate" DESC
FETCH NEXT 10 ROWS ONLY
