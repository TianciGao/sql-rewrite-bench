-- draft_id: JOB_DRAFT_0012
-- intended equivalence: explicit join normalization and layout cleanup only; no intended semantic change
-- not official case
-- Proposed positive rewrite: normalize old-style comma joins into explicit INNER JOINs while preserving the original filter semantics.
SELECT min(cn.name) AS movie_company,
       min(mi_idx.info) AS rating,
       min(t.title) AS drama_horror_movie
FROM company_name AS cn
JOIN movie_companies AS mc ON cn.id = mc.company_id
JOIN company_type AS ct ON ct.id = mc.company_type_id
JOIN movie_info AS mi ON mc.movie_id = mi.movie_id
JOIN info_type AS it1 ON mi.info_type_id = it1.id
JOIN movie_info_idx AS mi_idx ON mc.movie_id = mi_idx.movie_id
JOIN info_type AS it2 ON mi_idx.info_type_id = it2.id
JOIN title AS t ON t.id = mi.movie_id AND t.id = mi_idx.movie_id AND t.id = mc.movie_id
WHERE cn.country_code = '[us]'
  AND ct.kind = 'production companies'
  AND it1.info = 'genres'
  AND it2.info = 'rating'
  AND mi.info in ('Drama', 'Horror')
  AND mi_idx.info > '8.0'
  AND t.production_year BETWEEN 2005 AND 2008
  AND mi.movie_id = mi_idx.movie_id;
;
