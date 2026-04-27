-- Case-local minimal PG DDL for PERF_0105
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code STRING,
  name STRING
);

CREATE TABLE company_type (
  id INT,
  kind STRING
);

CREATE TABLE info_type (
  id INT,
  info STRING
);

CREATE TABLE keyword (
  id INT,
  keyword STRING
);

CREATE TABLE kind_type (
  id INT,
  kind STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT,
  note STRING
);

CREATE TABLE movie_info (
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE title (
  id INT,
  title STRING,
  kind_id INT,
  production_year INT
);
