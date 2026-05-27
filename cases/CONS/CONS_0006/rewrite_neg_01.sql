SELECT
  SUM(f.sal) AS sum_sal,
  (SELECT COUNT(DISTINCT deptno) FROM emp WHERE job = 'CLERK') AS count_distinct_clerk,
  SUM(f.sal_d10) AS sum_sal_d10,
  SUM(f.sal_d20) AS sum_sal_d20,
  SUM(f.cnt_d30) AS count_d30,
  SUM(f.cnt_d40) AS count_d40,
  SUM(f.cnt_d45) AS count_d45,
  SUM(f.cnt_d50) AS count_d50,
  SUM(f.sum_null_d60) AS sum_null_d60,
  SUM(f.sum_null_d70) AS sum_null_d70,
  SUM(f.cnt_d20) AS count_d20
FROM (
  SELECT
    sal,
    CASE WHEN deptno = 10 THEN sal ELSE NULL END AS sal_d10,
    CASE WHEN deptno = 20 THEN sal ELSE 0 END AS sal_d20,
    CASE WHEN deptno = 20 THEN 1 ELSE 0 END AS cnt_d30,
    CASE WHEN deptno = 40 THEN 1 ELSE 0 END AS cnt_d40,
    CASE WHEN deptno = 45 THEN 1 ELSE NULL END AS cnt_d45,
    CASE WHEN deptno = 50 THEN 1 ELSE NULL END AS cnt_d50,
    CASE WHEN deptno = 60 THEN CAST(NULL AS DECIMAL(12,2)) ELSE CAST(NULL AS DECIMAL(12,2)) END AS sum_null_d60,
    CASE WHEN deptno = 70 THEN NULL ELSE 1 END AS sum_null_d70,
    CASE WHEN deptno = 20 THEN 1 ELSE NULL END AS cnt_d20
  FROM emp
) AS f;
