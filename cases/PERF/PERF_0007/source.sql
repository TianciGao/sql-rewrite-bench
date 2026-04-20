-- PERF_0007 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/6.sql
-- Seed: TPC-H Query 6, Forecasting Revenue Change Query
-- Status: unmaterialized qgen template; substitution markers :1, :2, and :3 are intentionally preserved.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- $ID$
-- TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
-- Functional Query Definition
-- Approved February 1998
:x
:o
select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= date ':1'
	and l_shipdate < date ':1' + interval '1' year
	and l_discount between :2 - 0.01 and :2 + 0.01
	and l_quantity < :3;
:n -1
