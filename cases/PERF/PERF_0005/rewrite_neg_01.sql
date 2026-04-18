-- PERF_0005 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the source manager predicate.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    dt.d_year,
    item_filtered.i_brand_id as brand_id,
    item_filtered.i_brand as brand,
    sum(store_sales.ss_ext_sales_price) as ext_price
from (
    select
        d_date_sk,
        d_year
    from date_dim
    where d_moy = 11
      and d_year = 2001
) dt
join store_sales
  on dt.d_date_sk = store_sales.ss_sold_date_sk
join (
    select
        i_item_sk,
        i_brand_id,
        i_brand
    from item
    where i_manager_id = 2
) item_filtered
  on store_sales.ss_item_sk = item_filtered.i_item_sk
group by
    dt.d_year,
    item_filtered.i_brand,
    item_filtered.i_brand_id
order by
    dt.d_year,
    ext_price desc,
    brand_id
limit 100;
