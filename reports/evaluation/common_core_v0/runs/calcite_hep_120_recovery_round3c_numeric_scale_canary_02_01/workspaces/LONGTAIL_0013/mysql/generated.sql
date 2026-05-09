SELECT `DisplayName`, `AnsweredQuestions`, CAST(CASE WHEN `$f6` IS NOT NULL THEN `$f6` ELSE 0 END AS DECIMAL(18, 4)) AS `AvgScore`, `TotalBounty`, `GoldBadges`, `QuestionCount`, `BestPostContent`
FROM (SELECT `Users`.`DisplayName`, `t4`.`TotalBounty`, `t4`.`GoldBadges`, `t4`.`QuestionCount`, `Posts1`.`Body` AS `BestPostContent`, COUNT(DISTINCT `Posts`.`Id`) AS `AnsweredQuestions`, AVG(`Posts`.`Score`) AS `$f6`
FROM `Users`
LEFT JOIN `Posts` ON `Users`.`Id` = `Posts`.`OwnerUserId` AND `Posts`.`PostTypeId` = 2
LEFT JOIN (SELECT `Id` AS `PostId`, `Title`, `OwnerUserId`, `CreationDate`, `Score`, ROW_NUMBER() OVER (PARTITION BY `OwnerUserId` ORDER BY `Score` IS NULL DESC, `Score` DESC) AS `rank_value`
FROM `Posts`
WHERE `PostTypeId` = 1) AS `t0` ON `Users`.`Id` = `t0`.`OwnerUserId` AND `t0`.`rank_value` = 1
LEFT JOIN `Posts` AS `Posts1` ON `t0`.`PostId` = `Posts1`.`Id`
LEFT JOIN (SELECT `Users0`.`Id` AS `UserId`, `Users0`.`DisplayName`, CASE WHEN CASE WHEN COUNT(`Votes`.`BountyAmount`) = 0 THEN NULL ELSE COALESCE(SUM(`Votes`.`BountyAmount`), 0) END IS NOT NULL THEN CAST(CASE WHEN COUNT(`Votes`.`BountyAmount`) = 0 THEN NULL ELSE COALESCE(SUM(`Votes`.`BountyAmount`), 0) END AS SIGNED) ELSE 0 END AS `TotalBounty`, COALESCE(SUM(CASE WHEN `Badges`.`Class` = 1 THEN 1 ELSE 0 END), 0) AS `GoldBadges`, COUNT(DISTINCT `Posts2`.`Id`) AS `QuestionCount`
FROM `Users` AS `Users0`
LEFT JOIN `Votes` ON `Users0`.`Id` = `Votes`.`UserId` AND `Votes`.`VoteTypeId` IN (8, 9)
LEFT JOIN `Badges` ON `Users0`.`Id` = `Badges`.`UserId`
LEFT JOIN `Posts` AS `Posts2` ON `Users0`.`Id` = `Posts2`.`OwnerUserId` AND `Posts2`.`PostTypeId` = 1
GROUP BY `Users0`.`Id`, `Users0`.`DisplayName`) AS `t4` ON `Users`.`Id` = `t4`.`UserId`
WHERE `Users`.`Reputation` > 1000
GROUP BY `Users`.`DisplayName`, `t4`.`TotalBounty`, `t4`.`GoldBadges`, `t4`.`QuestionCount`, `Posts1`.`Body`) AS `t9`
WHERE `t9`.`AnsweredQuestions` > 0
ORDER BY `AvgScore` IS NULL DESC, `AvgScore` DESC, `TotalBounty` IS NULL DESC, `TotalBounty` DESC;
