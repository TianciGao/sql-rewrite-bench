-- Case-local minimal PG DDL for PERF_0095
-- Reduced witness schema, not a full JOB schema reproduction.

CREATE TABLE complete_cast (
  movie_id INT,
  subject_id INT,
  status_id INT
);

CREATE TABLE comp_cast_type (
  id INT,
  kind VARCHAR(64)
);

CREATE TABLE char_name (
  id INT,
  name TEXT
);

CREATE TABLE cast_info (
  movie_id INT,
  person_role_id INT,
  person_id INT
);

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE kind_type (
  id INT,
  kind VARCHAR(32)
);

CREATE TABLE movie_keyword (
  movie_id INT,
  keyword_id INT
);

CREATE TABLE name (
  id INT
);

CREATE TABLE title (
  id INT,
  title TEXT,
  production_year INT,
  kind_id INT
);
