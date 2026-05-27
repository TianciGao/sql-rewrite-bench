-- draft_id: JOB_DRAFT_0004
-- intended equivalence: explicit join normalization and layout cleanup only; no intended semantic change
-- not official case
-- Proposed positive rewrite: normalize old-style comma joins into explicit INNER JOINs while preserving the original filter semantics.
SELECT min(mi_idx.info) AS rating,
       min(t.title) AS movie_title
FROM info_type AS it
CROSS JOIN keyword AS k
JOIN movie_keyword AS mk ON k.id = mk.keyword_id
JOIN movie_info_idx AS mi_idx ON mk.movie_id = mi_idx.movie_id
JOIN title AS t ON t.id = mi_idx.movie_id AND t.id = mk.movie_id
WHERE it.info ='rating'
  AND k.keyword like '%sequel%'
  AND mi_idx.info > '5.0'
  AND t.production_year > 2005
  AND it.id = mi_idx.info_type_id;
;
