-- DRAFT DDL only; not executed in this task
CREATE TABLE results (driverid INT, fastestlaptime STRING) USING parquet;
CREATE TABLE drivers (driverid INT, code STRING, dob DATE) USING parquet;
