-- DRAFT DDL only; not executed in this task
CREATE TABLE frpm (
  cdscode TEXT,
  fm_count TEXT,
  enrollment_k12 DOUBLE,
  `free meal count (k-12)` TEXT,
  `enrollment (k-12)` DOUBLE
);
CREATE TABLE schools (cdscode TEXT, county TEXT, charter INTEGER, school TEXT);
