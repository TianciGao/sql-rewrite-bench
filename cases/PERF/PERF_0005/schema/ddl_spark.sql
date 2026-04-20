-- PERF_0005 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table date_dim
(
    d_date_sk INT,
    d_moy INT,
    d_year INT
);

create table item
(
    i_item_sk INT,
    i_manager_id INT,
    i_brand_id INT,
    i_brand STRING
);

create table store_sales
(
    ss_sold_date_sk INT,
    ss_item_sk INT,
    ss_ext_sales_price decimal(7,2)
);
