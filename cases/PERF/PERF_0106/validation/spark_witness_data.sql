-- Case-local witness data for PERF_0106 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name VALUES
  (1, '[us]');

INSERT INTO company_type VALUES
  (1, 'production companies');

INSERT INTO comp_cast_type VALUES
  (1, 'complete+verified');

INSERT INTO complete_cast VALUES
  (1, 1),
  (2, 1);

INSERT INTO info_type VALUES
  (1, 'release dates');

INSERT INTO keyword VALUES
  (1, 'loner'),
  (2, 'nerd');

INSERT INTO kind_type VALUES
  (1, 'movie');

INSERT INTO movie_companies VALUES
  (1, 1, 1),
  (2, 1, 1);

INSERT INTO movie_info VALUES
  (1, 1, 'USA: 2004', 'internet release'),
  (2, 1, 'USA: 2007', 'internet release');

INSERT INTO movie_keyword VALUES
  (1, 1),
  (2, 2);

INSERT INTO title VALUES
  (1, 'Alpha Loner Movie', 1, 2004),
  (2, 'Zulu Nerd Movie', 1, 2007);
