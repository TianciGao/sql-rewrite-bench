CREATE TABLE Users (
  Id INT,
  Reputation INT,
  Views INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  Score INT
);
CREATE TABLE Badges (
  Id INT,
  UserId INT
);
