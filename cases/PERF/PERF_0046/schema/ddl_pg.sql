create table store_sales (ss_sold_date_sk integer, ss_item_sk integer, ss_store_sk integer, ss_sales_price decimal(9,2), ss_quantity integer);
create table date_dim (d_date_sk integer primary key, d_year integer, d_qoy integer, d_moy integer, d_month_seq integer);
create table store (s_store_sk integer primary key, s_store_id varchar(30));
create table item (i_item_sk integer primary key, i_category varchar(30), i_class varchar(30), i_brand varchar(30), i_product_name varchar(80));
