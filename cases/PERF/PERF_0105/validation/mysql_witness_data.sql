-- Case-local witness data for PERF_0105 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name VALUES
  (1, '[de]', 'Nordic Noir Co');

INSERT INTO company_type VALUES
  (1, 'production companies');

INSERT INTO info_type VALUES
  (1, 'countries'),
  (2, 'rating');

INSERT INTO keyword VALUES
  (1, 'violence'),
  (2, 'murder');

INSERT INTO kind_type VALUES
  (1, 'movie');

INSERT INTO movie_companies VALUES
  (1, 1, 1, '(2008)'),
  (2, 1, 1, '(2009)');

INSERT INTO movie_info VALUES
  (1, 1, 'Germany'),
  (2, 1, 'Sweden');

INSERT INTO movie_info_idx VALUES
  (1, 2, '7.2'),
  (2, 2, '6.5');

INSERT INTO movie_keyword VALUES
  (1, 1),
  (2, 2);

INSERT INTO title VALUES
  (1, 'Alpha Violence Film', 1, 2008),
  (2, 'Zulu Murder Film', 1, 2009);
