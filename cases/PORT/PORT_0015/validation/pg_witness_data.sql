-- DRAFT witness data only; not executed in this task
INSERT INTO league (id, name) VALUES
  (1, 'Alpha League'),
  (2, 'Beta League');
INSERT INTO match_tbl (id, league_id, season, home_team_goal, away_team_goal) VALUES
  (101, 1, '2009/2010', 3, 1),
  (102, 2, '2009/2010', 0, 2);
