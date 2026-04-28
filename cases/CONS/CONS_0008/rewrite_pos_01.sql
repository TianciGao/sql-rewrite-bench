SELECT e.t0a
FROM t0 e
JOIN (SELECT DISTINCT t1a FROM t1) d
  ON d.t1a = e.t0a
JOIN (SELECT DISTINCT t2b FROM t2) b
  ON b.t2b = e.t0b;
