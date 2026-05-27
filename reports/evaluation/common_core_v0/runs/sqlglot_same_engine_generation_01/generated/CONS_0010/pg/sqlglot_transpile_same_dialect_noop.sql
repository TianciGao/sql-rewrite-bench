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
  )
