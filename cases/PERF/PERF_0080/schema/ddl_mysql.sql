-- MySQL DDL for PERF_0080
-- draft_origin: JOB_DRAFT_0001

CREATE TABLE company_type (
  id INT,
  kind TEXT
);

CREATE TABLE info_type (
  id INT,
  info TEXT
);

CREATE TABLE movie_companies (
  id INT,
  company_type_id INT,
  movie_id INT,
  note TEXT
);

CREATE TABLE movie_info_idx (
  id INT,
  movie_id INT,
  info_type_id INT,
  info TEXT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
