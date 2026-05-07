WITH `CommentStats` AS (
  SELECT
    `c`.`PostId` AS `PostId`,
    COUNT(*) AS `comment_count`,
    COUNT(DISTINCT `c`.`UserId`) AS `distinct_commenters`
  FROM `Comments` AS `c`
  GROUP BY
    `c`.`PostId`
)
SELECT
  `p`.`Id` AS `PostId`,
  `p`.`Title` AS `Title`,
  `p`.`Score` AS `Score`,
  `cs`.`comment_count` AS `comment_count`,
  `cs`.`distinct_commenters` AS `distinct_commenters`,
  `u`.`DisplayName` AS `OwnerDisplayName`
FROM `CommentStats` AS `cs`
JOIN `Posts` AS `p`
  ON `cs`.`PostId` = `p`.`Id`
LEFT JOIN `Users` AS `u`
  ON `p`.`OwnerUserId` = `u`.`Id`
WHERE
  `cs`.`comment_count` >= 3
ORDER BY
  `cs`.`distinct_commenters` DESC,
  `p`.`Score` DESC,
  `p`.`Id`
