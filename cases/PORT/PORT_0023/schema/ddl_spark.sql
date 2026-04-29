CREATE TABLE player (player_api_id INT, player_name STRING) USING PARQUET;
CREATE TABLE player_attributes (player_api_id INT, attr_date DATE, long_shots INT) USING PARQUET;
