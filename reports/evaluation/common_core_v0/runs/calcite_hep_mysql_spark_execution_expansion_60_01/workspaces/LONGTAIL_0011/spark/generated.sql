SELECT `t0`.`Title`, `t0`.`CreationDate`, `t0`.`Score`, `t0`.`ViewCount`, `t0`.`OwnerDisplayName`
FROM (SELECT `Posts`.`Id`, `Posts`.`Title`, `Posts`.`CreationDate`, `Posts`.`Score`, `Posts`.`ViewCount`, `Users`.`DisplayName` `OwnerDisplayName`, DENSE_RANK() OVER (PARTITION BY `Posts`.`OwnerUserId` ORDER BY `Posts`.`Score` DESC NULLS FIRST) `PostRank`
FROM `Posts`
INNER JOIN `Users` ON `Posts`.`OwnerUserId` = `Users`.`Id`
WHERE `Posts`.`PostTypeId` = 1 AND `Posts`.`CreationDate` >= '2022-01-01') `t0`
INNER JOIN (SELECT `t2`.`OwnerDisplayName`, MAX(`t2`.`PostRank`) `MaxPostRank`
FROM (SELECT `Users0`.`DisplayName` `OwnerDisplayName`, DENSE_RANK() OVER (PARTITION BY `Posts0`.`OwnerUserId` ORDER BY `Posts0`.`Score` DESC NULLS FIRST) `PostRank`
FROM `Posts` `Posts0`
INNER JOIN `Users` `Users0` ON `Posts0`.`OwnerUserId` = `Users0`.`Id`
WHERE `Posts0`.`PostTypeId` = 1 AND `Posts0`.`CreationDate` >= '2022-01-01') `t2`
GROUP BY `t2`.`OwnerDisplayName`) `t3` ON `t0`.`OwnerDisplayName` = `t3`.`OwnerDisplayName`
WHERE `t0`.`PostRank` = `t3`.`MaxPostRank`
ORDER BY `t0`.`Score` DESC NULLS FIRST, `t0`.`ViewCount` DESC NULLS FIRST
