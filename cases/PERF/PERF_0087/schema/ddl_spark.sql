-- Case-local minimal Spark DDL for PERF_0087
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(255),
  name STRING
);

CREATE TABLE company_type (
  id INT,
  kind VARCHAR(32)
);

CREATE TABLE keyword (
  id INT,
  keyword STRING
);

CREATE TABLE link_type (
  id INT,
  link VARCHAR(32)
);

CREATE TABLE movie_companies (
  id INT,
  company_id INT,
  company_type_id INT,
  movie_id INT,
  note STRING
);

CREATE TABLE movie_keyword (
  id INT,
  keyword_id INT,
  movie_id INT
);

CREATE TABLE movie_link (
  id INT,
  link_type_id INT,
  movie_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title STRING
);
