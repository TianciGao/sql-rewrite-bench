WITH `historystats` AS (
  SELECT
    `ph`.`postid` AS `postid`,
    COUNT(*) AS `revision_count`,
    COUNT(DISTINCT `ph`.`userid`) AS `distinct_editors`,
    MIN(`ph`.`creationdate`) AS `first_revision_at`,
    MAX(`ph`.`creationdate`) AS `last_revision_at`
  FROM `posthistory` AS `ph`
  GROUP BY
    `ph`.`postid`
)
SELECT
  `p`.`id` AS `postid`,
  `p`.`title` AS `title`,
  `hs`.`revision_count` AS `revision_count`,
  `hs`.`distinct_editors` AS `distinct_editors`,
  `hs`.`first_revision_at` AS `first_revision_at`,
  `hs`.`last_revision_at` AS `last_revision_at`,
  `p`.`score` AS `score`,
  `p`.`viewcount` AS `viewcount`
FROM `historystats` AS `hs`
JOIN `posts` AS `p`
  ON `hs`.`postid` = `p`.`id`
WHERE
  `hs`.`revision_count` >= 2
ORDER BY
  `hs`.`revision_count` DESC,
  `hs`.`last_revision_at` DESC,
  `p`.`id`
