-- Case-local minimal MySQL DDL for PERF_0091
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(8),
  name TEXT
);

CREATE TABLE company_type (
  id INT,
  kind VARCHAR(64)
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE kind_type (
  id INT,
  kind VARCHAR(32)
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
  info TEXT
);

CREATE TABLE title (
  id INT,
  title TEXT,
  kind_id INT
);
