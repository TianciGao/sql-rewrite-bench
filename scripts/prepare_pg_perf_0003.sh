#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

DATA_DIR="$(realpath "$PWD/datasets/loaded/job_perf0003_pg")"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<SQL
DROP TABLE IF EXISTS complete_cast CASCADE;
DROP TABLE IF EXISTS comp_cast_type CASCADE;
DROP TABLE IF EXISTS company_name CASCADE;
DROP TABLE IF EXISTS company_type CASCADE;
DROP TABLE IF EXISTS keyword CASCADE;
DROP TABLE IF EXISTS link_type CASCADE;
DROP TABLE IF EXISTS movie_companies CASCADE;
DROP TABLE IF EXISTS movie_info CASCADE;
DROP TABLE IF EXISTS movie_keyword CASCADE;
DROP TABLE IF EXISTS movie_link CASCADE;
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

CREATE TABLE company_name (
    id integer NOT NULL PRIMARY KEY,
    name text NOT NULL,
    country_code character varying(255),
    imdb_id integer,
    name_pcode_nf character varying(5),
    name_pcode_sf character varying(5),
    md5sum character varying(32)
);

CREATE TABLE company_type (
    id integer NOT NULL PRIMARY KEY,
    kind character varying(32) NOT NULL
);

CREATE TABLE keyword (
    id integer NOT NULL PRIMARY KEY,
    keyword text NOT NULL,
    phonetic_code character varying(5)
);

CREATE TABLE link_type (
    id integer NOT NULL PRIMARY KEY,
    link character varying(32) NOT NULL
);

CREATE TABLE movie_companies (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    company_id integer NOT NULL,
    company_type_id integer NOT NULL,
    note text
);

CREATE TABLE movie_info (
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

CREATE TABLE movie_link (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    linked_movie_id integer NOT NULL,
    link_type_id integer NOT NULL
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

\copy complete_cast    FROM '${DATA_DIR}/complete_cast.csv'    csv escape '\'
\copy comp_cast_type   FROM '${DATA_DIR}/comp_cast_type.csv'   csv escape '\'
\copy company_name     FROM '${DATA_DIR}/company_name.csv'     csv escape '\'
\copy company_type     FROM '${DATA_DIR}/company_type.csv'     csv escape '\'
\copy keyword          FROM '${DATA_DIR}/keyword.csv'          csv escape '\'
\copy link_type        FROM '${DATA_DIR}/link_type.csv'        csv escape '\'
\copy movie_companies  FROM '${DATA_DIR}/movie_companies.csv'  csv escape '\'
\copy movie_info       FROM '${DATA_DIR}/movie_info.csv'       csv escape '\'
\copy movie_keyword    FROM '${DATA_DIR}/movie_keyword.csv'    csv escape '\'
\copy movie_link       FROM '${DATA_DIR}/movie_link.csv'       csv escape '\'
\copy title            FROM '${DATA_DIR}/title.csv'            csv escape '\'

SELECT 'complete_cast', COUNT(*) FROM complete_cast;
SELECT 'comp_cast_type', COUNT(*) FROM comp_cast_type;
SELECT 'company_name', COUNT(*) FROM company_name;
SELECT 'company_type', COUNT(*) FROM company_type;
SELECT 'keyword', COUNT(*) FROM keyword;
SELECT 'link_type', COUNT(*) FROM link_type;
SELECT 'movie_companies', COUNT(*) FROM movie_companies;
SELECT 'movie_info', COUNT(*) FROM movie_info;
SELECT 'movie_keyword', COUNT(*) FROM movie_keyword;
SELECT 'movie_link', COUNT(*) FROM movie_link;
SELECT 'title', COUNT(*) FROM title;
SQL
