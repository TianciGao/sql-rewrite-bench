WITH "rankedposts" AS (
  SELECT
    "p"."title" AS "title",
    "p"."creationdate" AS "creationdate",
    "p"."score" AS "score",
    "p"."viewcount" AS "viewcount",
    "u"."displayname" AS "ownerdisplayname",
    DENSE_RANK() OVER (PARTITION BY "p"."owneruserid" ORDER BY "p"."score" DESC) AS "postrank"
  FROM "posts" AS "p"
  JOIN "users" AS "u"
    ON "p"."owneruserid" = "u"."id"
  WHERE
    "p"."creationdate" >= '2022-01-01' AND "p"."posttypeid" = 1
), "maxrank" AS (
  SELECT
    "rankedposts"."ownerdisplayname" AS "ownerdisplayname",
    MAX("rankedposts"."postrank") AS "maxpostrank"
  FROM "rankedposts" AS "rankedposts"
  GROUP BY
    "rankedposts"."ownerdisplayname"
)
SELECT
  "rp"."title" AS "title",
  "rp"."creationdate" AS "creationdate",
  "rp"."score" AS "score",
  "rp"."viewcount" AS "viewcount",
  "rp"."ownerdisplayname" AS "ownerdisplayname"
FROM "rankedposts" AS "rp"
JOIN "maxrank" AS "mr"
  ON "mr"."maxpostrank" = "rp"."postrank"
  AND "mr"."ownerdisplayname" = "rp"."ownerdisplayname"
ORDER BY
  "rp"."score" DESC,
  "rp"."viewcount" DESC
