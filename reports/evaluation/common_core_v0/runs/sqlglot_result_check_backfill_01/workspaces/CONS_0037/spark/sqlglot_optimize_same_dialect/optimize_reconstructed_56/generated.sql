SELECT
  `emp`.`deptno` AS `deptno`,
  COUNT(DISTINCT `dept`.`name`) AS `_col_1`
FROM `emp` AS `emp`
LEFT JOIN `dept` AS `dept`
  ON `dept`.`deptno` = `emp`.`deptno`
GROUP BY
  `emp`.`deptno`
