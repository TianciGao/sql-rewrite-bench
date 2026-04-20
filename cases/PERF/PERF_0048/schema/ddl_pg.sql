create table store_sales (
    ss_sold_date_sk integer,
    ss_store_sk integer,
    ss_ext_sales_price decimal(9,2),
    ss_net_profit decimal(9,2)
);

create table store_returns (
    sr_returned_date_sk integer,
    sr_store_sk integer,
    sr_return_amt decimal(9,2),
    sr_net_loss decimal(9,2)
);

create table catalog_sales (
    cs_sold_date_sk integer,
    cs_call_center_sk integer,
    cs_ext_sales_price decimal(9,2),
    cs_net_profit decimal(9,2)
);

create table catalog_returns (
    cr_returned_date_sk integer,
    cr_call_center_sk integer,
    cr_return_amount decimal(9,2),
    cr_net_loss decimal(9,2)
);

create table web_sales (
    ws_sold_date_sk integer,
    ws_web_page_sk integer,
    ws_ext_sales_price decimal(9,2),
    ws_net_profit decimal(9,2)
);

create table web_returns (
    wr_returned_date_sk integer,
    wr_web_page_sk integer,
    wr_return_amt decimal(9,2),
    wr_net_loss decimal(9,2)
);

create table date_dim (
    d_date_sk integer primary key,
    d_date date
);

create table store (
    s_store_sk integer primary key
);

create table web_page (
    wp_web_page_sk integer primary key
);
