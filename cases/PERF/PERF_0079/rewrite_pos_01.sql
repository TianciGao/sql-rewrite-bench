-- case_id: PERF_0079
-- draft_origin: JOB_DRAFT_0010
-- intended equivalence: explicit join normalization and layout cleanup only; no intended semantic change
-- official case-local positive rewrite candidate; validation status established only by engine runs
-- Proposed positive rewrite: normalize old-style comma joins into explicit INNER JOINs while preserving the original filter semantics.
SELECT min(chn.name) AS uncredited_voiced_character,
       min(t.title) AS russian_movie
FROM char_name AS chn
JOIN cast_info AS ci ON chn.id = ci.person_role_id
JOIN movie_companies AS mc ON ci.movie_id = mc.movie_id
JOIN company_name AS cn ON cn.id = mc.company_id
JOIN company_type AS ct ON ct.id = mc.company_type_id
JOIN role_type AS rt ON rt.id = ci.role_id
JOIN title AS t ON t.id = mc.movie_id AND t.id = ci.movie_id
WHERE ci.note like '%(voice)%'
  AND ci.note like '%(uncredited)%'
  AND cn.country_code = '[ru]'
  AND rt.role = 'actor'
  AND t.production_year > 2005;
