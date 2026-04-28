SELECT d.*, agg.emp_count AS num_dept_groups
FROM dept d
LEFT JOIN (
  SELECT deptno, COUNT(*) AS emp_count
  FROM emp
  GROUP BY deptno
) AS agg
  ON agg.deptno = d.deptno;
