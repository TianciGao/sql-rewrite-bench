SELECT
  *
FROM `tmp_emps` AS `e1`
WHERE
  EXISTS(
    SELECT
      `e2`.`deptno` AS `deptno`
    FROM `tmp_emps` AS `e2`
    WHERE
      `e1`.`deptno` <> `e2`.`deptno` AND `e2`.`commission` = `e2`.`e1`.`commission`
  )
