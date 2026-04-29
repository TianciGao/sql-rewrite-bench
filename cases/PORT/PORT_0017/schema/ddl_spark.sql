-- DRAFT DDL only; not executed in this task
CREATE TABLE frpm (cdscode STRING, fm_count STRING, enrollment_k12 DOUBLE) USING parquet;
CREATE TABLE schools (cdscode STRING, county STRING, charter INT, school STRING) USING parquet;
