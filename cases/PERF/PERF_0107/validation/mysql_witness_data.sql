-- Case-local witness data for PERF_0107 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name VALUES
  (1, '[de]', 'Atlas Film'),
  (2, '[de]', 'Warner Europa');

INSERT INTO company_type VALUES
  (1, 'production companies');

INSERT INTO comp_cast_type VALUES
  (1, 'cast'),
  (2, 'complete+verified');

INSERT INTO complete_cast VALUES
  (1, 1, 2),
  (2, 1, 2);

INSERT INTO keyword VALUES
  (1, 'sequel');

INSERT INTO link_type VALUES
  (1, 'followed by'),
  (2, 'follows');

INSERT INTO movie_companies VALUES
  (1, 1, 1, NULL),
  (2, 2, 1, NULL);

INSERT INTO movie_info VALUES
  (1, 'Germany'),
  (2, 'English');

INSERT INTO movie_keyword VALUES
  (1, 1),
  (2, 1);

INSERT INTO movie_link VALUES
  (1, 11, 1),
  (2, 12, 2);

INSERT INTO title VALUES
  (1, 'Alpha Sequel', 1980),
  (2, 'Zulu Sequel', 1990);
