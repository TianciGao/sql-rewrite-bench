SELECT *
FROM `emp`
WHERE NOT EXISTS (SELECT `emp0`.`empno` AS `empno`, `emp0`.`ename` AS `ename`, `emp0`.`job` AS `job`, `emp0`.`mgr` AS `mgr`, `emp0`.`hiredate` AS `hiredate`, `emp0`.`sal` AS `sal`, `emp0`.`comm` AS `comm`, `emp0`.`deptno` AS `deptno`, `bonus`.`ename` AS `ename0`, `bonus`.`job` AS `job0`, `bonus`.`sal` AS `sal0`, `bonus`.`comm` AS `comm0`
FROM `emp` AS `emp0`
INNER JOIN `bonus` ON `emp0`.`sal` = `emp`.`sal` AND `bonus`.`job` = `emp`.`job`
WHERE `emp0`.`empno` <> `emp`.`empno`)
