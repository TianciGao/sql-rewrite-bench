-- draft_id: JOB_DRAFT_0001
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: change one equality literal to a related but different value. This rewrite is intentionally semantically different from the source query.
SELECT min(mc.note) AS production_note,
       min(t.title) AS movie_title,
       min(t.production_year) AS movie_year
FROM company_type AS ct
JOIN movie_companies AS mc ON ct.id = mc.company_type_id
JOIN movie_info_idx AS mi_idx ON mc.movie_id = mi_idx.movie_id
JOIN title AS t ON t.id = mc.movie_id AND t.id = mi_idx.movie_id
CROSS JOIN info_type AS it
WHERE ct.kind = 'distributors'
  AND it.info = 'bottom 10 rank'
  AND mc.note not like '%(as Metro-Goldwyn-Mayer Pictures)%'
  AND t.production_year BETWEEN 2005 AND 2010
  AND it.id = mi_idx.info_type_id;
;
