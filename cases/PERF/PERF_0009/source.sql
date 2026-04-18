-- PERF_0009 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source path: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/4.sql
-- Seed: TPC-H Query 4, Order Priority Checking Query
-- Status: raw qgen template copied for provenance only; not materialized in this step.
-- Non-claims: no rewrite, DDL, data profile, validation, plan, admission, or promotion fact is asserted here.

-- $ID$
-- TPC-H/TPC-R Order Priority Checking Query (Q4)
-- Functional Query Definition
-- Approved February 1998
:x
:o
select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate >= date ':1'
	and o_orderdate < date ':1' + interval '3' month
	and exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_commitdate < l_receiptdate
	)
group by
	o_orderpriority
order by
	o_orderpriority;
:n -1
