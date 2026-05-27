CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  ViewCount INT,
  Score INT
);
