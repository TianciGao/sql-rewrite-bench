-- draft_id: JOB_DRAFT_0011
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: narrow a LIKE predicate to force divergence. This rewrite is intentionally semantically different from the source query.
SELECT min(cn.name) AS from_company,
       min(lt.link) AS movie_link_type,
       min(t.title) AS non_polish_sequel_movie
FROM company_name AS cn
JOIN movie_companies AS mc ON mc.company_id = cn.id
JOIN company_type AS ct ON mc.company_type_id = ct.id
JOIN movie_link AS ml ON ml.movie_id = mc.movie_id
JOIN link_type AS lt ON lt.id = ml.link_type_id
JOIN movie_keyword AS mk ON ml.movie_id = mk.movie_id
JOIN keyword AS k ON mk.keyword_id = k.id
JOIN title AS t ON ml.movie_id = t.id AND t.id = mk.movie_id AND t.id = mc.movie_id
WHERE cn.country_code !='[pl]'
  AND (cn.name LIKE 'Film%' OR cn.name LIKE '%Warner%')
  AND ct.kind ='production companies'
  AND k.keyword ='sequel'
  AND lt.link LIKE '%follow%'
  AND mc.note IS NULL
  AND t.production_year BETWEEN 1950 AND 2000
  AND mk.movie_id = mc.movie_id;
;
