SELECT d.*, agg.job_count AS num_dept_groups
FROM dept d
LEFT JOIN (
  SELECT deptno, COUNT(DISTINCT job) AS job_count
  FROM emp
  GROUP BY deptno
) AS agg
  ON agg.deptno = d.deptno;
