-- PERF_0046 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (ss_sold_date_sk int, ss_item_sk int, ss_store_sk int, ss_sales_price decimal(9,2), ss_quantity int);
create table date_dim (d_date_sk int primary key, d_year int, d_qoy int, d_moy int, d_month_seq int);
create table store (s_store_sk int primary key, s_store_id varchar(30));
create table item (i_item_sk int primary key, i_category varchar(30), i_class varchar(30), i_brand varchar(30), i_product_name varchar(80));
