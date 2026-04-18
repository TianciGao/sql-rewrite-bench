-- PERF_0005 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table date_dim
(
    d_date_sk integer not null,
    d_moy integer,
    d_year integer,
    primary key (d_date_sk)
);

create table item
(
    i_item_sk integer not null,
    i_manager_id integer,
    i_brand_id integer,
    i_brand varchar(50),
    primary key (i_item_sk)
);

create table store_sales
(
    ss_sold_date_sk integer,
    ss_item_sk integer,
    ss_ext_sales_price decimal(7,2)
);
