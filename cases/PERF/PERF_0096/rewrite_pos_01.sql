SELECT min(lt.link) AS link_type,
       min(t1.title) AS first_movie,
       min(t2.title) AS second_movie
FROM keyword AS k
JOIN movie_keyword AS mk
  ON mk.keyword_id = k.id
JOIN title AS t1
  ON t1.id = mk.movie_id
JOIN movie_link AS ml
  ON ml.movie_id = t1.id
JOIN title AS t2
  ON ml.linked_movie_id = t2.id
JOIN link_type AS lt
  ON lt.id = ml.link_type_id
WHERE k.keyword ='character-name-in-title'
  AND mk.movie_id = t1.id;
