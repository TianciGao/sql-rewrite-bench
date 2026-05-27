-- Case-local minimal MySQL DDL for PERF_0097
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(8),
  name TEXT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE kind_type (
  id INT,
  kind VARCHAR(32)
);

CREATE TABLE link_type (
  id INT,
  link VARCHAR(64)
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT
);

CREATE TABLE movie_info_idx (
  movie_id INT,
  info_type_id INT,
  info TEXT
);

CREATE TABLE movie_link (
  movie_id INT,
  linked_movie_id INT,
  link_type_id INT
);

CREATE TABLE title (
  id INT,
  title TEXT,
  kind_id INT,
  production_year INT
);
