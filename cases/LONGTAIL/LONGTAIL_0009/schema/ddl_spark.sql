CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  Title STRING,
  CreationDate STRING,
  OwnerUserId INT,
  ViewCount INT,
  Score INT,
  AnswerCount INT,
  CommentCount INT,
  PostTypeId INT
);
CREATE TABLE Comments (
  Id INT,
  PostId INT
);
CREATE TABLE Votes (
  Id INT,
  PostId INT,
  VoteTypeId INT
);
