-- MySQL DDL for PERF_0081
-- draft_origin: JOB_DRAFT_0004

CREATE TABLE info_type (
  id INT,
  info TEXT
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE movie_info_idx (
  id INT,
  movie_id INT,
  info_type_id INT,
  info TEXT
);

CREATE TABLE movie_keyword (
  id INT,
  keyword_id INT,
  movie_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
