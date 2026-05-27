SELECT
  `t1`.`account_id` AS `account_id`
FROM `loan` AS `t1`
JOIN `account` AS `t2`
  ON `t1`.`account_id` = `t2`.`account_id`
  AND DATE_FORMAT(CAST(`t2`.`account_date` AS DATETIME), '%Y') = '1993'
WHERE
  `t1`.`duration` > 12
ORDER BY
  `t1`.`amount` DESC
LIMIT 1
