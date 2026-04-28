SELECT
  SUM(sal) AS sum_sal,
  COUNT(DISTINCT CASE WHEN job = 'CLERK' THEN deptno ELSE NULL END) AS count_distinct_clerk,
  SUM(CASE WHEN deptno = 10 THEN sal END) AS sum_sal_d10,
  SUM(CASE WHEN deptno = 20 THEN sal ELSE 0 END) AS sum_sal_d20,
  SUM(CASE WHEN deptno = 30 THEN 1 ELSE 0 END) AS count_d30,
  COUNT(CASE WHEN deptno = 40 THEN 'x' END) AS count_d40,
  SUM(CASE WHEN deptno = 45 THEN 1 END) AS count_d45,
  SUM(CASE WHEN deptno = 50 THEN 1 ELSE NULL END) AS count_d50,
  SUM(CASE WHEN deptno = 60 THEN CAST(NULL AS DECIMAL(12,2)) END) AS sum_null_d60,
  SUM(CASE WHEN deptno = 70 THEN NULL ELSE 1 END) AS sum_null_d70,
  COUNT(CASE WHEN deptno = 20 THEN 1 END) AS count_d20
FROM emp;
