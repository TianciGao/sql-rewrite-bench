-- PERF_0008 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source path: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql
-- Seed: TPC-H Query 3, Shipping Priority Query
-- Status: raw qgen template copied for provenance only; not materialized in this step.
-- Non-claims: no rewrite, DDL, data profile, validation, plan, admission, or promotion fact is asserted here.

-- $ID$
-- TPC-H/TPC-R Shipping Priority Query (Q3)
-- Functional Query Definition
-- Approved February 1998
:x
:o
select
	l_orderkey,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	o_orderdate,
	o_shippriority
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = ':1'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date ':2'
	and l_shipdate > date ':2'
group by
	l_orderkey,
	o_orderdate,
	o_shippriority
order by
	revenue desc,
	o_orderdate;
:n 10
