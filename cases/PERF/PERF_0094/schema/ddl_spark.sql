-- Case-local minimal Spark DDL for PERF_0094
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE cast_info (
  movie_id INT,
  person_id INT,
  note STRING
);

CREATE TABLE info_type (
  id INT,
  info STRING
);

CREATE TABLE movie_info (
  movie_id INT,
  info_type_id INT,
  info STRING,
  note STRING
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE name (
  id INT,
  gender STRING
);

CREATE TABLE title (
  id INT,
  title STRING,
  production_year INT
);
