select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= '1995-01-01'
	and l_shipdate < date_add('1995-01-01', interval 1 year)
	and l_discount between 0.08 and 0.10
	and l_quantity < 25;
