-- Case-local witness data for PERF_0103 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO cast_info VALUES
  (1, 1, '(producer)'),
  (2, 2, '(executive producer)');

INSERT INTO info_type VALUES
  (1, 'budget'),
  (2, 'votes');

INSERT INTO movie_info VALUES
  (1, 1, '50000'),
  (2, 1, '90000');

INSERT INTO movie_info_idx VALUES
  (1, 2, '300'),
  (2, 2, '800');

INSERT INTO name VALUES
  (1, 'Tim Alpha', 'm'),
  (2, 'Tim Zulu', 'm');

INSERT INTO title VALUES
  (1, 'Alpha Producer Film'),
  (2, 'Zulu Executive Film');
