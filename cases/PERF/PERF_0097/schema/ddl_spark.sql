-- Case-local minimal Spark DDL for PERF_0097
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code STRING,
  name STRING
);

CREATE TABLE info_type (
  id INT,
  info STRING
);

CREATE TABLE kind_type (
  id INT,
  kind STRING
);

CREATE TABLE link_type (
  id INT,
  link STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info STRING
);

CREATE TABLE movie_link (
  movie_id INT,
  linked_movie_id INT,
  link_type_id INT
);

CREATE TABLE title (
  id INT,
  title STRING,
  kind_id INT,
  production_year INT
);
