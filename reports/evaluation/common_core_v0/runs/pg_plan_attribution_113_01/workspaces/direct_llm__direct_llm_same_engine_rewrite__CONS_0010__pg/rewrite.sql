SELECT E1.*
FROM emp E1
WHERE NOT EXISTS (
  SELECT 1
  FROM emp E2
  JOIN bonus B
    ON E2.sal = E1.sal
   AND B.job = E1.job
  WHERE E2.empno <> E1.empno
);
