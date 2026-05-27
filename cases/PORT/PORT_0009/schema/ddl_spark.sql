-- DRAFT DDL only; not executed in this task
CREATE TABLE loan (account_id INT, duration INT, amount DOUBLE) USING parquet;
CREATE TABLE account (account_id INT, date DATE) USING parquet;
