set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0009_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM t0
WHERE t0a < (
  SELECT SUM(c)
  FROM (
    SELECT t1c AS c
    FROM t1
    WHERE t1a = t0a
    UNION ALL
    SELECT t2c AS c
    FROM t2
    WHERE t2b = t0b
  ) AS tmp
);
rollback;
