WITH `commentstats` AS (
  SELECT
    `c`.`postid` AS `postid`,
    COUNT(*) AS `comment_count`,
    COUNT(DISTINCT `c`.`userid`) AS `distinct_commenters`
  FROM `comments` AS `c`
  GROUP BY
    `c`.`postid`
)
SELECT
  `p`.`id` AS `postid`,
  `p`.`title` AS `title`,
  `p`.`score` AS `score`,
  `cs`.`comment_count` AS `comment_count`,
  `cs`.`distinct_commenters` AS `distinct_commenters`,
  `u`.`displayname` AS `ownerdisplayname`
FROM `commentstats` AS `cs`
JOIN `posts` AS `p`
  ON `cs`.`postid` = `p`.`id`
LEFT JOIN `users` AS `u`
  ON `p`.`owneruserid` = `u`.`id`
WHERE
  `cs`.`comment_count` >= 3
ORDER BY
  `cs`.`distinct_commenters` DESC,
  `p`.`score` DESC,
  `p`.`id`
