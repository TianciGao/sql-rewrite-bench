SELECT
  MIN(mi.info) AS movie_budget,
  MIN(mi_idx.info) AS movie_votes,
  MIN(n.name) AS writer,
  MIN(t.title) AS complete_gore_movie
FROM title AS t
JOIN movie_info AS mi
  ON mi.movie_id = t.id
JOIN info_type AS it1
  ON it1.id = mi.info_type_id
JOIN movie_info_idx AS mi_idx
  ON mi_idx.movie_id = t.id
JOIN info_type AS it2
  ON it2.id = mi_idx.info_type_id
JOIN cast_info AS ci
  ON ci.movie_id = t.id
JOIN name AS n
  ON n.id = ci.person_id
JOIN movie_keyword AS mk
  ON mk.movie_id = t.id
JOIN keyword AS k
  ON k.id = mk.keyword_id
JOIN complete_cast AS cc
  ON cc.movie_id = t.id
JOIN comp_cast_type AS cct1
  ON cct1.id = cc.subject_id
JOIN comp_cast_type AS cct2
  ON cct2.id = cc.status_id
WHERE cct1.kind IN ('cast', 'crew')
  AND cct2.kind = 'complete+verified'
  AND ci.note IN ('(writer)', '(head writer)', '(written by)', '(story)', '(story editor)')
  AND it1.info = 'genres'
  AND it2.info = 'votes'
  AND k.keyword IN ('murder', 'violence', 'blood', 'gore', 'death', 'female-nudity', 'hospital')
  AND mi.info IN ('Horror', 'Thriller')
  AND n.gender = 'm'
  AND t.production_year > 2000
  AND (
    t.title LIKE '%Freddy%'
    OR t.title LIKE '%Jason%'
    OR t.title LIKE 'Saw%'
  );
