set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0007;
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
