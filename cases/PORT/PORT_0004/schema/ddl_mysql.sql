-- DRAFT DDL only for PORT_0004; not executed
CREATE TABLE patient (
  id INT,
  sex TEXT,
  diagnosis TEXT,
  birthday DATETIME -- conservative choice; source may also tolerate DATE-level storage
);
