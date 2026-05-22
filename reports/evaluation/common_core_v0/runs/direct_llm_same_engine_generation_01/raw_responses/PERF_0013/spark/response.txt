select
	n_name,
	sum(l_extendedprice * (1 - l_discount)) as revenue
from
	customer
join
	orders on c_custkey = o_custkey
join
	lineitem on l_orderkey = o_orderkey
join
	supplier on l_suppkey = s_suppkey
join
	nation on c_nationkey = s_nationkey
join
	region on s_nationkey = n_nationkey
where
	r_regionkey = n_regionkey
	and r_name = 'MIDDLE EAST'
	and o_orderdate >= date '1997-01-01'
	and o_orderdate < date '1997-01-01' + interval '1' year
group by
	n_name
order by
	revenue desc;
