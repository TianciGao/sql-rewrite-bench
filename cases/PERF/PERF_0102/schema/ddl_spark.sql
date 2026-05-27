-- Case-local minimal PG DDL for PERF_0102
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE cast_info (
  movie_id INT,
  person_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code STRING
);

CREATE TABLE keyword (
  id INT,
  keyword STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE name (
  id INT,
  name STRING
);

CREATE TABLE title (
  id INT,
  title STRING
);
