set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0011_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT E1.ENAME
FROM emp E1
WHERE EXISTS (
  SELECT 1
  FROM dept D
  LEFT JOIN bonus B
    ON D.DNAME = B.ENAME
   AND B.JOB = E1.JOB
  WHERE B.ENAME IS NULL
);
rollback;
