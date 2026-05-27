set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0006_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
select
	l_returnflag,
	l_linestatus,
	sum(l_quantity) as sum_qty,
	sum(l_extendedprice) as sum_base_price,
	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
	avg(l_quantity) as avg_qty,
	avg(l_extendedprice) as avg_price,
	avg(l_discount) as avg_disc,
	count(*) as count_order
from
	lineitem
where
	l_shipdate <= '1998-08-27'
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;
rollback;
