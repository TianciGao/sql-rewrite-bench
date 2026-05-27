select
    i.i_brand_id as brand_id,
    i.i_brand as brand,
    sum(ss.ss_ext_sales_price) as ext_price
from date_dim d
join store_sales ss on d.d_date_sk = ss.ss_sold_date_sk
join item i on ss.ss_item_sk = i.i_item_sk
where i.i_manager_id = 36
  and d.d_moy = 12
  and d.d_year = 2001
group by i.i_brand, i.i_brand_id
order by ext_price desc, i.i_brand_id
limit 100;
