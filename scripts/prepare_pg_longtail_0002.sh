#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<'SQL'
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS badges CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  displayname TEXT
);

CREATE TABLE posts (
  id BIGINT PRIMARY KEY,
  owneruserid BIGINT,
  posttypeid INT,
  score INT,
  viewcount INT
);

CREATE TABLE badges (
  id BIGINT PRIMARY KEY,
  userid BIGINT,
  class INT
);

INSERT INTO users (id, displayname) VALUES
  (1, 'Alice'),
  (2, 'Bob'),
  (3, 'Carol');

INSERT INTO posts (id, owneruserid, posttypeid, score, viewcount) VALUES
  (1, 1, 1, 10, 60),
  (2, 1, 2, 5, 90),
  (3, 1, 2, 7, 120),
  (4, 2, 1, 8, 50),
  (5, 2, 1, 7, 70),
  (6, 3, 2, 8, 40);

INSERT INTO badges (id, userid, class) VALUES
  (1, 1, 1),
  (2, 1, 2),
  (3, 2, 3),
  (4, 3, 2);

SELECT 'users', COUNT(*) FROM users;
SELECT 'posts', COUNT(*) FROM posts;
SELECT 'badges', COUNT(*) FROM badges;
SQL
