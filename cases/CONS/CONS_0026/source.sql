SELECT d.*, (
  SELECT COUNT(*)
  FROM emp
  WHERE emp.deptno = d.deptno
  GROUP BY emp.deptno
) AS num_dept_groups
FROM dept AS d;
