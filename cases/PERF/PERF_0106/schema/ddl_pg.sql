-- Case-local minimal PG DDL for PERF_0106
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(8)
);

CREATE TABLE company_type (
  id INT,
  kind VARCHAR(64)
);

CREATE TABLE comp_cast_type (
  id INT,
  kind VARCHAR(64)
);

CREATE TABLE complete_cast (
  movie_id INT,
  status_id INT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(64)
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
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
  info_type_id INT,
  info TEXT,
  note TEXT
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE title (
  id INT,
  title TEXT,
  kind_id INT,
  production_year INT
);
