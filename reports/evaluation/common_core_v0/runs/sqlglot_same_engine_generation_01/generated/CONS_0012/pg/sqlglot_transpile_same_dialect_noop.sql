SELECT
  *
FROM dept AS d
WHERE
  EXISTS(
    SELECT
      *
    FROM emp AS e
    WHERE
      e.deptno = d.deptno
    LIMIT 1
    OFFSET 2
  )
