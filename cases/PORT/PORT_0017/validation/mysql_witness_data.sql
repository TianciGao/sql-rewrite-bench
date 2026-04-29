-- DRAFT witness data only; not executed in this task
INSERT INTO frpm (cdscode, fm_count, enrollment_k12, `free meal count (k-12)`, `enrollment (k-12)`) VALUES
  ('LA_A', '10', 100.0, '10', 100.0),
  ('LA_B', '30', 100.0, '30', 100.0);
INSERT INTO schools (cdscode, county, charter, school) VALUES
  ('LA_A', 'Los Angeles', 0, 'Alpha Academy'),
  ('LA_B', 'Los Angeles', 0, 'Beta Academy');
