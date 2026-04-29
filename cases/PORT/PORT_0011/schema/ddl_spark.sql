-- DRAFT DDL only; not executed in this task
CREATE TABLE budget (link_to_event INT, event_status STRING, remaining DOUBLE) USING parquet;
CREATE TABLE event (event_id INT, event_name STRING) USING parquet;
