SELECT `DisplayName`, `AnsweredQuestions`, CASE WHEN `$f6` IS NOT NULL THEN CAST(`$f6` AS INTEGER) ELSE 0 END `AvgScore`, `TotalBounty`, `GoldBadges`, `QuestionCount`, `BestPostContent`
FROM (SELECT `Users`.`DisplayName`, `t4`.`TotalBounty`, `t4`.`GoldBadges`, `t4`.`QuestionCount`, `Posts1`.`Body` `BestPostContent`, COUNT(DISTINCT `Posts`.`Id`) `AnsweredQuestions`, CAST(CASE WHEN COUNT(`Posts`.`Score`) = 0 THEN NULL ELSE COALESCE(SUM(`Posts`.`Score`), 0) END / COUNT(`Posts`.`Score`) AS INTEGER) `$f6`
FROM `Users`
LEFT JOIN `Posts` ON `Users`.`Id` = `Posts`.`OwnerUserId` AND `Posts`.`PostTypeId` = 2
LEFT JOIN (SELECT `Id` `PostId`, `Title`, `OwnerUserId`, `CreationDate`, `Score`, ROW_NUMBER() OVER (PARTITION BY `OwnerUserId` ORDER BY `Score` DESC NULLS FIRST) `rank_value`
FROM `Posts`
WHERE `PostTypeId` = 1) `t0` ON `Users`.`Id` = `t0`.`OwnerUserId` AND `t0`.`rank_value` = 1
LEFT JOIN `Posts` `Posts1` ON `t0`.`PostId` = `Posts1`.`Id`
LEFT JOIN (SELECT `Users0`.`Id` `UserId`, `Users0`.`DisplayName`, CASE WHEN CASE WHEN COUNT(`Votes`.`BountyAmount`) = 0 THEN NULL ELSE COALESCE(SUM(`Votes`.`BountyAmount`), 0) END IS NOT NULL THEN CAST(CASE WHEN COUNT(`Votes`.`BountyAmount`) = 0 THEN NULL ELSE COALESCE(SUM(`Votes`.`BountyAmount`), 0) END AS INTEGER) ELSE 0 END `TotalBounty`, COALESCE(SUM(CASE WHEN `Badges`.`Class` = 1 THEN 1 ELSE 0 END), 0) `GoldBadges`, COUNT(DISTINCT `Posts2`.`Id`) `QuestionCount`
FROM `Users` `Users0`
LEFT JOIN `Votes` ON `Users0`.`Id` = `Votes`.`UserId` AND `Votes`.`VoteTypeId` IN (8, 9)
LEFT JOIN `Badges` ON `Users0`.`Id` = `Badges`.`UserId`
LEFT JOIN `Posts` `Posts2` ON `Users0`.`Id` = `Posts2`.`OwnerUserId` AND `Posts2`.`PostTypeId` = 1
GROUP BY `Users0`.`Id`, `Users0`.`DisplayName`) `t4` ON `Users`.`Id` = `t4`.`UserId`
WHERE `Users`.`Reputation` > 1000
GROUP BY `Users`.`DisplayName`, `t4`.`TotalBounty`, `t4`.`GoldBadges`, `t4`.`QuestionCount`, `Posts1`.`Body`) `t9`
WHERE `t9`.`AnsweredQuestions` > 0
ORDER BY 3 DESC NULLS FIRST, `TotalBounty` DESC NULLS FIRST
