SELECT dept, cnt
FROM (
  SELECT dept, COUNT(manager_id) AS cnt
  FROM employees_nulls
  GROUP BY dept
) grouped
WHERE cnt >= 2
ORDER BY dept;
