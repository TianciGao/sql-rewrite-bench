SELECT `Posts`.`Id` `PostId`, `Posts`.`Title`, `Posts`.`Score`, `t0`.`comment_count`, `t0`.`distinct_commenters`, `Users`.`DisplayName` `OwnerDisplayName`
FROM (SELECT `PostId`, COUNT(*) `comment_count`, COUNT(DISTINCT `UserId`) `distinct_commenters`
FROM `Comments`
GROUP BY `PostId`) `t0`
INNER JOIN `Posts` ON `t0`.`PostId` = `Posts`.`Id`
LEFT JOIN `Users` ON `Posts`.`OwnerUserId` = `Users`.`Id`
WHERE `t0`.`comment_count` >= 3
ORDER BY `t0`.`distinct_commenters` DESC NULLS FIRST, `Posts`.`Score` DESC NULLS FIRST, `Posts`.`Id` NULLS LAST
