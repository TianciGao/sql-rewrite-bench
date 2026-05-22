set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0035_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
with v1 as (
    select
        i.i_category,
        i.i_brand,
        cc.cc_name,
        d.d_year,
        d.d_moy,
        sum(cs.cs_sales_price) as sum_sales,
        avg(sum(cs.cs_sales_price)) over (
            partition by i.i_category, i.i_brand, cc.cc_name, d.d_year
        ) as avg_monthly_sales,
        rank() over (
            partition by i.i_category, i.i_brand, cc.cc_name
            order by d.d_year, d.d_moy
        ) as rn
    from item i
    join catalog_sales cs on cs.cs_item_sk = i.i_item_sk
    join date_dim d on cs.cs_sold_date_sk = d.d_date_sk
    join call_center cc on cc.cc_call_center_sk = cs.cs_call_center_sk
    where (
          d.d_year = 2000
          or (d.d_year = 2000 - 1 and d.d_moy = 12)
          or (d.d_year = 2000 + 1 and d.d_moy = 1)
      )
    group by i.i_category, i.i_brand, cc.cc_name, d.d_year, d.d_moy
),
v2 as (
    select
        v1.cc_name,
        v1.d_year,
        v1.d_moy,
        v1.avg_monthly_sales,
        v1.sum_sales,
        v1_lag.sum_sales as psum,
        v1_lead.sum_sales as nsum
    from v1
    join v1 v1_lag on v1.i_category = v1_lag.i_category
                  and v1.i_brand = v1_lag.i_brand
                  and v1.cc_name = v1_lag.cc_name
                  and v1.rn = v1_lag.rn + 1
    join v1 v1_lead on v1.i_category = v1_lead.i_category
                   and v1.i_brand = v1_lead.i_brand
                   and v1.cc_name = v1_lead.cc_name
                   and v1.rn = v1_lead.rn - 1
)
select *
from v2
where d_year = 2000
  and avg_monthly_sales > 0
  and case
          when avg_monthly_sales > 0
            then abs(sum_sales - avg_monthly_sales) / avg_monthly_sales
          else null
      end > 0.1
order by sum_sales - avg_monthly_sales, nsum
limit 100;
rollback;
