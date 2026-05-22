SELECT `Posts`.`Id` AS `PostId`, `Posts`.`Title`, `t0`.`revision_count`, `t0`.`distinct_editors`, `t0`.`first_revision_at`, `t0`.`last_revision_at`, `Posts`.`Score`, `Posts`.`ViewCount`
FROM (SELECT `PostId`, COUNT(*) AS `revision_count`, COUNT(DISTINCT `UserId`) AS `distinct_editors`, MIN(`CreationDate`) AS `first_revision_at`, MAX(`CreationDate`) AS `last_revision_at`
FROM `PostHistory`
GROUP BY `PostId`) AS `t0`
INNER JOIN `Posts` ON `t0`.`PostId` = `Posts`.`Id`
WHERE `t0`.`revision_count` >= 2
ORDER BY `t0`.`revision_count` IS NULL DESC, `t0`.`revision_count` DESC, `t0`.`last_revision_at` IS NULL DESC, `t0`.`last_revision_at` DESC, `Posts`.`Id` IS NULL, `Posts`.`Id`
