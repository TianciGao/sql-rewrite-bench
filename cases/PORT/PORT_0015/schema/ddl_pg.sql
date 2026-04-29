-- DRAFT DDL only; not executed in this task
CREATE TABLE league (id INTEGER, name TEXT);
CREATE TABLE match_tbl (id INTEGER, league_id INTEGER, season TEXT, home_team_goal INTEGER, away_team_goal INTEGER);
