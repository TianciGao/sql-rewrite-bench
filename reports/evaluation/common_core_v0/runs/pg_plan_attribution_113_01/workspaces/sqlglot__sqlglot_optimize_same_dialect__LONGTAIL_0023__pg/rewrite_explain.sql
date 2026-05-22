set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_longtail_0023_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
WITH "outboundlinks" AS (
  SELECT
    "pl"."postid" AS "postid",
    COUNT(*) AS "outbound_count"
  FROM "postlinks" AS "pl"
  GROUP BY
    "pl"."postid"
), "inboundlinks" AS (
  SELECT
    "pl"."relatedpostid" AS "postid",
    COUNT(*) AS "inbound_count"
  FROM "postlinks" AS "pl"
  GROUP BY
    "pl"."relatedpostid"
)
SELECT
  "p"."id" AS "postid",
  "p"."title" AS "title",
  COALESCE("o"."outbound_count", 0) AS "outbound_count",
  COALESCE("i"."inbound_count", 0) AS "inbound_count",
  COALESCE("o"."outbound_count", 0) + COALESCE("i"."inbound_count", 0) AS "total_links"
FROM "posts" AS "p"
LEFT JOIN "outboundlinks" AS "o"
  ON "o"."postid" = "p"."id"
LEFT JOIN "inboundlinks" AS "i"
  ON "i"."postid" = "p"."id"
WHERE
  COALESCE("o"."outbound_count", 0) + COALESCE("i"."inbound_count", 0) > 0
ORDER BY
  "total_links" DESC,
  "p"."id";
rollback;
