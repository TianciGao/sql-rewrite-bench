CREATE TABLE Users (
  Id INT,
  DisplayName STRING
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  Score INT,
  ViewCount INT
);
