CREATE TABLE users (
  id BIGINT NOT NULL,
  displayname TEXT,
  reputation BIGINT,
  PRIMARY KEY (id)
);

CREATE TABLE posts (
  id BIGINT NOT NULL,
  owneruserid BIGINT,
  posttypeid BIGINT,
  score BIGINT,
  PRIMARY KEY (id)
);

CREATE TABLE badges (
  id BIGINT NOT NULL,
  userid BIGINT,
  class BIGINT,
  name TEXT,
  PRIMARY KEY (id)
);
