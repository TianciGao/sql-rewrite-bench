set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0082_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT min(t.title) AS typical_european_movie
FROM company_type ct
JOIN movie_companies mc ON ct.id = mc.company_type_id
JOIN movie_info mi ON mc.movie_id = mi.movie_id
JOIN title t ON t.id = mi.movie_id
JOIN info_type it ON it.id = mi.info_type_id
WHERE ct.kind = 'production companies'
  AND mc.note LIKE '%(theatrical)%'
  AND mc.note LIKE '%(France)%'
  AND mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Denish', 'Norwegian', 'German')
  AND t.production_year > 2005;
rollback;
