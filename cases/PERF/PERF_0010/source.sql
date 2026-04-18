-- PERF_0010 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source path: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/12.sql
-- Seed: TPC-H Query 12, Shipping Modes and Order Priority Query
-- Status: raw qgen template copied for provenance only; not materialized in this step.
-- Non-claims: no rewrite, DDL, data profile, validation, plan, admission, or promotion fact is asserted here.

-- $ID$
-- TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
-- Functional Query Definition
-- Approved February 1998
:x
:o
select
	l_shipmode,
	sum(case
		when o_orderpriority = '1-URGENT'
			or o_orderpriority = '2-HIGH'
			then 1
		else 0
	end) as high_line_count,
	sum(case
		when o_orderpriority <> '1-URGENT'
			and o_orderpriority <> '2-HIGH'
			then 1
		else 0
	end) as low_line_count
from
	orders,
	lineitem
where
	o_orderkey = l_orderkey
	and l_shipmode in (':1', ':2')
	and l_commitdate < l_receiptdate
	and l_shipdate < l_commitdate
	and l_receiptdate >= date ':3'
	and l_receiptdate < date ':3' + interval '1' year
group by
	l_shipmode
order by
	l_shipmode;
:n -1
