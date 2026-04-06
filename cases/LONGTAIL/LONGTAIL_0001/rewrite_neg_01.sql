WITH ranked AS (
  SELECT
    dept,
    emp_id,
    emp_name,
    salary,
    ROW_NUMBER() OVER (
      PARTITION BY dept
      ORDER BY salary DESC, emp_id ASC
    ) AS rn
  FROM employees
)
SELECT dept, emp_name, salary
FROM ranked
WHERE rn = 1
ORDER BY dept, salary DESC, emp_name ASC;
