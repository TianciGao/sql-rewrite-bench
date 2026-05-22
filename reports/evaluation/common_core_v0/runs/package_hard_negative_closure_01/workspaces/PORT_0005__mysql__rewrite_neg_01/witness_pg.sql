-- DRAFT witness data only; backfilled from existing case-local witness_rows.yaml
INSERT INTO drivers (nationality, dob) VALUES
  ('argentina_null', NULL),
  ('japan_earliest', TIMESTAMP '1979-07-04 00:00:00'),
  ('canada_mid', TIMESTAMP '1985-02-11 00:00:00'),
  ('brazil_latest', TIMESTAMP '1992-09-30 00:00:00');
