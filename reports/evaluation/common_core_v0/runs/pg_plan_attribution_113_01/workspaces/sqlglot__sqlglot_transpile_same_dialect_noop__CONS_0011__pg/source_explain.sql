set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_cons_001;
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
