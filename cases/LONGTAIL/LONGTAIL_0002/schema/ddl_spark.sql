CREATE TABLE users (
  id BIGINT,
  displayname STRING,
  reputation BIGINT
);

CREATE TABLE posts (
  id BIGINT,
  owneruserid BIGINT,
  posttypeid BIGINT,
  score BIGINT
);

CREATE TABLE badges (
  id BIGINT,
  userid BIGINT,
  class BIGINT,
  name STRING
);
