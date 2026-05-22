set search_path to attr24_direct_llm__direct_llm_execute_repair_1shot__perf_001;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
select
    c_count,
    count(*) as custdist
from
    (
        select
            c_custkey,
            count(o_orderkey) as c_count
        from
            customer
            left join orders on
                c_custkey = o_custkey
                and o_comment not like '%express%deposits%'
        group by
            c_custkey
    ) as c_orders
group by
    c_count
order by
    custdist desc,
    c_count desc;
rollback;
