set search_path to attr24_sqlglot__sqlglot_optimize_same_dialect__cons_0010__pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT E1.*
FROM emp E1
WHERE NOT EXISTS (
  SELECT 1
  FROM emp E2
  JOIN bonus B
    ON E2.SAL = E1.SAL
   AND B.JOB = E1.JOB
  WHERE E2.EMPNO <> E1.EMPNO
);
rollback;
