-- MySQL DDL for PERF_0083
-- draft_origin: JOB_DRAFT_0006

CREATE TABLE cast_info (
  id INT,
  movie_id INT,
  person_id INT
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
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
  id INT,
  production_year INT,
  title TEXT
);
