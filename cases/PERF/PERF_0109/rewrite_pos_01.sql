SELECT min(mi.info) AS movie_budget,
       min(mi_idx.info) AS movie_votes,
       min(n.name) AS writer,
       min(t.title) AS violent_liongate_movie
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
JOIN movie_companies AS mc
  ON mc.movie_id = t.id
JOIN company_name AS cn
  ON cn.id = mc.company_id
WHERE ci.note IN ('(writer)',
                  '(head writer)',
                  '(written by)',
                  '(story)',
                  '(story editor)')
  AND cn.name LIKE 'Lionsgate%'
  AND it1.info = 'genres'
  AND it2.info = 'votes'
  AND k.keyword IN ('murder',
                    'violence',
                    'blood',
                    'gore',
                    'death',
                    'female-nudity',
                    'hospital')
  AND mi.info IN ('Horror',
                  'Action',
                  'Sci-Fi',
                  'Thriller',
                  'Crime',
                  'War')
  AND ci.movie_id = mi.movie_id
  AND ci.movie_id = mi_idx.movie_id
  AND ci.movie_id = mk.movie_id
  AND ci.movie_id = mc.movie_id
  AND mi.movie_id = mi_idx.movie_id
  AND mi.movie_id = mk.movie_id
  AND mi.movie_id = mc.movie_id
  AND mi_idx.movie_id = mk.movie_id
  AND mi_idx.movie_id = mc.movie_id
  AND mk.movie_id = mc.movie_id;
