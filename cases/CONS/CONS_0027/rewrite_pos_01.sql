SELECT e1.ename
FROM emp e1
WHERE EXISTS (SELECT 1 FROM dept d)
  AND EXISTS (SELECT 1 FROM bonus b)
  AND (
    EXISTS (SELECT 1 FROM dept d WHERE d.loc = 'NEW YORK')
    OR EXISTS (SELECT 1 FROM bonus b WHERE b.job = e1.job)
  );
