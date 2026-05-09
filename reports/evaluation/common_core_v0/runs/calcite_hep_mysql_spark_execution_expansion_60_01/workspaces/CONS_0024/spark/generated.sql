SELECT `emp`.`empno`
FROM `emp`
LEFT JOIN `dept` ON `emp`.`deptno` = `dept`.`deptno` AND EXISTS (SELECT `deptno`, SUM(`sal`) `$f1`
FROM `emp`
WHERE `deptno` = `dept`.`deptno`
GROUP BY `deptno`
HAVING SUM(`sal`) > 1000000)
