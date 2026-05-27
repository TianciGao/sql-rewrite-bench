set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0077_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT min(t.title) AS movie_title
FROM keyword k
JOIN movie_keyword mk ON k.id = mk.keyword_id
JOIN movie_info mi ON mk.movie_id = mi.movie_id
JOIN title t ON t.id = mi.movie_id
WHERE k.keyword LIKE '%sequel%'
  AND mi.info IN ('Sweden',
                  'Norway',
                  'Germany',
                  'Denmark',
                  'Swedish',
                  'Denish',
                  'Norwegian',
                  'German')
  AND t.production_year > 2005;
rollback;
