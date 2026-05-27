CREATE TABLE PostHistory (
  Id INT,
  PostId INT,
  CreationDate TIMESTAMP,
  UserId INT
);
CREATE TABLE Posts (
  Id INT,
  Title TEXT,
  Score INT,
  ViewCount INT,
  AnswerCount INT,
  CommentCount INT
);
CREATE TABLE Users (
  Id INT,
  DisplayName TEXT
);
