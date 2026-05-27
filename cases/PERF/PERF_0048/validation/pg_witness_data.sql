insert into date_dim (d_date_sk, d_date) values (1, date '1998-08-04');

insert into store (s_store_sk) values (10);
insert into web_page (wp_web_page_sk) values (20);

insert into store_sales (ss_sold_date_sk, ss_store_sk, ss_ext_sales_price, ss_net_profit) values
    (1, 10, 100.00, 30.00);

insert into store_returns (sr_returned_date_sk, sr_store_sk, sr_return_amt, sr_net_loss) values
    (1, 10, 5.00, 1.00);

insert into web_sales (ws_sold_date_sk, ws_web_page_sk, ws_ext_sales_price, ws_net_profit) values
    (1, 20, 200.00, 50.00);
