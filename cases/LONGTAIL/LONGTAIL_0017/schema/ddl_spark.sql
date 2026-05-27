CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT,
  CreationDate STRING,
  LastAccessDate STRING,
  UpVotes INT,
  DownVotes INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  ViewCount INT
);
