-- Case-local minimal Spark DDL for PERF_0093
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE aka_name (
  id INT,
  name STRING,
  person_id INT
);

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
  id INT
);

CREATE TABLE title (
  id INT,
  title STRING,
  episode_nr INT
);
