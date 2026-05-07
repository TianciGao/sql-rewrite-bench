WITH `HistoryStats` AS (
  SELECT
    `ph`.`PostId` AS `PostId`,
    COUNT(*) AS `revision_count`,
    COUNT(DISTINCT `ph`.`UserId`) AS `distinct_editors`,
    MIN(`ph`.`CreationDate`) AS `first_revision_at`,
    MAX(`ph`.`CreationDate`) AS `last_revision_at`
  FROM `PostHistory` AS `ph`
  GROUP BY
    `ph`.`PostId`
)
SELECT
  `p`.`Id` AS `PostId`,
  `p`.`Title` AS `Title`,
  `hs`.`revision_count` AS `revision_count`,
  `hs`.`distinct_editors` AS `distinct_editors`,
  `hs`.`first_revision_at` AS `first_revision_at`,
  `hs`.`last_revision_at` AS `last_revision_at`,
  `p`.`Score` AS `Score`,
  `p`.`ViewCount` AS `ViewCount`
FROM `HistoryStats` AS `hs`
JOIN `Posts` AS `p`
  ON `hs`.`PostId` = `p`.`Id`
WHERE
  `hs`.`revision_count` >= 2
ORDER BY
  `hs`.`revision_count` DESC,
  `hs`.`last_revision_at` DESC,
  `p`.`Id`
