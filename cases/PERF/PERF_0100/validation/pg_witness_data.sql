-- Case-local witness data for PERF_0100 on PG
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO char_name VALUES
  (1, 'Alpha Hero'),
  (2, 'Bravo Hero');

INSERT INTO cast_info VALUES
  (1, 1, 1, '(producer)'),
  (2, 2, 1, '(producer)');

INSERT INTO company_name VALUES
  (1, '[us]');

INSERT INTO company_type VALUES
  (1, 'production companies');

INSERT INTO movie_companies VALUES
  (1, 1, 1),
  (2, 1, 1);

INSERT INTO role_type VALUES
  (1, 'actor');

INSERT INTO title VALUES
  (1, 'Alpha Producer Story', 2001),
  (2, 'Bravo Producer Story', 2010);
