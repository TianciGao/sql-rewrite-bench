CREATE TABLE cards (id INT, uuid STRING) USING parquet;
CREATE TABLE foreign_data (uuid STRING, language STRING) USING parquet;
