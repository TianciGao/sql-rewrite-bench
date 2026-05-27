SELECT t0a
FROM t0 e
WHERE EXISTS (
  SELECT *
  FROM t1 d
  WHERE d.t1a = e.t0a
)
AND EXISTS (
  SELECT *
  FROM t2 b
  WHERE b.t2b = e.t0b
);
