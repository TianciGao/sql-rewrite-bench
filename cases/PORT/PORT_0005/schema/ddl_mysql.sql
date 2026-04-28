-- DRAFT DDL only for PORT_0005; not executed
CREATE TABLE drivers (
  nationality TEXT,
  dob DATETIME -- conservative choice; source may also tolerate DATE-level storage
);
