set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0077_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
-- case_id: PERF_0077
-- source_family: JOB/IMDB
-- original JOB query: 3a.sql
-- draft_origin: JOB_DRAFT_0003
SELECT min(t.title) AS movie_title
FROM keyword AS k,
     movie_info AS mi,
     movie_keyword AS mk,
     title AS t
WHERE k.keyword like '%sequel%'
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
  AND t.id = mk.movie_id
  AND mk.movie_id = mi.movie_id
  AND k.id = mk.keyword_id;
rollback;
