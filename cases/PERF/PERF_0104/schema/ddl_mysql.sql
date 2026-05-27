-- Case-local minimal PG DDL for PERF_0104
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

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE link_type (
  id INT,
  link TEXT
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT,
  note TEXT
);

CREATE TABLE movie_info (
  movie_id INT,
  info TEXT
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE movie_link (
  movie_id INT,
  linked_movie_id INT,
  link_type_id INT
);

CREATE TABLE title (
  id INT,
  title TEXT,
  production_year INT
);
