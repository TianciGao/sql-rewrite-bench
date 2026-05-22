SELECT
  `E1`.`ENAME` AS `ENAME`
FROM `emp` AS `E1`
WHERE
  EXISTS(
    SELECT
      1 AS `1`
    FROM `dept` AS `D`
    LEFT JOIN `bonus` AS `B`
      ON `B`.`ENAME` = `D`.`DNAME` AND `B`.`JOB` = `E1`.`JOB`
    WHERE
      `B`.`ENAME` IS NULL
  )
