-- draft_id: JOB_DRAFT_0006
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: narrow a LIKE predicate to force divergence. This rewrite is intentionally semantically different from the source query.
SELECT min(k.keyword) AS movie_keyword,
       min(n.name) AS actor_name,
       min(t.title) AS marvel_movie
FROM cast_info AS ci
JOIN movie_keyword AS mk ON ci.movie_id = mk.movie_id
JOIN keyword AS k ON k.id = mk.keyword_id
JOIN title AS t ON t.id = mk.movie_id AND t.id = ci.movie_id
CROSS JOIN name AS n
WHERE k.keyword = 'marvel-cinematic-universe'
  AND n.name LIKE 'Downey%Robert%'
  AND t.production_year > 2010
  AND n.id = ci.person_id;
;
