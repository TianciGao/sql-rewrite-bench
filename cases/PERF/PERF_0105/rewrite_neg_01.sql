SELECT min(cn.name) AS movie_company,
       min(mi_idx.info) AS rating,
       min(t.title) AS western_violent_movie
FROM title AS t
JOIN kind_type AS kt
  ON kt.id = t.kind_id
JOIN movie_info AS mi
  ON mi.movie_id = t.id
JOIN info_type AS it1
  ON it1.id = mi.info_type_id
JOIN movie_keyword AS mk
  ON mk.movie_id = t.id
JOIN keyword AS k
  ON k.id = mk.keyword_id
JOIN movie_info_idx AS mi_idx
  ON mi_idx.movie_id = t.id
JOIN info_type AS it2
  ON it2.id = mi_idx.info_type_id
JOIN movie_companies AS mc
  ON mc.movie_id = t.id
JOIN company_type AS ct
  ON ct.id = mc.company_type_id
JOIN company_name AS cn
  ON cn.id = mc.company_id
WHERE cn.country_code != '[us]'
  AND it1.info = 'countries'
  AND it2.info = 'rating'
  AND k.keyword IN ('murder',
                    'murder-in-title')
  AND kt.kind IN ('movie',
                  'episode')
  AND mc.note NOT LIKE '%(USA)%'
  AND mc.note LIKE '%(200%)%'
  AND mi.info IN ('Sweden',
                  'Norway',
                  'Germany',
                  'Denmark',
                  'Swedish',
                  'Danish',
                  'Norwegian',
                  'German',
                  'USA',
                  'American')
  AND mi_idx.info < '8.5'
  AND t.production_year > 2005
  AND mk.movie_id = mi.movie_id
  AND mk.movie_id = mi_idx.movie_id
  AND mk.movie_id = mc.movie_id
  AND mi.movie_id = mi_idx.movie_id
  AND mi.movie_id = mc.movie_id
  AND mc.movie_id = mi_idx.movie_id;
