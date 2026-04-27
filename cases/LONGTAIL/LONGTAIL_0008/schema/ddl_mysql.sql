CREATE TABLE Users (
  Id INT,
  DisplayName TEXT,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  Title TEXT,
  CreationDate TIMESTAMP,
  Score INT,
  ViewCount INT
);
CREATE TABLE Votes (
  Id INT,
  PostId INT,
  VoteTypeId INT
);
