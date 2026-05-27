-- DRAFT DDL only for PORT_0007; not executed
CREATE TABLE comments (
  text TEXT,
  postid INT,
  score DOUBLE -- conservative numeric choice; exact source type may differ
);

CREATE TABLE posts (
  id INT,
  viewcount INT
);
