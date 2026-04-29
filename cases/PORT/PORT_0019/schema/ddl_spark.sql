CREATE TABLE results (driver_id INT, race_id INT, status_id INT) USING PARQUET;
CREATE TABLE races (race_id INT, name STRING) USING PARQUET;
CREATE TABLE status (status_id INT, label STRING) USING PARQUET;
