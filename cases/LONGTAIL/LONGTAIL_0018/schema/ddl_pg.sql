CREATE TABLE Users (
  Id INT,
  DisplayName TEXT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  ViewCount INT,
  Score INT
);
