-- PostgreSQL DDL for PERF_0079
-- draft_origin: JOB_DRAFT_0010

CREATE TABLE char_name (
  id INT,
  name TEXT
);

CREATE TABLE cast_info (
  id INT,
  movie_id INT,
  note TEXT,
  person_role_id INT,
  role_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(255)
);

CREATE TABLE company_type (
  id INT
);

CREATE TABLE movie_companies (
  id INT,
  company_id INT,
  company_type_id INT,
  movie_id INT
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
