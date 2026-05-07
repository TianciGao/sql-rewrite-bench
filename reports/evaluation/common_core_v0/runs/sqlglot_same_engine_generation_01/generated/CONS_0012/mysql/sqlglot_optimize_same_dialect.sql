SELECT
  *
FROM `dept` AS `d`
WHERE
  EXISTS(
    SELECT
      *
    FROM `emp` AS `e`
    WHERE
      `d`.`deptno` = `e`.`deptno`
    LIMIT 1
    OFFSET 2
  )
