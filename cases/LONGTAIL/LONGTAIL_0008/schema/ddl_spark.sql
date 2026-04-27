CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  Title STRING,
  CreationDate TIMESTAMP,
  Score INT,
  ViewCount INT
);
CREATE TABLE Votes (
  Id INT,
  PostId INT,
  VoteTypeId INT
);
