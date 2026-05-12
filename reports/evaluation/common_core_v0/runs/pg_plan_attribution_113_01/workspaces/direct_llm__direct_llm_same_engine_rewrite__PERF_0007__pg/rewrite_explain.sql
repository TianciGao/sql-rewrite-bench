set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0007_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= '1995-01-01'
	and l_shipdate < '1996-01-01'
	and l_discount between 0.08 and 0.10
	and l_quantity < 25;
rollback;
