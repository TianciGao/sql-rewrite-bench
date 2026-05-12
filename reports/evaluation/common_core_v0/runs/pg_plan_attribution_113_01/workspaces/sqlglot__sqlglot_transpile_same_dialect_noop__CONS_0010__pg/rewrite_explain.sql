set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_cons_001;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  E1.*
FROM emp AS E1
WHERE
  NOT EXISTS(
    SELECT
      1
    FROM emp AS E2
    JOIN bonus AS B
      ON E2.SAL = E1.SAL AND B.JOB = E1.JOB
    WHERE
      E2.EMPNO <> E1.EMPNO
  );
rollback;
