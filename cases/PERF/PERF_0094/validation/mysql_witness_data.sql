-- Case-local witness data for PERF_0094 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO cast_info VALUES
  (1, 1, '(writer)'),
  (2, 2, '(written by)');

INSERT INTO info_type VALUES
  (1, 'genres'),
  (2, 'rating');

INSERT INTO movie_info VALUES
  (1, 1, 'Thriller', NULL),
  (2, 1, 'Horror', NULL);

INSERT INTO movie_info_idx VALUES
  (1, 2, '8.5'),
  (2, 2, '8.7');

INSERT INTO name VALUES
  (1, 'f'),
  (2, 'f');

INSERT INTO title VALUES
  (1, 'A Thriller Piece', 2010),
  (2, 'Horror Peak', 2011);
