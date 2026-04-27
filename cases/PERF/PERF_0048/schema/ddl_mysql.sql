-- PERF_0048 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
    ss_sold_date_sk int,
    ss_store_sk int,
    ss_ext_sales_price decimal(9,2),
    ss_net_profit decimal(9,2)
);

create table store_returns (
    sr_returned_date_sk int,
    sr_store_sk int,
    sr_return_amt decimal(9,2),
    sr_net_loss decimal(9,2)
);

create table catalog_sales (
    cs_sold_date_sk int,
    cs_call_center_sk int,
    cs_ext_sales_price decimal(9,2),
    cs_net_profit decimal(9,2)
);

create table catalog_returns (
    cr_returned_date_sk int,
    cr_call_center_sk int,
    cr_return_amount decimal(9,2),
    cr_net_loss decimal(9,2)
);

create table web_sales (
    ws_sold_date_sk int,
    ws_web_page_sk int,
    ws_ext_sales_price decimal(9,2),
    ws_net_profit decimal(9,2)
);

create table web_returns (
    wr_returned_date_sk int,
    wr_web_page_sk int,
    wr_return_amt decimal(9,2),
    wr_net_loss decimal(9,2)
);

create table date_dim (
    d_date_sk int primary key,
    d_date date
);

create table store (
    s_store_sk int primary key
);

create table web_page (
    wp_web_page_sk int primary key
);
