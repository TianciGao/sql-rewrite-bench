#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

DATA_DIR="$(realpath "$PWD/datasets/loaded/job_perf0004_pg")"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<SQL
DROP TABLE IF EXISTS complete_cast CASCADE;
DROP TABLE IF EXISTS comp_cast_type CASCADE;
DROP TABLE IF EXISTS cast_info CASCADE;
DROP TABLE IF EXISTS info_type CASCADE;
DROP TABLE IF EXISTS keyword CASCADE;
DROP TABLE IF EXISTS movie_info CASCADE;
DROP TABLE IF EXISTS movie_info_idx CASCADE;
DROP TABLE IF EXISTS movie_keyword CASCADE;
DROP TABLE IF EXISTS name CASCADE;
DROP TABLE IF EXISTS title CASCADE;

CREATE TABLE complete_cast (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer,
    subject_id integer NOT NULL,
    status_id integer NOT NULL
);

CREATE TABLE comp_cast_type (
    id integer NOT NULL PRIMARY KEY,
    kind character varying(32) NOT NULL
);

CREATE TABLE cast_info (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    movie_id integer NOT NULL,
    person_role_id integer,
    note text,
    nr_order integer,
    role_id integer NOT NULL
);

CREATE TABLE info_type (
    id integer NOT NULL PRIMARY KEY,
    info character varying(32) NOT NULL
);

CREATE TABLE keyword (
    id integer NOT NULL PRIMARY KEY,
    keyword text NOT NULL,
    phonetic_code character varying(5)
);

CREATE TABLE movie_info (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info text NOT NULL,
    note text
);

CREATE TABLE movie_info_idx (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info text NOT NULL,
    note text
);

CREATE TABLE movie_keyword (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    keyword_id integer NOT NULL
);

CREATE TABLE name (
    id integer NOT NULL PRIMARY KEY,
    name text NOT NULL,
    imdb_index character varying(12),
    imdb_id integer,
    gender character varying(1),
    name_pcode_cf character varying(5),
    name_pcode_nf character varying(5),
    surname_pcode character varying(5),
    md5sum character varying(32)
);

CREATE TABLE title (
    id integer NOT NULL PRIMARY KEY,
    title text NOT NULL,
    imdb_index character varying(12),
    kind_id integer NOT NULL,
    production_year integer,
    imdb_id integer,
    phonetic_code character varying(5),
    episode_of_id integer,
    season_nr integer,
    episode_nr integer,
    series_years character varying(49),
    md5sum character varying(32)
);

\copy complete_cast  FROM '${DATA_DIR}/complete_cast.csv'  csv escape '\'
\copy comp_cast_type FROM '${DATA_DIR}/comp_cast_type.csv' csv escape '\'
\copy cast_info      FROM '${DATA_DIR}/cast_info.csv'      csv escape '\'
\copy info_type      FROM '${DATA_DIR}/info_type.csv'      csv escape '\'
\copy keyword        FROM '${DATA_DIR}/keyword.csv'        csv escape '\'
\copy movie_info     FROM '${DATA_DIR}/movie_info.csv'     csv escape '\'
\copy movie_info_idx FROM '${DATA_DIR}/movie_info_idx.csv' csv escape '\'
\copy movie_keyword  FROM '${DATA_DIR}/movie_keyword.csv'  csv escape '\'
\copy name           FROM '${DATA_DIR}/name.csv'           csv escape '\'
\copy title          FROM '${DATA_DIR}/title.csv'          csv escape '\'

SELECT 'complete_cast', COUNT(*) FROM complete_cast;
SELECT 'comp_cast_type', COUNT(*) FROM comp_cast_type;
SELECT 'cast_info', COUNT(*) FROM cast_info;
SELECT 'info_type', COUNT(*) FROM info_type;
SELECT 'keyword', COUNT(*) FROM keyword;
SELECT 'movie_info', COUNT(*) FROM movie_info;
SELECT 'movie_info_idx', COUNT(*) FROM movie_info_idx;
SELECT 'movie_keyword', COUNT(*) FROM movie_keyword;
SELECT 'name', COUNT(*) FROM name;
SELECT 'title', COUNT(*) FROM title;
SQL
