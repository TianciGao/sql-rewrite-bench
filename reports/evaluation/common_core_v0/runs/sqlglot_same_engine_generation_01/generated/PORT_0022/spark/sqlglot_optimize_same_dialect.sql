SELECT
  CAST(COUNT(`t1`.`id`) AS DOUBLE) / 12 AS `_col_0`
FROM `postlinks` AS `t1`
JOIN `posts` AS `t2`
  ON `t1`.`postid` = `t2`.`id` AND `t2`.`answercount` <= 2
WHERE
  DATE_FORMAT(CAST(`t1`.`creationdate` AS TIMESTAMP), '%yyyy') = '2010'
