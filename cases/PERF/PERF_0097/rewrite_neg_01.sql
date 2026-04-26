SELECT min(cn1.name) AS first_company,
       min(cn2.name) AS second_company,
       min(mi_idx1.info) AS first_rating,
       min(mi_idx2.info) AS second_rating,
       min(t1.title) AS first_movie,
       min(t2.title) AS second_movie
FROM link_type AS lt
JOIN movie_link AS ml
  ON lt.id = ml.link_type_id
JOIN title AS t1
  ON t1.id = ml.movie_id
JOIN title AS t2
  ON t2.id = ml.linked_movie_id
JOIN movie_info_idx AS mi_idx1
  ON t1.id = mi_idx1.movie_id
 AND ml.movie_id = mi_idx1.movie_id
JOIN info_type AS it1
  ON it1.id = mi_idx1.info_type_id
JOIN kind_type AS kt1
  ON kt1.id = t1.kind_id
JOIN movie_companies AS mc1
  ON t1.id = mc1.movie_id
 AND ml.movie_id = mc1.movie_id
 AND mi_idx1.movie_id = mc1.movie_id
JOIN company_name AS cn1
  ON cn1.id = mc1.company_id
JOIN movie_info_idx AS mi_idx2
  ON t2.id = mi_idx2.movie_id
 AND ml.linked_movie_id = mi_idx2.movie_id
JOIN info_type AS it2
  ON it2.id = mi_idx2.info_type_id
JOIN kind_type AS kt2
  ON kt2.id = t2.kind_id
JOIN movie_companies AS mc2
  ON t2.id = mc2.movie_id
 AND ml.linked_movie_id = mc2.movie_id
 AND mi_idx2.movie_id = mc2.movie_id
JOIN company_name AS cn2
  ON cn2.id = mc2.company_id
WHERE cn1.country_code = '[us]'
  AND it1.info = 'rating'
  AND it2.info = 'rating'
  AND kt1.kind in ('tv series')
  AND kt2.kind in ('tv series')
  AND lt.link = 'sequel'
  AND mi_idx2.info < '3.0'
  AND t2.production_year BETWEEN 2005 AND 2008;
