CREATE TABLE drivers (driver_id INT, forename STRING, surname STRING, nationality STRING, dob DATE) USING PARQUET;
CREATE TABLE driverstandings (driver_id INT, race_id INT) USING PARQUET;
CREATE TABLE races (race_id INT, name STRING) USING PARQUET;
