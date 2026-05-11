set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__port_0003;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT gsoffered FROM schools ORDER BY ABS(longitude) DESC NULLS LAST LIMIT 1;
rollback;
