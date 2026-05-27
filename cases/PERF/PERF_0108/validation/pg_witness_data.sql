-- Case-local witness data for PERF_0108 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO cast_info VALUES
  (1, 1, '(writer)'),
  (2, 2, '(writer)');

INSERT INTO comp_cast_type VALUES
  (1, 'cast'),
  (2, 'complete+verified');

INSERT INTO complete_cast VALUES
  (1, 1, 2),
  (2, 1, 2);

INSERT INTO info_type VALUES
  (1, 'genres'),
  (2, 'votes');

INSERT INTO keyword VALUES
  (1, 'violence');

INSERT INTO movie_info VALUES
  (1, 1, 'Thriller'),
  (2, 1, 'Horror');

INSERT INTO movie_info_idx VALUES
  (1, 2, '600'),
  (2, 2, '900');

INSERT INTO movie_keyword VALUES
  (1, 1),
  (2, 1);

INSERT INTO name VALUES
  (1, 'Alan Writer', 'm'),
  (2, 'Zed Writer', 'm');

INSERT INTO title VALUES
  (1, 'Alpha Thriller', 2005),
  (2, 'Zulu Horror', 2006);
