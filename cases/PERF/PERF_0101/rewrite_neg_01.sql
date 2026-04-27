SELECT min(an.name) AS cool_actor_pseudonym,
       min(t.title) AS series_named_after_char
FROM aka_name AS an
JOIN name AS n
  ON n.id = an.person_id
JOIN cast_info AS ci
  ON ci.person_id = n.id
JOIN title AS t
  ON t.id = ci.movie_id
JOIN movie_keyword AS mk
  ON mk.movie_id = t.id
JOIN keyword AS k
  ON k.id = mk.keyword_id
JOIN movie_companies AS mc
  ON mc.movie_id = t.id
JOIN company_name AS cn
  ON cn.id = mc.company_id
WHERE cn.country_code ='[us]'
  AND k.keyword ='character-name-in-title'
  AND t.episode_nr >= 50
  AND t.episode_nr < 100
  AND an.person_id = ci.person_id
  AND ci.movie_id = mc.movie_id
  AND ci.movie_id = mk.movie_id
  AND mc.movie_id = mk.movie_id;
