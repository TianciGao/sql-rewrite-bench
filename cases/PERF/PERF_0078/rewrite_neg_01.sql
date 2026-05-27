-- case_id: PERF_0078
-- draft_origin: JOB_DRAFT_0017
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- official case-local negative rewrite candidate; validation status established only by engine runs
-- Proposed hard negative: change one equality literal to a related but different value. This rewrite is intentionally semantically different from the source query.
SELECT min(n.name) AS member_in_charnamed_american_movie,
       min(n.name) AS a1
FROM cast_info AS ci
JOIN movie_companies AS mc ON ci.movie_id = mc.movie_id
JOIN company_name AS cn ON mc.company_id = cn.id
JOIN movie_keyword AS mk ON ci.movie_id = mk.movie_id
JOIN keyword AS k ON mk.keyword_id = k.id
JOIN name AS n ON n.id = ci.person_id
JOIN title AS t ON ci.movie_id = t.id AND t.id = mk.movie_id AND t.id = mc.movie_id
WHERE cn.country_code ='[gb]'
  AND k.keyword ='character-name-in-title'
  AND n.name LIKE 'B%';
