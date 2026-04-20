-- PERF_0005 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `date_dim` (
  `d_date_sk` int NOT NULL,
  `d_moy` int DEFAULT NULL,
  `d_year` int DEFAULT NULL,
  PRIMARY KEY (`d_date_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `item` (
  `i_item_sk` int NOT NULL,
  `i_manager_id` int DEFAULT NULL,
  `i_brand_id` int DEFAULT NULL,
  `i_brand` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`i_item_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `store_sales` (
  `ss_sold_date_sk` int DEFAULT NULL,
  `ss_item_sk` int DEFAULT NULL,
  `ss_ext_sales_price` decimal(7,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
