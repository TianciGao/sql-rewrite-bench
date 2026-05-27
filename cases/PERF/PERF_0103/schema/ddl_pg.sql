-- Case-local minimal PG DDL for PERF_0103
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
  info TEXT
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info TEXT
);

CREATE TABLE name (
  id INT,
  name TEXT,
  gender VARCHAR(4)
);

CREATE TABLE title (
  id INT,
  title TEXT
);
