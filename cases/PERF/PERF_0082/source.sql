-- draft_id: JOB_DRAFT_0005
-- original local source path: /home/tianci_gao/code/sql-rewrite-bench/runs/codex_overnight/job_candidate_drafts_30/candidates/JOB_DRAFT_0005/source.sql
-- not official case
SELECT min(t.title) AS typical_european_movie
FROM company_type AS ct,
     info_type AS it,
     movie_companies AS mc,
     movie_info AS mi,
     title AS t
WHERE ct.kind = 'production companies'
  AND mc.note like '%(theatrical)%'
  AND mc.note like '%(France)%'
  AND mi.info IN ('Sweden',
                  'Norway',
                  'Germany',
                  'Denmark',
                  'Swedish',
                  'Denish',
                  'Norwegian',
                  'German')
  AND t.production_year > 2005
  AND t.id = mi.movie_id
  AND t.id = mc.movie_id
  AND mc.movie_id = mi.movie_id
  AND ct.id = mc.company_type_id
  AND it.id = mi.info_type_id;
