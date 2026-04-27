-- Case-local minimal PG DDL for PERF_0085
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE aka_name (
  id INT,
  name TEXT,
  person_id INT
);

CREATE TABLE cast_info (
  id INT,
  movie_id INT,
  person_id INT
);

CREATE TABLE info_type (
  id INT,
  info VARCHAR(32)
);

CREATE TABLE link_type (
  id INT,
  link VARCHAR(32)
);

CREATE TABLE movie_link (
  id INT,
  link_type_id INT,
  linked_movie_id INT
);

CREATE TABLE name (
  id INT,
  gender VARCHAR(1),
  name TEXT,
  name_pcode_cf VARCHAR(5)
);

CREATE TABLE person_info (
  id INT,
  info_type_id INT,
  note TEXT,
  person_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
