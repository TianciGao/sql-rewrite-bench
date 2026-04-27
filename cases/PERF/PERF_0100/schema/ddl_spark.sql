-- Case-local minimal PG DDL for PERF_0100
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE char_name (
  id INT,
  name STRING
);

CREATE TABLE cast_info (
  movie_id INT,
  person_role_id INT,
  role_id INT,
  note STRING
);

CREATE TABLE company_name (
  id INT,
  country_code STRING
);

CREATE TABLE company_type (
  id INT,
  kind STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT
);

CREATE TABLE role_type (
  id INT,
  role STRING
);

CREATE TABLE title (
  id INT,
  title STRING,
  production_year INT
);
