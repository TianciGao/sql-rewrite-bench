SELECT `emp`.`empno`
FROM `emp`
LEFT JOIN `dept` ON `emp`.`deptno` = `dept`.`deptno` AND EXISTS (SELECT `deptno`, SUM(`sal`) AS `$f1`
FROM `emp`
WHERE `deptno` = `dept`.`deptno`
GROUP BY `deptno`
HAVING `$f1` > 1000000)
