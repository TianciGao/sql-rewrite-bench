INSERT INTO Users VALUES
  (1, 'Alice', 1500),
  (2, 'Bob', 1200);
INSERT INTO Posts VALUES
  (101, 'AliceQuestion', '2023-01-01', 1, 600, 10, 2, 0, 1),
  (102, 'AliceAnswer', '2023-01-02', 1, 200, 3, 0, 0, 2),
  (201, 'BobQuestion', '2023-01-03', 2, 500, 7, 1, 2, 1);
INSERT INTO Comments VALUES
  (1, 102),
  (2, 201),
  (3, 201);
INSERT INTO Votes VALUES
  (1, 101, 2),
  (2, 101, 2),
  (3, 102, 3),
  (4, 201, 2),
  (5, 201, 3);
