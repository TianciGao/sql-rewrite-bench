SELECT `Posts`.`Id` `PostId`, `Posts`.`Title`, CASE WHEN `t0`.`outbound_count` IS NOT NULL THEN CAST(`t0`.`outbound_count` AS BIGINT) ELSE 0 END `outbound_count`, CASE WHEN `t2`.`inbound_count` IS NOT NULL THEN CAST(`t2`.`inbound_count` AS BIGINT) ELSE 0 END `inbound_count`, CASE WHEN `t0`.`outbound_count` IS NOT NULL THEN CAST(`t0`.`outbound_count` AS BIGINT) ELSE 0 END + CASE WHEN `t2`.`inbound_count` IS NOT NULL THEN CAST(`t2`.`inbound_count` AS BIGINT) ELSE 0 END `total_links`
FROM `Posts`
LEFT JOIN (SELECT `PostId`, COUNT(*) `outbound_count`
FROM `PostLinks`
GROUP BY `PostId`) `t0` ON `Posts`.`Id` = `t0`.`PostId`
LEFT JOIN (SELECT `RelatedPostId` `PostId`, COUNT(*) `inbound_count`
FROM `PostLinks`
GROUP BY `RelatedPostId`) `t2` ON `Posts`.`Id` = `t2`.`PostId`
WHERE CASE WHEN `t0`.`outbound_count` IS NOT NULL THEN CAST(`t0`.`outbound_count` AS BIGINT) ELSE 0 END + CASE WHEN `t2`.`inbound_count` IS NOT NULL THEN CAST(`t2`.`inbound_count` AS BIGINT) ELSE 0 END > 0
ORDER BY 5 DESC NULLS FIRST, `Posts`.`Id` NULLS LAST
