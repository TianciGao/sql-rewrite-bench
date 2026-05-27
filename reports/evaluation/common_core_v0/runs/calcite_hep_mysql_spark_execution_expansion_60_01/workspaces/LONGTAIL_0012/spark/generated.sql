SELECT `UserName`, `TotalPosts`, `TotalQuestions`, `TotalAnswers`, `LastPostTitle`, `LastPostDate`, `AvgUpVotes`, `AvgDownVotes`, `Reputation`, `Views`, ROW_NUMBER() OVER (ORDER BY `TotalPosts` DESC NULLS FIRST) `rank_value`
FROM (SELECT `Users`.`DisplayName` `UserName`, `Posts`.`Title` `LastPostTitle`, `Users`.`Reputation`, `Users`.`Views`, COUNT(DISTINCT `Posts`.`Id`) `TotalPosts`, COALESCE(SUM(CASE WHEN `Posts`.`PostTypeId` = 1 THEN 1 ELSE 0 END), 0) `TotalQuestions`, COALESCE(SUM(CASE WHEN `Posts`.`PostTypeId` = 2 THEN 1 ELSE 0 END), 0) `TotalAnswers`, MAX(`Posts`.`CreationDate`) `LastPostDate`, CAST(COALESCE(SUM(CASE WHEN `t0`.`UpVotes` IS NOT NULL THEN CAST(`t0`.`UpVotes` AS INTEGER) ELSE 0 END), 0) / COUNT(*) AS INTEGER) `AvgUpVotes`, CAST(COALESCE(SUM(CASE WHEN `t0`.`DownVotes` IS NOT NULL THEN CAST(`t0`.`DownVotes` AS INTEGER) ELSE 0 END), 0) / COUNT(*) AS INTEGER) `AvgDownVotes`
FROM `Users`
LEFT JOIN `Posts` ON `Users`.`Id` = `Posts`.`OwnerUserId`
LEFT JOIN (SELECT `PostId`, COALESCE(SUM(CASE WHEN `VoteTypeId` = 2 THEN 1 ELSE 0 END), 0) `UpVotes`, COALESCE(SUM(CASE WHEN `VoteTypeId` = 3 THEN 1 ELSE 0 END), 0) `DownVotes`
FROM `Votes`
GROUP BY `PostId`) `t0` ON `Posts`.`Id` = `t0`.`PostId`
WHERE `Users`.`Reputation` > 1000
GROUP BY `Users`.`DisplayName`, `Posts`.`Title`, `Users`.`Reputation`, `Users`.`Views`) `t4`
WHERE `t4`.`TotalPosts` > 0
ORDER BY `TotalPosts` DESC NULLS FIRST, `LastPostDate` DESC NULLS FIRST
LIMIT 10
