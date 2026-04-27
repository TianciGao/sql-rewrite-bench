-- draft_id: JOB_DRAFT_0006
-- intended equivalence: explicit join normalization and layout cleanup only; no intended semantic change
-- not official case
-- Proposed positive rewrite: normalize old-style comma joins into explicit INNER JOINs while preserving the original filter semantics.
SELECT min(k.keyword) AS movie_keyword,
       min(n.name) AS actor_name,
       min(t.title) AS marvel_movie
FROM cast_info AS ci
JOIN movie_keyword AS mk ON ci.movie_id = mk.movie_id
JOIN keyword AS k ON k.id = mk.keyword_id
JOIN title AS t ON t.id = mk.movie_id AND t.id = ci.movie_id
CROSS JOIN name AS n
WHERE k.keyword = 'marvel-cinematic-universe'
  AND n.name LIKE '%Downey%Robert%'
  AND t.production_year > 2010
  AND n.id = ci.person_id;
;
