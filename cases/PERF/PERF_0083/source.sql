-- draft_id: JOB_DRAFT_0006
-- original local source path: /home/tianci_gao/code/sql-rewrite-bench/runs/codex_overnight/job_candidate_drafts_30/candidates/JOB_DRAFT_0006/source.sql
-- not official case
SELECT min(k.keyword) AS movie_keyword,
       min(n.name) AS actor_name,
       min(t.title) AS marvel_movie
FROM cast_info AS ci,
     keyword AS k,
     movie_keyword AS mk,
     name AS n,
     title AS t
WHERE k.keyword = 'marvel-cinematic-universe'
  AND n.name LIKE '%Downey%Robert%'
  AND t.production_year > 2010
  AND k.id = mk.keyword_id
  AND t.id = mk.movie_id
  AND t.id = ci.movie_id
  AND ci.movie_id = mk.movie_id
  AND n.id = ci.person_id;
