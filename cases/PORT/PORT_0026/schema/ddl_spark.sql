CREATE TABLE races (raceid INT, date DATE) USING parquet;
CREATE TABLE results (raceid INT, driverid INT, time STRING) USING parquet;
