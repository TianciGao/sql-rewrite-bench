-- Case-local minimal PG DDL for PERF_0086
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE aka_name (
  id INT,
  name TEXT,
  person_id INT
);

CREATE TABLE cast_info (
  id INT,
  movie_id INT,
  note TEXT,
  person_id INT,
  role_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(255)
);

CREATE TABLE movie_companies (
  id INT,
  company_id INT,
  movie_id INT,
  note TEXT
);

CREATE TABLE name (
  id INT,
  name TEXT
);

CREATE TABLE role_type (
  id INT,
  role VARCHAR(32)
);

CREATE TABLE title (
  id INT,
  title TEXT
);
