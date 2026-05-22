SELECT i, j
FROM table1
WHERE j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
