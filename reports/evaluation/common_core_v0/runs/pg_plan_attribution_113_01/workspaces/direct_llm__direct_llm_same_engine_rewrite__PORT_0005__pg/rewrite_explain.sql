set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_port_0005_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT nationality FROM drivers WHERE dob IS NOT NULL ORDER BY dob ASC NULLS FIRST LIMIT 1;
rollback;
