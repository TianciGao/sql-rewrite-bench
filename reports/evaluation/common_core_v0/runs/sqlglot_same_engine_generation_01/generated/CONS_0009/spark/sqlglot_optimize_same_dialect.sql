WITH `tmp` AS (
  SELECT
    `t1`.`t1c` AS `c`
  FROM `t1` AS `t1`
  WHERE
    `t1`.`t0a` = `t1`.`t1a`
  UNION ALL
  SELECT
    `t2`.`t2c` AS `c`
  FROM `t2` AS `t2`
  WHERE
    `t2`.`t0b` = `t2`.`t2b`
), `_u_0` AS (
  SELECT
    SUM(`tmp`.`c`) AS `_col_0`
  FROM `tmp` AS `tmp`
)
SELECT
  *
FROM `t0` AS `t0`
JOIN `_u_0` AS `_u_0`
  ON `_u_0`.`_col_0` > `t0`.`t0a`
