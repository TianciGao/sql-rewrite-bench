set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_port_0003_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT gsoffered FROM schools ORDER BY ABS(longitude) DESC NULLS LAST LIMIT 1;
rollback;
