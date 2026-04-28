SELECT e.t0a
FROM t0 e
WHERE EXISTS (
  SELECT 1
  FROM t1 d
  WHERE d.t1a = e.t0a
    AND d.t1b = e.t0b
)
AND EXISTS (
  SELECT 1
  FROM t2 b
  WHERE b.t2a = e.t0a
);
