CREATE TABLE Posts (
  Id INT,
  PostTypeId INT,
  Score INT,
  ViewCount INT,
  OwnerUserId INT
);
CREATE TABLE PostTypes (
  Id INT,
  Name TEXT
);
