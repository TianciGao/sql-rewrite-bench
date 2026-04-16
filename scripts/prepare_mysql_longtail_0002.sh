#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS Badges;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  Id BIGINT NOT NULL PRIMARY KEY,
  DisplayName TEXT,
  Reputation BIGINT
);

CREATE TABLE Posts (
  Id BIGINT NOT NULL PRIMARY KEY,
  OwnerUserId BIGINT,
  PostTypeId BIGINT,
  Score BIGINT,
  ViewCount BIGINT
);

CREATE TABLE Badges (
  Id BIGINT NOT NULL PRIMARY KEY,
  UserId BIGINT,
  Class BIGINT,
  Name TEXT
);

INSERT INTO Users (Id, DisplayName, Reputation) VALUES
  (1, 'Alice', 1000),
  (2, 'Bob', 800),
  (3, 'Carol', 700),
  (4, 'Dave', 500);

INSERT INTO Posts (Id, OwnerUserId, PostTypeId, Score, ViewCount) VALUES
  (101, 1, 1, 10, 100),
  (102, 1, 2, 7, 90),
  (103, 1, 2, 5, 80),
  (201, 2, 1, 8, 50),
  (202, 2, 1, 7, 70),
  (301, 3, 2, 8, 40),
  (401, 4, 1, 2, 10),
  (402, 4, 2, 3, 30);

INSERT INTO Badges (Id, UserId, Class, Name) VALUES
  (1, 1, 1, 'Teacher'),
  (2, 1, 2, 'Student'),
  (3, 2, 3, 'Supporter'),
  (4, 3, 2, 'Editor');

SELECT 'Users' AS table_name, COUNT(*) AS row_count FROM Users;
SELECT 'Posts' AS table_name, COUNT(*) AS row_count FROM Posts;
SELECT 'Badges' AS table_name, COUNT(*) AS row_count FROM Badges;
SQL
