-- case_id: PORT_0007
-- draft source id: PORT_PARROT_DRAFT_0001
-- draft-only / not validated
-- target dialect: spark_like_negative
-- DRAFT: Spark hard negative requires review
SELECT text
FROM comments
WHERE postid IN (
  SELECT id
  FROM posts
  WHERE viewcount BETWEEN 100 AND 150
)
ORDER BY score ASC
LIMIT 1
