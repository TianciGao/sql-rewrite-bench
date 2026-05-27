-- DRAFT DDL only; not executed in this task
CREATE TABLE league (id INT, name STRING) USING parquet;
CREATE TABLE match_tbl (id INT, league_id INT, season STRING, home_team_goal INT, away_team_goal INT) USING parquet;
