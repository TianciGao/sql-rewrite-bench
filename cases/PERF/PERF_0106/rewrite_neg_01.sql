SELECT min(kt.kind) AS movie_kind,
       min(t.title) AS complete_nerdy_internet_movie
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
JOIN movie_companies AS mc
  ON mc.movie_id = t.id
JOIN company_name AS cn
  ON cn.id = mc.company_id
JOIN company_type AS ct
  ON ct.id = mc.company_type_id
JOIN complete_cast AS cc
  ON cc.movie_id = t.id
JOIN comp_cast_type AS cct1
  ON cct1.id = cc.status_id
WHERE cct1.kind = 'complete+verified'
  AND cn.country_code = '[us]'
  AND it1.info = 'release dates'
  AND k.keyword IN ('nerd')
  AND kt.kind IN ('movie')
  AND mi.note LIKE '%internet%'
  AND mi.info LIKE 'USA:% 200%'
  AND t.production_year > 2000
  AND mk.movie_id = mi.movie_id
  AND mk.movie_id = mc.movie_id
  AND mk.movie_id = cc.movie_id
  AND mi.movie_id = mc.movie_id
  AND mi.movie_id = cc.movie_id
  AND mc.movie_id = cc.movie_id;
