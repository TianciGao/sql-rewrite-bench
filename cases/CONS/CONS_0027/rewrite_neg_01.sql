SELECT e1.ename
FROM emp e1
WHERE EXISTS (
  SELECT 1
  FROM dept d
  LEFT JOIN bonus b
    ON d.loc = 'NEW YORK' OR b.job = e1.job
);
