-- DRAFT witness data only; not executed in this task
INSERT INTO account (account_id, date) VALUES
  (1, DATE '1993-05-10'),
  (2, DATE '1993-03-10');
INSERT INTO loan (account_id, duration, amount) VALUES
  (1, 24, 500.0),
  (2, 18, 100.0);
