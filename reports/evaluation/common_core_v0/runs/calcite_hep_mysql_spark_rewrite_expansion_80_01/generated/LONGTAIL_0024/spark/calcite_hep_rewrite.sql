SELECT `Posts`.`Id` `PostId`, `Posts`.`Title`, `t0`.`revision_count`, `t0`.`distinct_editors`, `t0`.`first_revision_at`, `t0`.`last_revision_at`, `Posts`.`Score`, `Posts`.`ViewCount`
FROM (SELECT `PostId`, COUNT(*) `revision_count`, COUNT(DISTINCT `UserId`) `distinct_editors`, MIN(`CreationDate`) `first_revision_at`, MAX(`CreationDate`) `last_revision_at`
FROM `PostHistory`
GROUP BY `PostId`) `t0`
INNER JOIN `Posts` ON `t0`.`PostId` = `Posts`.`Id`
WHERE `t0`.`revision_count` >= 2
ORDER BY `t0`.`revision_count` DESC NULLS FIRST, `t0`.`last_revision_at` DESC NULLS FIRST, `Posts`.`Id` NULLS LAST
