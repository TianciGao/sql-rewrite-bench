-- PostgreSQL DDL for PERF_0078
-- draft_origin: JOB_DRAFT_0017

CREATE TABLE cast_info (
  id INT,
  movie_id INT,
  person_id INT
);

CREATE TABLE company_name (
  id INT,
  country_code VARCHAR(255)
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE movie_companies (
  id INT,
  company_id INT,
  movie_id INT
);

CREATE TABLE movie_keyword (
  id INT,
  keyword_id INT,
  movie_id INT
);

CREATE TABLE name (
  id INT,
  name TEXT
);

CREATE TABLE title (
  id INT
);
