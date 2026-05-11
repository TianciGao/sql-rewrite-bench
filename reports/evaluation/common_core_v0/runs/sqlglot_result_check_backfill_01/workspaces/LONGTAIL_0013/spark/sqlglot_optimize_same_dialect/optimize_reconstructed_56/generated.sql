WITH `rankedposts` AS (
  SELECT
    `p`.`id` AS `postid`,
    `p`.`owneruserid` AS `owneruserid`,
    ROW_NUMBER() OVER (PARTITION BY `p`.`owneruserid` ORDER BY `p`.`score` DESC) AS `rank_value`
  FROM `posts` AS `p`
  WHERE
    `p`.`posttypeid` = 1
), `userstats` AS (
  SELECT
    `u`.`id` AS `userid`,
    COALESCE(SUM(`v`.`bountyamount`), 0) AS `totalbounty`,
    SUM(CASE WHEN `b`.`class` = 1 THEN 1 ELSE 0 END) AS `goldbadges`,
    COUNT(DISTINCT `p`.`id`) AS `questioncount`
  FROM `users` AS `u`
  LEFT JOIN `votes` AS `v`
    ON `u`.`id` = `v`.`userid` AND `v`.`votetypeid` IN (8, 9)
  LEFT JOIN `badges` AS `b`
    ON `b`.`userid` = `u`.`id`
  LEFT JOIN `posts` AS `p`
    ON `p`.`owneruserid` = `u`.`id` AND `p`.`posttypeid` = 1
  GROUP BY
    `u`.`id`,
    `u`.`displayname`
)
SELECT
  `u`.`displayname` AS `displayname`,
  COUNT(DISTINCT `p`.`id`) AS `answeredquestions`,
  COALESCE(AVG(`p`.`score`), 0) AS `avgscore`,
  `us`.`totalbounty` AS `totalbounty`,
  `us`.`goldbadges` AS `goldbadges`,
  `us`.`questioncount` AS `questioncount`,
  `bp`.`body` AS `bestpostcontent`
FROM `users` AS `u`
LEFT JOIN `posts` AS `p`
  ON `p`.`owneruserid` = `u`.`id` AND `p`.`posttypeid` = 2
LEFT JOIN `rankedposts` AS `rp`
  ON `rp`.`owneruserid` = `u`.`id` AND `rp`.`rank_value` = 1
LEFT JOIN `posts` AS `bp`
  ON `bp`.`id` = `rp`.`postid`
LEFT JOIN `userstats` AS `us`
  ON `u`.`id` = `us`.`userid`
WHERE
  `u`.`reputation` > 1000
GROUP BY
  `u`.`displayname`,
  `us`.`totalbounty`,
  `us`.`goldbadges`,
  `us`.`questioncount`,
  `bp`.`body`
HAVING
  COUNT(DISTINCT `p`.`id`) > 0
ORDER BY
  `avgscore` DESC,
  `totalbounty` DESC
