SELECT
  `E1`.*
FROM `emp` AS `E1`
WHERE
  NOT EXISTS(
    SELECT
      1 AS `1`
    FROM `emp` AS `E2`
    JOIN `bonus` AS `B`
      ON `B`.`JOB` = `E1`.`JOB` AND `E1`.`SAL` = `E2`.`SAL`
    WHERE
      `E1`.`EMPNO` <> `E2`.`EMPNO`
  )
