CREATE TABLE Users (
  Id INT,
  DisplayName TEXT,
  Reputation INT,
  CreationDate TEXT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT
);
