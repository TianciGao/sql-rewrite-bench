-- PERF_0046 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim (d_date_sk, d_year, d_qoy, d_moy, d_month_seq) values (1, 2001, 1, 1, 1212);
insert into item (i_item_sk, i_category, i_class, i_brand, i_product_name) values (10, 'Books', 'Reference', 'BrandA', 'ProductA');
insert into store (s_store_sk, s_store_id) values (20, 'STORE20');
insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_store_sk, ss_sales_price, ss_quantity) values (1, 10, 20, 25.00, 4);
