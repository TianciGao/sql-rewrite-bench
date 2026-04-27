-- Case-local minimal Spark DDL for PERF_0091
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

CREATE TABLE kind_type (
  id INT,
  kind STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT
);

CREATE TABLE movie_info (
  movie_id INT,
  info_type_id INT
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE title (
  id INT,
  title STRING,
  kind_id INT
);
