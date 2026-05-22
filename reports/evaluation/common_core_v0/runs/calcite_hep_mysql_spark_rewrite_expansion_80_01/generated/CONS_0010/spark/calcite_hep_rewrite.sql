SELECT *
FROM `emp`
WHERE NOT EXISTS (SELECT `emp0`.`empno` `empno`, `emp0`.`ename` `ename`, `emp0`.`job` `job`, `emp0`.`mgr` `mgr`, `emp0`.`hiredate` `hiredate`, `emp0`.`sal` `sal`, `emp0`.`comm` `comm`, `emp0`.`deptno` `deptno`, `bonus`.`ename` `ename0`, `bonus`.`job` `job0`, `bonus`.`sal` `sal0`, `bonus`.`comm` `comm0`
FROM `emp` `emp0`
INNER JOIN `bonus` ON `emp0`.`sal` = `emp`.`sal` AND `bonus`.`job` = `emp`.`job`
WHERE `emp0`.`empno` <> `emp`.`empno`)
