-- Case-local minimal Spark DDL for PERF_0092
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE aka_title (
  id INT,
  title STRING,
  movie_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code STRING
);

CREATE TABLE company_type (
  id INT
);

CREATE TABLE info_type (
  id INT,
  info STRING
);

CREATE TABLE keyword (
  id INT
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT
);

CREATE TABLE movie_info (
  movie_id INT,
  info_type_id INT,
  note STRING
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE title (
  id INT,
  title STRING,
  production_year INT
);
