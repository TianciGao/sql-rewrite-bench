with customer_total_return as (
    select
        sr_customer_sk as ctr_customer_sk,
        sr_store_sk as ctr_store_sk,
        sum(sr_fee) as ctr_total_return
    from store_returns
    join date_dim on sr_returned_date_sk = d_date_sk
    where d_year = 2000
    group by sr_customer_sk, sr_store_sk
)
select c_customer_id
from customer_total_return ctr1
join store on s_store_sk = ctr1.ctr_store_sk
join customer on ctr1.ctr_customer_sk = c_customer_sk
where ctr1.ctr_total_return > (
        select avg(ctr_total_return) * 1.2
        from customer_total_return ctr2
        where ctr1.ctr_store_sk = ctr2.ctr_store_sk
    )
  and s_state = 'TN'
order by c_customer_id
limit 100;
