with ss as (
    select
        i.i_item_id,
        sum(ss.ss_ext_sales_price) as total_sales
    from store_sales ss
    join date_dim d on ss.ss_sold_date_sk = d.d_date_sk
    join customer_address ca on ss.ss_addr_sk = ca.ca_address_sk
    join item i on ss.ss_item_sk = i.i_item_sk
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and d.d_year = 2000
      and d.d_moy = 1
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
),
cs as (
    select
        i.i_item_id,
        sum(cs.cs_ext_sales_price) as total_sales
    from catalog_sales cs
    join date_dim d on cs.cs_sold_date_sk = d.d_date_sk
    join customer_address ca on cs.cs_bill_addr_sk = ca.ca_address_sk
    join item i on cs.cs_item_sk = i.i_item_sk
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and d.d_year = 2000
      and d.d_moy = 1
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
),
ws as (
    select
        i.i_item_id,
        sum(ws.ws_ext_sales_price) as total_sales
    from web_sales ws
    join date_dim d on ws.ws_sold_date_sk = d.d_date_sk
    join customer_address ca on ws.ws_bill_addr_sk = ca.ca_address_sk
    join item i on ws.ws_item_sk = i.i_item_sk
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and d.d_year = 2000
      and d.d_moy = 1
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
)
select
    i_item_id,
    sum(total_sales) as total_sales
from (
    select * from ss
    union all
    select * from cs
    union all
    select * from ws
) tmp1
group by i_item_id
order by total_sales, i_item_id
limit 100;
