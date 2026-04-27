SELECT min(cn.name) AS company_name,
       min(lt.link) AS link_type,
       min(t.title) AS german_follow_up
FROM title AS t
JOIN movie_link AS ml
  ON ml.movie_id = t.id
JOIN link_type AS lt
  ON lt.id = ml.link_type_id
JOIN movie_keyword AS mk
  ON mk.movie_id = t.id
JOIN keyword AS k
  ON k.id = mk.keyword_id
JOIN movie_companies AS mc
  ON mc.movie_id = t.id
JOIN company_type AS ct
  ON ct.id = mc.company_type_id
JOIN company_name AS cn
  ON cn.id = mc.company_id
JOIN movie_info AS mi
  ON mi.movie_id = t.id
WHERE cn.country_code != '[pl]'
  AND (cn.name LIKE '%Film%'
       OR cn.name LIKE '%Warner%')
  AND ct.kind ='production companies'
  AND k.keyword ='sequel'
  AND lt.link LIKE '%follow%'
  AND mc.note IS NULL
  AND mi.info IN ('Germany',
                  'German')
  AND t.production_year BETWEEN 2005 AND 2010
  AND ml.movie_id = mk.movie_id
  AND ml.movie_id = mc.movie_id
  AND mk.movie_id = mc.movie_id
  AND ml.movie_id = mi.movie_id
  AND mk.movie_id = mi.movie_id
  AND mc.movie_id = mi.movie_id;
