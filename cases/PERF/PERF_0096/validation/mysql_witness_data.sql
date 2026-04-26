-- Case-local witness data for PERF_0096 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO keyword VALUES
  (1, 'character-name-in-title'),
  (2, '10,000-mile-club');

INSERT INTO link_type VALUES
  (1, 'follows');

INSERT INTO movie_keyword VALUES
  (1, 1),
  (3, 2);

INSERT INTO movie_link VALUES
  (1, 2, 1),
  (3, 4, 1);

INSERT INTO title VALUES
  (1, 'Character Trail'),
  (2, 'Linked Story'),
  (3, 'Distance Movie'),
  (4, 'Far Followup');
