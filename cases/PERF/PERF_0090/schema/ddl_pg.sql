-- Case-local minimal PG DDL for PERF_0090
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE char_name (
  id INT,
  name TEXT
);

CREATE TABLE cast_info (
  id INT,
  note TEXT,
  movie_id INT,
  person_role_id INT,
  role_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(8)
);

CREATE TABLE company_type (
  id INT
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT
);

CREATE TABLE role_type (
  id INT,
  role VARCHAR(32)
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
