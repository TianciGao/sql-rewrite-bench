SELECT
  `table1`.`i` AS `i`,
  `table1`.`j` AS `j`
FROM `table1` AS `table1`
WHERE
  NOT `table1`.`j` IN (
    SELECT
      `table1`.`table2`.`i` AS `i`
    FROM `table2` AS `table2`
    WHERE
      `table1`.`i` = `table2`.`j`
  )
