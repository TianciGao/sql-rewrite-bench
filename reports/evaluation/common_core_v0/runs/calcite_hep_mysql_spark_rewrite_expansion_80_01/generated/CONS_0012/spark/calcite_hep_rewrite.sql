SELECT *
FROM `dept`
WHERE EXISTS (SELECT `empno`, `ename`, `job`, `mgr`, `hiredate`, `sal`, `comm`, `deptno`
FROM `emp`
WHERE `deptno` = `dept`.`deptno`
LIMIT 1
OFFSET 2)
