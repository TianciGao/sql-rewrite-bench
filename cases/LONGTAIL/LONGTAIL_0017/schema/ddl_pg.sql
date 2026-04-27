CREATE TABLE Users (
  Id INT,
  DisplayName TEXT,
  Reputation INT,
  CreationDate TEXT,
  LastAccessDate TEXT,
  UpVotes INT,
  DownVotes INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  ViewCount INT
);
