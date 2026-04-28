SELECT d.*, (
  SELECT COUNT(*)
  FROM (
    SELECT empno, ename, job
    FROM emp
    WHERE emp.deptno = d.deptno
  ) AS sub
  GROUP BY deptno
) AS num_dept_groups
FROM dept AS d;
