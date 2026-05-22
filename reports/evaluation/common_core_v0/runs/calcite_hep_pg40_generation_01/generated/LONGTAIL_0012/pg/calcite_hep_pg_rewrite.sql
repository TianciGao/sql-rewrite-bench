SELECT "UserName", "TotalPosts", "TotalQuestions", "TotalAnswers", "LastPostTitle", "LastPostDate", "AvgUpVotes", "AvgDownVotes", "Reputation", "Views", ROW_NUMBER() OVER (ORDER BY "TotalPosts" DESC) AS "rank_value"
FROM (SELECT "Users"."DisplayName" AS "UserName", "Posts"."Title" AS "LastPostTitle", "Users"."Reputation", "Users"."Views", COUNT(DISTINCT "Posts"."Id") AS "TotalPosts", COALESCE(SUM(CASE WHEN "Posts"."PostTypeId" = 1 THEN 1 ELSE 0 END), 0) AS "TotalQuestions", COALESCE(SUM(CASE WHEN "Posts"."PostTypeId" = 2 THEN 1 ELSE 0 END), 0) AS "TotalAnswers", MAX("Posts"."CreationDate") AS "LastPostDate", CAST(COALESCE(SUM(CASE WHEN "t0"."UpVotes" IS NOT NULL THEN CAST("t0"."UpVotes" AS INTEGER) ELSE 0 END), 0) / COUNT(*) AS INTEGER) AS "AvgUpVotes", CAST(COALESCE(SUM(CASE WHEN "t0"."DownVotes" IS NOT NULL THEN CAST("t0"."DownVotes" AS INTEGER) ELSE 0 END), 0) / COUNT(*) AS INTEGER) AS "AvgDownVotes"
FROM "Users"
LEFT JOIN "Posts" ON "Users"."Id" = "Posts"."OwnerUserId"
LEFT JOIN (SELECT "PostId", COALESCE(SUM(CASE WHEN "VoteTypeId" = 2 THEN 1 ELSE 0 END), 0) AS "UpVotes", COALESCE(SUM(CASE WHEN "VoteTypeId" = 3 THEN 1 ELSE 0 END), 0) AS "DownVotes"
FROM "Votes"
GROUP BY "PostId") AS "t0" ON "Posts"."Id" = "t0"."PostId"
WHERE "Users"."Reputation" > 1000
GROUP BY "Users"."DisplayName", "Posts"."Title", "Users"."Reputation", "Users"."Views") AS "t4"
WHERE "t4"."TotalPosts" > 0
ORDER BY "TotalPosts" DESC, "LastPostDate" DESC
FETCH NEXT 10 ROWS ONLY
