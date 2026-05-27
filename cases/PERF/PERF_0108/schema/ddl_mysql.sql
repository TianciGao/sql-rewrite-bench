-- Case-local minimal PG DDL for PERF_0108
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE cast_info (
  movie_id INT,
  person_id INT,
  note TEXT
);

CREATE TABLE comp_cast_type (
  id INT,
  kind VARCHAR(64)
);

CREATE TABLE complete_cast (
  movie_id INT,
  subject_id INT,
  status_id INT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
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

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE name (
  id INT,
  name TEXT,
  gender VARCHAR(4)
);

CREATE TABLE title (
  id INT,
  title TEXT,
  production_year INT
);
