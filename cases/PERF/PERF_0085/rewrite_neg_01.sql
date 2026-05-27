-- draft_id: JOB_DRAFT_0007
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: narrow a LIKE predicate to force divergence. This rewrite is intentionally semantically different from the source query.
SELECT min(n.name) AS of_person,
       min(t.title) AS biography_movie
FROM aka_name AS an
JOIN cast_info AS ci ON an.person_id = ci.person_id
JOIN name AS n ON n.id = an.person_id AND ci.person_id = n.id
JOIN person_info AS pi ON n.id = pi.person_id AND pi.person_id = an.person_id AND pi.person_id = ci.person_id
JOIN info_type AS it ON it.id = pi.info_type_id
JOIN title AS t ON t.id = ci.movie_id
JOIN movie_link AS ml ON ml.linked_movie_id = t.id
JOIN link_type AS lt ON lt.id = ml.link_type_id
WHERE an.name LIKE '%a'
  AND it.info ='mini biography'
  AND lt.link ='features'
  AND n.name_pcode_cf BETWEEN 'A' AND 'F'
  AND (n.gender='m' OR (n.gender = 'f'
  AND n.name LIKE 'B%'))
  AND pi.note ='Volker Boehm'
  AND t.production_year BETWEEN 1980 AND 1995
  AND ci.movie_id = ml.linked_movie_id;
;
