SELECT E1.ENAME
FROM emp E1
WHERE EXISTS (
  SELECT 1
  FROM dept D
  LEFT JOIN bonus B
    ON D.dname = B.ename
   AND B.job = E1.job
  WHERE B.ename IS NULL
);
