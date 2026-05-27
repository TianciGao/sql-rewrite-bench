SELECT e1.ename
FROM emp e1
WHERE EXISTS (
  SELECT 1
  FROM dept d
  JOIN bonus b
    ON d.dname = b.ename
   AND b.job = e1.job
);
