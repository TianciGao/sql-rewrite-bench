-- Case-local minimal MySQL DDL for PERF_0094
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE cast_info (
  movie_id INT,
  person_id INT,
  note TEXT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE movie_info (
  movie_id INT,
  info_type_id INT,
  info TEXT,
  note TEXT
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info TEXT
);

CREATE TABLE name (
  id INT,
  gender VARCHAR(1)
);

CREATE TABLE title (
  id INT,
  title TEXT,
  production_year INT
);
