-- draft_id: JOB_DRAFT_0008
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: narrow a LIKE predicate to force divergence. This rewrite is intentionally semantically different from the source query.
SELECT min(an1.name) AS actress_pseudonym,
       min(t.title) AS japanese_movie_dubbed
FROM aka_name AS an1
JOIN cast_info AS ci ON an1.person_id = ci.person_id
JOIN name AS n1 ON an1.person_id = n1.id AND n1.id = ci.person_id
JOIN role_type AS rt ON ci.role_id = rt.id
JOIN title AS t ON ci.movie_id = t.id
JOIN movie_companies AS mc ON t.id = mc.movie_id
JOIN company_name AS cn ON mc.company_id = cn.id
WHERE ci.note ='(voice: English version)'
  AND cn.country_code ='[jp]'
  AND mc.note like '(Japan)%'
  AND mc.note not like '%(USA)%'
  AND n1.name like '%Yo%'
  AND n1.name not like '%Yu%'
  AND rt.role ='actress'
  AND ci.movie_id = mc.movie_id;
;
