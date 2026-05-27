WITH `RankedPosts` AS (
  SELECT
    `p`.`Title` AS `Title`,
    `p`.`CreationDate` AS `CreationDate`,
    `p`.`Score` AS `Score`,
    `p`.`ViewCount` AS `ViewCount`,
    `u`.`DisplayName` AS `OwnerDisplayName`,
    DENSE_RANK() OVER (PARTITION BY `p`.`OwnerUserId` ORDER BY `p`.`Score` DESC) AS `PostRank`
  FROM `Posts` AS `p`
  JOIN `Users` AS `u`
    ON `p`.`OwnerUserId` = `u`.`Id`
  WHERE
    `p`.`CreationDate` >= '2022-01-01' AND `p`.`PostTypeId` = 1
), `MaxRank` AS (
  SELECT
    `RankedPosts`.`OwnerDisplayName` AS `OwnerDisplayName`,
    MAX(`RankedPosts`.`PostRank`) AS `MaxPostRank`
  FROM `RankedPosts` AS `RankedPosts`
  GROUP BY
    `RankedPosts`.`OwnerDisplayName`
)
SELECT
  `rp`.`Title` AS `Title`,
  `rp`.`CreationDate` AS `CreationDate`,
  `rp`.`Score` AS `Score`,
  `rp`.`ViewCount` AS `ViewCount`,
  `rp`.`OwnerDisplayName` AS `OwnerDisplayName`
FROM `RankedPosts` AS `rp`
JOIN `MaxRank` AS `mr`
  ON `mr`.`MaxPostRank` = `rp`.`PostRank`
  AND `mr`.`OwnerDisplayName` = `rp`.`OwnerDisplayName`
ORDER BY
  `rp`.`Score` DESC,
  `rp`.`ViewCount` DESC
