set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0024_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
select
    s_name,
    s_address
from
    supplier
join
    nation on s_nationkey = n_nationkey
where
    s_suppkey in (
        select
            ps_suppkey
        from
            partsupp
        where
            ps_partkey in (
                select
                    p_partkey
                from
                    part
                where
                    p_name like 'pale%'
            )
            and ps_availqty > (
                select
                    0.5 * sum(l_quantity)
                from
                    lineitem
                where
                    l_partkey = ps_partkey
                    and l_suppkey = ps_suppkey
                    and l_shipdate >= date '1997-01-01'
                    and l_shipdate < date '1997-01-01' + interval '1' year
            )
    )
    and n_name = 'BRAZIL'
order by
    s_name;
rollback;
