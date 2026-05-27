CREATE TABLE Users (
  Id INT,
  DisplayName TEXT
);
CREATE TABLE Posts (
  Id INT,
  Title TEXT,
  CreationDate TEXT,
  Score INT,
  ViewCount INT,
  OwnerUserId INT,
  PostTypeId INT
);
CREATE TABLE Votes (
  Id INT,
  UserId INT,
  VoteTypeId INT
);
CREATE TABLE Badges (
  Id INT,
  UserId INT,
  Class INT
);
