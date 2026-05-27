-- Case-local minimal MySQL DDL for PERF_0096
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE link_type (
  id INT,
  link VARCHAR(64)
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
  title TEXT
);
