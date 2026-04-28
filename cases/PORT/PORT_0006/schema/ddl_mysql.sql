-- DRAFT DDL only for PORT_0006; not executed
CREATE TABLE loan (
  status TEXT,
  account_id INT,
  amount DOUBLE -- conservative numeric choice; exact source type may differ
);
