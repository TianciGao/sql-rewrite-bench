CREATE TABLE Users (
  Id INT,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  Score INT
);
