CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT,
  CreationDate STRING
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT
);
