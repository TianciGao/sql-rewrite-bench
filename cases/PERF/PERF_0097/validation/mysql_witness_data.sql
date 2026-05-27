-- Case-local witness data for PERF_0097 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name VALUES
  (1, '[us]', 'Alpha Studio'),
  (2, '[us]', 'Beta Studio'),
  (3, '[us]', 'Gamma Studio');

INSERT INTO info_type VALUES
  (1, 'rating'),
  (2, 'rating');

INSERT INTO kind_type VALUES
  (1, 'tv series');

INSERT INTO link_type VALUES
  (1, 'follows'),
  (2, 'sequel');

INSERT INTO movie_companies VALUES
  (1, 1),
  (2, 2),
  (3, 1),
  (4, 3);

INSERT INTO movie_info_idx VALUES
  (1, 1, '7.0'),
  (2, 2, '2.5'),
  (3, 1, '8.0'),
  (4, 2, '2.8');

INSERT INTO movie_link VALUES
  (1, 2, 1),
  (3, 4, 2);

INSERT INTO title VALUES
  (1, 'Pilot Echo', 1, 2004),
  (2, 'A Bad Followup', 1, 2006),
  (3, 'Series Prime', 1, 2005),
  (4, 'B Sequel Return', 1, 2007);
