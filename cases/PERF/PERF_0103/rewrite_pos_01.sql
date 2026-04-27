SELECT min(mi.info) AS movie_budget,
       min(mi_idx.info) AS movie_votes,
       min(t.title) AS movie_title
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
WHERE ci.note IN ('(producer)',
                  '(executive producer)')
  AND it1.info = 'budget'
  AND it2.info = 'votes'
  AND n.gender = 'm'
  AND n.name LIKE '%Tim%'
  AND ci.movie_id = mi.movie_id
  AND ci.movie_id = mi_idx.movie_id
  AND mi.movie_id = mi_idx.movie_id;
