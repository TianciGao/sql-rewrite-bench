-- Spark DDL for PERF_0084
-- draft_origin: JOB_DRAFT_0012

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(255),
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

CREATE TABLE movie_companies (
  id INT,
  company_id INT,
  company_type_id INT,
  movie_id INT
);

CREATE TABLE movie_info (
  id INT,
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE movie_info_idx (
  id INT,
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title STRING
);
