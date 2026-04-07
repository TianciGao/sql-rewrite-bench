SELECT dept, COUNT(*) AS cnt
FROM employees_nulls
GROUP BY dept
HAVING COUNT(*) >= 2
ORDER BY dept;
