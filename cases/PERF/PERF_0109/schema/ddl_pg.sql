-- Case-local minimal PG DDL for PERF_0109
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE cast_info (
  movie_id INT,
  person_id INT,
  note TEXT
);

CREATE TABLE company_name (
  id INT,
  name TEXT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT
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
  name TEXT
);

CREATE TABLE title (
  id INT,
  title TEXT
);
