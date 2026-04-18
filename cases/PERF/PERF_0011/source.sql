-- PERF_0011 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source path: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/14.sql
-- Seed: TPC-H Query 14, Promotion Effect Query
-- Status: raw qgen template copied for provenance only; not materialized in this step.
-- Non-claims: no rewrite, DDL, data profile, validation, plan, admission, or promotion fact is asserted here.

-- $ID$
-- TPC-H/TPC-R Promotion Effect Query (Q14)
-- Functional Query Definition
-- Approved February 1998
:x
:o
select
	100.00 * sum(case
		when p_type like 'PROMO%'
			then l_extendedprice * (1 - l_discount)
		else 0
	end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
	lineitem,
	part
where
	l_partkey = p_partkey
	and l_shipdate >= date ':1'
	and l_shipdate < date ':1' + interval '1' month;
:n -1
