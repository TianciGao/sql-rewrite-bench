-- DRAFT DDL only for PORT_0005; not executed
CREATE TABLE drivers (
  nationality STRING,
  dob TIMESTAMP -- conservative choice; source may also tolerate DATE-level storage
);
