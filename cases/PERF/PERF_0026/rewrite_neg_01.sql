-- PERF_0026 negative rewrite candidate.
-- Strategy: keep the positive rewrite shape but change one country-code prefix from '19' to '18'.
-- Non-equivalence is not yet proven.

with eligible_prefixes(cntrycode) as (
    values
        ('18'),
        ('29'),
        ('21'),
        ('25'),
        ('16'),
        ('10'),
        ('14')
),
eligible_avg as (
    select
        avg(customer.c_acctbal) as avg_acctbal
    from
        customer
        join eligible_prefixes
            on substring(customer.c_phone from 1 for 2) = eligible_prefixes.cntrycode
    where
        customer.c_acctbal > 0.00
)
select
    custsale.cntrycode,
    count(*) as numcust,
    sum(custsale.c_acctbal) as totacctbal
from
    (
        select
            substring(customer.c_phone from 1 for 2) as cntrycode,
            customer.c_acctbal
        from
            customer
            join eligible_prefixes
                on substring(customer.c_phone from 1 for 2) = eligible_prefixes.cntrycode
            cross join eligible_avg
        where
            customer.c_acctbal > eligible_avg.avg_acctbal
            and not exists (
                select
                    1
                from
                    orders
                where
                    orders.o_custkey = customer.c_custkey
            )
    ) as custsale
group by
    custsale.cntrycode
order by
    custsale.cntrycode;
