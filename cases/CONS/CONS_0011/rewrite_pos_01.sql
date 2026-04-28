SELECT e1.ename
FROM emp e1
WHERE EXISTS (
  SELECT 1
  FROM dept d
  WHERE NOT EXISTS (
    SELECT 1
    FROM bonus b
    WHERE b.ename = d.dname
      AND b.job = e1.job
  )
);
