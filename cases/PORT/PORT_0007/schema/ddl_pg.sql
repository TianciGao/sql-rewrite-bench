-- DRAFT DDL only for PORT_0007; not executed
CREATE TABLE comments (
  text TEXT,
  postid INTEGER,
  score DOUBLE PRECISION -- conservative numeric choice; exact source type may differ
);

CREATE TABLE posts (
  id INTEGER,
  viewcount INTEGER
);
