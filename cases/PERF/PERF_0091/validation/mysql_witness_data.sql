-- Case-local witness data for PERF_0091 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name VALUES
  (1, '[us]', 'Alpha Pictures');

INSERT INTO company_type VALUES
  (1, 'production companies');

INSERT INTO info_type VALUES
  (1, 'rating'),
  (2, 'release dates');

INSERT INTO kind_type VALUES
  (1, 'movie');

INSERT INTO movie_companies VALUES
  (1, 1, 1),
  (2, 1, 1);

INSERT INTO movie_info VALUES
  (1, 2),
  (2, 2);

INSERT INTO movie_info_idx VALUES
  (1, 1, '7.1'),
  (2, 1, '8.0');

INSERT INTO title VALUES
  (1, 'A Champion Tale', 1),
  (2, 'Champion Returns', 1);
