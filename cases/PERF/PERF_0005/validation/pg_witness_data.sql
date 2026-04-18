-- PERF_0005 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-DS scale dataset and does not imply MySQL/Spark readiness.

insert into date_dim (d_date_sk, d_moy, d_year) values
    (1, 11, 2001);

insert into item (i_item_sk, i_manager_id, i_brand_id, i_brand) values
    (10, 1, 100, 'brand_manager_1'),
    (20, 2, 200, 'brand_manager_2');

insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_ext_sales_price) values
    (1, 10, 150.00),
    (1, 20, 80.00);
