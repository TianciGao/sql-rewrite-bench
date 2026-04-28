-- DRAFT DDL only for PORT_0004; not executed
CREATE TABLE patient (
  id INT,
  sex STRING,
  diagnosis STRING,
  birthday TIMESTAMP -- conservative choice; source may also tolerate DATE-level storage
);
