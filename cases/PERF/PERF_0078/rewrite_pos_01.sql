-- case_id: PERF_0078
-- draft_origin: JOB_DRAFT_0017
-- intended equivalence: explicit join normalization and layout cleanup only; no intended semantic change
-- official case-local positive rewrite candidate; validation status established only by engine runs
-- Proposed positive rewrite: normalize old-style comma joins into explicit INNER JOINs while preserving the original filter semantics.
SELECT min(n.name) AS member_in_charnamed_american_movie,
       min(n.name) AS a1
FROM cast_info AS ci
JOIN movie_companies AS mc ON ci.movie_id = mc.movie_id
JOIN company_name AS cn ON mc.company_id = cn.id
JOIN movie_keyword AS mk ON ci.movie_id = mk.movie_id
JOIN keyword AS k ON mk.keyword_id = k.id
JOIN name AS n ON n.id = ci.person_id
JOIN title AS t ON ci.movie_id = t.id AND t.id = mk.movie_id AND t.id = mc.movie_id
WHERE cn.country_code ='[us]'
  AND k.keyword ='character-name-in-title'
  AND n.name LIKE 'B%';
