-- Case-local minimal PG DDL for PERF_0107
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE company_name (
  id INT,
  country_code STRING,
  name STRING
);

CREATE TABLE company_type (
  id INT,
  kind STRING
);

CREATE TABLE comp_cast_type (
  id INT,
  kind STRING
);

CREATE TABLE complete_cast (
  movie_id INT,
  subject_id INT,
  status_id INT
);

CREATE TABLE keyword (
  id INT,
  keyword STRING
);

CREATE TABLE link_type (
  id INT,
  link STRING
);

CREATE TABLE movie_companies (
  movie_id INT,
  company_id INT,
  company_type_id INT,
  note STRING
);

CREATE TABLE movie_info (
  movie_id INT,
  info STRING
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
  title STRING,
  production_year INT
);
