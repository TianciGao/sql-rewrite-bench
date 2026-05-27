set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0054_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
select
    dt.d_year,
    item.i_brand_id as brand_id,
    item.i_brand as brand,
    sum(ss_ext_sales_price) as sum_agg
from date_dim dt
join store_sales on dt.d_date_sk = store_sales.ss_sold_date_sk
join item on store_sales.ss_item_sk = item.i_item_sk
where item.i_manufact_id = 436
  and dt.d_moy = 12
group by dt.d_year, item.i_brand, item.i_brand_id
order by dt.d_year, sum_agg desc, brand_id
limit 100;
rollback;
